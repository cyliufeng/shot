# Screenshot tool

This tool uses `mss` to capture the configured screen area once per second and saves JPEG files named with the capture time.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python screenshot_tool.py
```

By default images are saved under `screenshots\`. Use `-o` to choose another directory:

```powershell
python screenshot_tool.py --output-dir D:\captures
```

The configured region is `left=330`, `top=285`, `width=931`, `height=695`.
The script validates that this region fits within the virtual desktop before starting. On a 1920x1080 monitor, this region ends at `right=1261`, `bottom=980` and fits within the screen.

## YOLOv8 显卡训练

请使用项目自己的 `.venv`，其他 Python 环境中安装的 PyTorch 不会自动生效。
当前已验证的环境是 Python 3.11.9、Ultralytics 8.4.215、
PyTorch 2.5.1+cu118、torchvision 0.20.1+cu118，显卡为 GTX 1650（4 GB）。

重新配置环境时，先安装普通依赖，再安装 CUDA 版 PyTorch：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu118
```

在项目目录执行以下命令启动训练：

```powershell
.\.venv\Scripts\python.exe train_yolo.py
```

脚本使用 `dataset/data.yaml`，直接读取 `dataset/images/train` 和
`dataset/images/val` 中的图片及对应标签。现有数据为 74 张训练图、18 张验证图；
其中 15 张已确认没有目标的图片配有空标签文件。原始截图保留在 `screenshots`。
`dataset/train.txt`、`dataset/val.txt` 仅保留为图片清单，当前训练配置不读取这两个文件。

训练配置为 YOLOv8 nano、图片尺寸 640、每批 2 张、最多 50 轮；
验证指标连续 15 轮没有改善时提前结束。GTX 1650 使用全精度训练（`amp=False`）。
首次运行可能需要下载官方 `yolov8n.pt` 预训练权重。

训练结果保存在 `runs/detect/yolov8n_game_gpu`；再次训练会自动使用新目录。
`weights/best.pt` 是验证效果最好的模型，`weights/last.pt` 是最后一轮模型，
`results.csv` 和 `results.png` 记录训练指标。验证图来自同一段游戏截图，
因此指标只能用于初步检查；还需要用其他游戏片段的图片检查实际识别效果。
