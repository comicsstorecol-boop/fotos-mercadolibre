import sys, glob, json, numpy as np, cv2
from insightface.app import FaceAnalysis
app = FaceAnalysis(name="buffalo_s", root="/home/claude/narr", allowed_modules=["detection", "landmark_2d_106"], providers=["CPUExecutionProvider"])
app.prepare(ctx_id=-1, det_size=(640, 640))
out = {}
for clip in sys.argv[1:]:
    fs = sorted(glob.glob(f"{clip}/*.jpg")); vals = []; boxes = []
    for f in fs:
        im = cv2.imread(f); faces = app.get(im)
        if not faces: vals.append(None); boxes.append(None); continue
        fc = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
        lm = fc.landmark_2d_106; m = lm[52:72]; fh = fc.bbox[3] - fc.bbox[1]
        vals.append(float((m[:, 1].max() - m[:, 1].min()) / fh)); boxes.append([float(v) for v in fc.bbox]); 
    out[clip] = {"boca": vals, "bbox": boxes}
    ok = [v for v in vals if v is not None]; print(clip, len(fs), "caras", len(ok), "min", round(min(ok), 3), "max", round(max(ok), 3), flush=True)
json.dump(out, open("boca.json", "w"))
