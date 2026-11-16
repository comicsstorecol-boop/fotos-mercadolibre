"""Mejora de resolución x2 con IA (Real-ESRGAN x2plus). Uso: python3 herramientas/mejorar_imagen.py entrada.png salida.png
Pesos: curl -L -o /tmp/x2.pth https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth ; pip install spandrel"""
import sys, torch, numpy as np, time
from PIL import Image
from spandrel import ModelLoader
m = ModelLoader().load_from_file(__import__("os").environ.get("ESRGAN", "/tmp/x2.pth")).model.eval()
torch.set_num_threads(4)
def up(src, dst, tile=256, pad=16):
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255
    H, W, _ = im.shape; out = np.zeros((H * 2, W * 2, 3), np.float32)
    for y in range(0, H, tile):
        for x in range(0, W, tile):
            y0, x0 = max(0, y - pad), max(0, x - pad); y1, x1 = min(H, y + tile + pad), min(W, x + tile + pad)
            t = torch.from_numpy(im[y0:y1, x0:x1]).permute(2, 0, 1)[None]
            with torch.no_grad(): r = m(t)[0].permute(1, 2, 0).clamp(0, 1).numpy()
            yy, xx = (y - y0) * 2, (x - x0) * 2; hh, ww = min(tile, H - y) * 2, min(tile, W - x) * 2
            out[y * 2:y * 2 + hh, x * 2:x * 2 + ww] = r[yy:yy + hh, xx:xx + ww]
    Image.fromarray((out * 255).round().astype(np.uint8)).save(dst)
t = time.time(); up(sys.argv[1], sys.argv[2]); print("ok", round(time.time() - t), "s")
