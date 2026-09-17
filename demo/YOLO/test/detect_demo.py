import os
import platform
import subprocess
from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
IMAGE = ROOT / "test.jpg"
MODEL = ROOT / "yolo11n.pt"
RESULT_DIR = ROOT / "runs" / "predict"
RESULT_IMAGE = RESULT_DIR / IMAGE.name

if not IMAGE.exists():
    raise FileNotFoundError(f"Test image not found: {IMAGE}")

if not MODEL.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL}")

model = YOLO(str(MODEL))
model.predict(source=str(IMAGE), save=True, project=str(ROOT / "runs"), name="predict", exist_ok=True)

if not RESULT_IMAGE.exists():
    raise FileNotFoundError(f"Result image not found: {RESULT_IMAGE}")

system = platform.system()
if system == "Windows":
    os.startfile(RESULT_IMAGE)
elif system == "Darwin":
    subprocess.run(["open", str(RESULT_IMAGE)], check=False)
else:
    subprocess.run(["xdg-open", str(RESULT_IMAGE)], check=False)

print("YOLO demo finished.")
print(f"Input image: {IMAGE}")
print(f"Model file: {MODEL}")
print(f"Result image opened: {RESULT_IMAGE}")
