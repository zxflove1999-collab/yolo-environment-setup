---
name: yolo-environment-setup
description: Install and use a packaged YOLO/Ultralytics setup skill, then configure a Windows-focused YOLO environment with Conda, PyTorch CPU/GPU selection, verification, and an included portable demo.
---

# Yolo Environment Setup

Use this skill when the user asks to install a YOLO setup skill from a provided package, deploy or troubleshoot a YOLO/Ultralytics object-detection environment, or run the included YOLO demo to verify success.

## Primary Outcome

Produce a practical, beginner-friendly workflow that lets a non-computer-science employee:

1. Check whether the machine can use NVIDIA GPU acceleration.
2. Use an existing Conda/Miniconda installation when present.
3. Create and activate an isolated `yolo` environment.
4. Install the correct PyTorch build and Ultralytics YOLO.
5. Verify installation with simple success markers.
6. Run a portable demo that opens the detected image automatically.

## Self-Install From A Package

This skill is designed to be distributed inside a package. If the user says anything like "I have a skill here; install it and configure YOLO", treat the package path they provide as the only required starting input.

Expected package layout:

```text
YOLO环境配置完整包
├─ skill
│  └─ yolo-environment-setup
│     ├─ SKILL.md
│     └─ agents
└─ demo
   └─ YOLO
      └─ test
         ├─ test.jpg
         ├─ yolo11n.pt
         ├─ detect_demo.py
         └─ README_demo.md
```

When given a `.zip` file path:

1. Extract it to a temporary or adjacent folder if it has not already been extracted.
2. Locate the folder that contains `skill/yolo-environment-setup/SKILL.md`.
3. Locate the demo folder containing `test.jpg`, `yolo11n.pt`, and `detect_demo.py`.

When given an extracted folder path:

1. Search that folder recursively for `skill/yolo-environment-setup/SKILL.md`.
2. Search that folder recursively for a directory containing all three demo files: `test.jpg`, `yolo11n.pt`, and `detect_demo.py`.

Install or update the skill by copying the package's `skill/yolo-environment-setup` folder to:

```text
%USERPROFILE%\.codex\skills\yolo-environment-setup
```

If an older `yolo-environment-setup` folder already exists, update it in place unless the user has asked not to. Do not require the user to manually install the skill or manually identify the demo path when these can be discovered from the package.

After installing the skill, continue the setup workflow in the same task. Do not stop after installation.

Minimum user prompt this skill should support:

```text
我这里有一个skill，你安装一下，然后给我配置YOLO环境。
```

If that prompt includes a package path, use it directly. If no package path is present and no attached/existing path is available, ask for the path to the downloaded zip file or extracted package folder.

## Environment Detection Rules

Do not assume ordinary PowerShell can find Conda. Use this decision order:

1. In ordinary PowerShell, try `conda --version`.
2. If PowerShell cannot recognize `conda`, do not conclude Conda is absent.
3. Search Windows for `Anaconda Prompt`, `Miniconda Prompt`, or `Anaconda PowerShell Prompt`.
4. If one exists, open it and run `conda --version` there.
5. Only recommend installing Miniconda when both ordinary PowerShell and Windows search fail to locate a usable Conda prompt.

When documenting this, explicitly explain that ordinary PowerShell may fail because Conda was not added to PATH.

Prefer doing checks directly for the user instead of asking them to run commands manually, unless a GUI installer, admin approval, or unavailable path blocks automation.

## GPU Versus CPU PyTorch

CUDA is only for NVIDIA GPUs.

Use `nvidia-smi` as the first practical check. If it works and shows an NVIDIA GPU, install a CUDA/GPU PyTorch build. If it fails, ask the user to check Windows Device Manager under Display adapters:

- If there is no NVIDIA adapter and only Intel/AMD integrated graphics appears, choose the CPU PyTorch build.
- If an NVIDIA adapter exists but `nvidia-smi` fails, repair or install the NVIDIA driver before choosing CUDA.

When choosing a PyTorch CUDA option, choose a version that is not higher than the `CUDA Version` shown by `nvidia-smi`. For example, if `nvidia-smi` shows CUDA 13.1 and PyTorch offers CUDA 12.6, 13.0, and 13.2, choose CUDA 13.0 rather than CUDA 13.2.

For CPU-only machines, state clearly that YOLO can still run, but it will be slower and may not be suitable for heavy batch or video workloads.

## Documentation Style

Write the document as if the reader is a beginner. Prefer exact commands, visible success phrases, and screenshots over conceptual explanations. Avoid long parameter analysis unless it changes an action the employee must take.

Important success markers:

- `Successfully installed` after `pip install -U ultralytics` means the YOLO package installed.
- `Setup complete` after `yolo checks` means YOLO environment checks passed.
- `True` from `python -c "import torch; print(torch.cuda.is_available())"` means PyTorch can use the NVIDIA GPU.

Do not include user-specific absolute paths in employee-facing instructions unless the document is explicitly for that one machine. Use relative paths or tell the employee to copy their own folder path.

## Recommended Setup Flow

Use this high-level sequence unless the user asks otherwise:

1. If the user provided a package, install/update the skill from the package and locate the demo folder automatically.
2. Check NVIDIA driver/GPU with `nvidia-smi`; if it fails, use Device Manager or available system information to decide CPU versus CUDA.
3. Check for Conda using the decision order above.
4. If needed, install Miniconda. Prefer `Just Me`, avoid adding Conda to PATH, and use Anaconda/Miniconda Prompt for commands.
5. Create the environment:

```powershell
conda create -n yolo python=3.10 -y
conda activate yolo
```

6. Install PyTorch from the official PyTorch selector using the correct CPU/CUDA option.
7. Install YOLO:

```powershell
pip install -U ultralytics
yolo checks
```

8. Run the located demo.

If network access, installer approval, admin rights, or missing hardware blocks completion, report `配置失败` and the exact blocked step. Otherwise finish with `配置成功`.

## Portable Demo Package

When preparing a demo folder, make it portable and avoid user-specific paths. Recommended structure:

```text
YOLO
└─ test
   ├─ test.jpg
   ├─ yolo11n.pt
   ├─ detect_demo.py
   └─ README_demo.md
```

The demo script should:

- Load `test.jpg` and `yolo11n.pt` from the same folder as the script.
- Save results under `runs/predict`.
- Automatically open the result image after inference.
- Print `YOLO demo finished.` when complete.

Use this pattern for the script:

```python
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
```

The employee-facing demo instructions should keep all commands in Anaconda Prompt. Do not tell employees to type `cmd` in File Explorer and then run `conda activate yolo`, because ordinary cmd may not know `conda`.

Recommended demo run steps:

1. Use the located `YOLO\test` folder from the package.
2. Run the demo inside the `yolo` environment.
3. Prefer direct invocation through the environment Python when available, for example:

```powershell
%USERPROFILE%\miniconda3\envs\yolo\python.exe detect_demo.py
```

4. If using an interactive terminal, keep commands in Anaconda Prompt, not ordinary cmd.

Success criteria:

1. No red error appears.
2. The command line prints `YOLO demo finished.`
3. A result image with detection boxes opens automatically.

Final response must clearly say one of:

```text
配置成功
```

or:

```text
配置失败
```

For success, include the demo folder path and note that the result image opened automatically. For failure, include the failing command or step and the next action needed from the user.

## Common Miniconda Install Issue

If the installer reports:

```text
Directory 'C:\Users\用户名\miniconda3' is not empty, please choose a different location.
```

Explain that the directory already contains files. Prefer choosing a new empty install directory such as:

```text
C:\Users\用户名\miniconda3_yolo
```

Do not casually instruct employees to delete an existing `miniconda3` folder unless they have confirmed it is safe.
