# YOLO Demo 测试说明

这个文件夹用于测试 YOLO 环境是否可以正常运行。

## 文件说明

- `test.jpg`：测试图片。
- `yolo11n.pt`：YOLO 测试模型文件，直接放在当前文件夹即可。
- `detect_demo.py`：测试脚本。
- `runs/`：运行后自动生成的结果文件夹。

注意：`yolo11n.pt` 必须和 `detect_demo.py` 放在同一个 `test` 文件夹中，不需要额外安装或解压。

## 运行方法

1. 把压缩包解压到电脑任意位置。
2. 打开 Anaconda Prompt。
3. 进入 YOLO 环境：

```powershell
conda activate yolo
```

4. 在文件资源管理器中找到解压出来的 `YOLO\test` 文件夹。
5. 点击文件资源管理器顶部地址栏，复制当前 `test` 文件夹路径。
6. 回到 Anaconda Prompt，输入 `cd /d`，后面粘贴刚才复制的路径。

示例：

```powershell
cd /d "D:\资料\YOLO\test"
```

注意：不要在普通 cmd 里执行 `conda activate yolo`。如果普通 cmd 无法识别 `conda`，请回到 Anaconda Prompt 操作。

7. 确认命令行前面仍然有 `(yolo)`。如果没有，重新输入：

```powershell
conda activate yolo
```

8. 执行测试脚本：

```powershell
python detect_demo.py
```

## 成功标准

如果命令运行结束后出现下面内容，说明脚本执行完成：

```text
YOLO demo finished.
```

同时，电脑会自动弹出一张已经画好识别框的结果图片。

识别结果仍然会自动保存在当前文件夹下的：

```text
runs\predict
```

一般情况下不需要手动打开这个文件夹。只要脚本运行结束后屏幕上自动弹出带识别框的图片，就说明 YOLO 可以正常运行。
