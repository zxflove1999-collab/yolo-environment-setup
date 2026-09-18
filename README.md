# YOLO Environment Setup Skill

This repository packages a Codex skill and a portable YOLO demo for setting up an Ultralytics YOLO environment on employee computers.

## What Is Included

```text
skill/
└─ yolo-environment-setup/
   ├─ SKILL.md
   └─ agents/

demo/
└─ YOLO/
   └─ test/
      ├─ detect_demo.py
      ├─ README_demo.md
      └─ test.jpg
```

## How To Use

1. Click **Code** on this GitHub page.
2. Click **Download ZIP**.
3. Extract the ZIP file to any folder on the computer.
4. Open Codex.
5. Send Codex this message, replacing the example path with the real ZIP or extracted folder path:

```text
我这里有一个skill，你安装一下，然后给我配置YOLO环境。路径是：D:\Downloads\yolo-environment-setup-main.zip
```

Codex should then install the skill, detect the included demo, configure the YOLO environment, and run the demo. At the end, Codex should report either `配置成功` or `配置失败`.

## Expected Demo Result

The demo runs `demo/YOLO/test/detect_demo.py`.

When successful:

- The command line prints `YOLO demo finished.`
- A result image with detection boxes opens automatically.
- The generated result is saved under `demo/YOLO/test/runs/predict/`.

The `runs/` folder is generated locally and is intentionally not committed to this repository.

## Notes

- CUDA acceleration requires an NVIDIA GPU and a working NVIDIA driver.
- Computers with only Intel or AMD integrated graphics should use the CPU version of PyTorch.
- On the first run, Ultralytics downloads the official `yolo11n.pt` weights if they are not already available. This requires network access.
