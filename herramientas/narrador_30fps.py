"""Pasa el narrador gamer a 30 fps reales (interpolación de movimiento) y rehace los primeros planos horizontales cv*.
Correr UNA vez después de setup.sh:  python3 herramientas/narrador_30fps.py   (~7 min). El repo guarda los clips originales a 24 fps."""
import json, subprocess, numpy as np, os, glob
import sys
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); G=os.path.join(K,"biblioteca","narrador","gamer"); O="/tmp/narr_orig24"
if not os.path.isdir(O):
    import shutil; shutil.copytree(G,O)
MI="minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
def run(a): subprocess.run(a, check=True)
def nfr(p): return int(subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=nb_read_frames","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
for ori in ("v","h"):
    for f in sorted(glob.glob(f"{O}/{ori}/*.mp4")):
        nom=os.path.basename(f)
        if nom.startswith("cv"): continue
        run(["ffmpeg","-loglevel","error","-y","-i",f,"-vf",MI,"-c:v","libx264","-crf","15","-preset","medium","-an",f"{G}/{ori}/{nom}"]); print("30fps",ori,nom,flush=True)
y0s={"cv1_0":335,"cv1_1":333,"cv2_0":513,"cv3_0":330,"cv4_0":329,"cv5_0":384,"cv6_0":432,"cv6_1":401}
for nom,y0 in y0s.items():
    run(["ffmpeg","-loglevel","error","-y","-i",f"{G}/v/{nom[1:]}.mp4","-vf",f"crop=1080:608:0:{y0},scale=1920:1080:flags=lanczos,cas=0.55","-c:v","libx264","-crf","15","-preset","medium","-an",f"{G}/h/{nom}.mp4"]); print("cerca",nom,flush=True)
d=json.load(open(f"{O}/boca.json")); out={}
for k,v in d.items():
    ori,nom=k.split("/"); n30=nfr(f"{G}/{ori}/{nom}.mp4"); n24=len(v["boca"])
    src=np.arange(n24); dst=np.clip(np.arange(n30)*24/30,0,n24-1)
    b=np.array([np.nan if x is None else x for x in v["boca"]],float); ok=~np.isnan(b)
    bi=np.interp(dst,src[ok],b[ok]).tolist()
    bb=[]
    for t in dst:
        j=int(round(t)); bb.append(v["bbox"][min(j,n24-1)])
    out[k]={"boca":bi,"bbox":bb}
json.dump(out,open(f"{G}/boca.json","w")); print("boca.json listo", len(out))
import shutil; shutil.rmtree("/tmp/narrador_frames/gamer", ignore_errors=True); print("LISTO")
