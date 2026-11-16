import sys, torch, torchaudio, json, numpy as np, soundfile as sf
import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'knnvc') + '/'
sys.path.insert(0, D + 'repo')
from wavlm.WavLM import WavLM, WavLMConfig
from hifigan.models import Generator as HiFiGAN
from hifigan.utils import AttrDict
from matcher import KNeighborsVC
torch.set_num_threads(2)
def _sf_load(path, *a, **k):
    d, sr = sf.read(str(path), dtype='float32', always_2d=True)
    return torch.tensor(d.T), sr
torchaudio.load = _sf_load
_m = None
def model():
    global _m
    if _m is None:
        ck = torch.load(D + 'WavLM-Large.pt', map_location='cpu'); w = WavLM(WavLMConfig(ck['cfg'])); w.load_state_dict(ck['model']); w.eval()
        h = AttrDict(json.load(open(D + 'repo/hifigan/config_v1_wavlm.json')))
        g = HiFiGAN(h); g.load_state_dict(torch.load(D + 'prematch_g_02500000.pt', map_location='cpu')['generator']); g.eval(); g.remove_weight_norm()
        _m = KNeighborsVC(w, g, h, 'cpu')
    return _m
_ref = {}
BLEND_LO, BLEND_HI, BLEND_MAX, BLEND_BASE = [float(v) for v in os.environ.get("VOZ_BLEND", "0.42,0.56,0.5,0.04").split(",")]
def ref_features(ref):
    """Features of the reference voice, computed in 20 s chunks and cached next to the file."""
    import os, subprocess, tempfile, glob
    cache = os.path.splitext(ref)[0] + ".feats.pt"
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(ref):
        return torch.load(cache)
    m = model(); feats = []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ref, "-ac", "1", "-ar", "16000",
                        "-f", "segment", "-segment_time", "20", f"{td}/c%03d.wav"], check=True)
        with torch.inference_mode():
            for p in sorted(glob.glob(f"{td}/c*.wav")):
                feats.append(m.get_features(p).cpu())
    f = torch.cat(feats, dim=0); torch.save(f, cache); return f

def convert(x, sr, ref_paths, topk=4):
    """x: float32 mono at sr -> converted float32 at 16k"""
    m = model(); key = tuple(ref_paths)
    if key not in _ref: _ref[key] = torch.cat([ref_features(p) for p in ref_paths], dim=0)
    t = torch.tensor(x, dtype=torch.float32)[None]
    if sr != 16000: t = torchaudio.functional.resample(t, sr, 16000)
    from matcher import fast_cosine_dist
    import torch.nn.functional as Fn
    R = _ref[key]
    with torch.inference_mode():
        q = m.get_features(t)
        # por bloques para no agotar la memoria con referencias largas
        idx, vals = [], []
        for i in range(0, q.shape[0], 64):
            b = fast_cosine_dist(q[i:i + 64], R).topk(k=topk, largest=False, dim=-1); idx.append(b.indices); vals.append(b.values)
        idx, vals = torch.cat(idx), torch.cat(vals)
        matched = R[idx].mean(dim=1)
        # blend the original (clear) pronunciation back in where the reference voice has no good match
        d = vals.mean(dim=1)
        w = ((d - BLEND_LO) / (BLEND_HI - BLEND_LO)).clamp(0, 1) * BLEND_MAX + BLEND_BASE
        w = Fn.avg_pool1d(w[None, None], 5, 1, 2, count_include_pad=False)[0, 0].clamp(0, 1)
        feats = (1 - w[:, None]) * matched + w[:, None] * q
        out = m.vocode(feats[None]).cpu().squeeze()
        lo = torchaudio.functional.loudness(out[None], 16000)
        out = torchaudio.functional.gain(out, -16 - lo)
    return out.numpy().astype(np.float32)
