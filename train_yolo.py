"""使用项目数据集，在 NVIDIA 显卡上训练 YOLOv8 敌人和人质检测模型。"""

from pathlib import Path
import os


# 使用脚本所在目录，避免从其他目录启动时找不到数据或权重。
PROJECT_DIR = Path(__file__).resolve().parent
os.environ["YOLO_CONFIG_DIR"] = str(PROJECT_DIR / ".ultralytics")

import torch
from ultralytics import YOLO


def main() -> None:
    """检查显卡后启动训练；训练结果自动保存到 runs/detect 下。"""
    if not torch.cuda.is_available():
        raise RuntimeError(
            "当前 Python 环境无法使用 CUDA，请使用项目 .venv 并安装 CUDA 版 PyTorch。"
        )

    print(f"训练显卡：{torch.cuda.get_device_name(0)}")
    model = YOLO(str(PROJECT_DIR / "yolov8n.pt"))
    model.train(
        data=str(PROJECT_DIR / "dataset" / "data.yaml"),
        epochs=50,
        imgsz=640,
        batch=2,  # GTX 1650 的显存为 4 GB，先使用较小的批次。
        device=0,
        amp=False,  # GTX 1650 使用全精度训练，避免混合精度出现异常损失。
        workers=0,  # Windows 下先使用主进程读取数据，便于排查问题。
        patience=15,
        cache=False,
        project=str(PROJECT_DIR / "runs" / "detect"),
        name="yolov8n_game_gpu",  # 同名目录存在时自动生成新目录，保留历史结果。
    )


if __name__ == "__main__":
    main()
