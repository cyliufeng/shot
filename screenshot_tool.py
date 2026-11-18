"""每秒截取一次固定屏幕区域，并保存为 JPEG 图片。

安装依赖：
    python -m pip install -r requirements.txt

运行程序：
    python screenshot_tool.py
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import mss
from PIL import Image


# 截图区域和截图间隔设置。
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CAPTURE_LEFT = 330
CAPTURE_TOP = 285
CAPTURE_WIDTH = 931
CAPTURE_HEIGHT = 695
CAPTURE_INTERVAL_SECONDS = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="每秒截取一次指定的屏幕区域。"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("screenshots"),
        help="截图文件的保存目录（默认为 screenshots）。",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=CAPTURE_INTERVAL_SECONDS,
        help="两次截图之间的秒数（默认为 1 秒）。",
    )
    return parser.parse_args()


def validate_interval(interval: float) -> None:
    if interval <= 0:
        raise ValueError("--interval 必须大于 0。")


def validate_region(monitor: dict[str, int]) -> None:
    """检查截图区域是否位于虚拟屏幕范围内；超出时给出错误信息。"""
    screen_left = monitor["left"]
    screen_top = monitor["top"]
    screen_right = screen_left + monitor["width"]
    screen_bottom = screen_top + monitor["height"]
    capture_right = CAPTURE_LEFT + CAPTURE_WIDTH
    capture_bottom = CAPTURE_TOP + CAPTURE_HEIGHT

    if (
        CAPTURE_LEFT < screen_left
        or CAPTURE_TOP < screen_top
        or capture_right > screen_right
        or capture_bottom > screen_bottom
    ):
        raise ValueError(
            "截图区域超出了当前虚拟屏幕的范围。"
            f"截图区域：左={CAPTURE_LEFT}，上={CAPTURE_TOP}，"
            f"宽={CAPTURE_WIDTH}，高={CAPTURE_HEIGHT}；"
            f"虚拟屏幕：左={screen_left}，上={screen_top}，"
            f"宽={monitor['width']}，高={monitor['height']}。"
            f"对于 {SCREEN_WIDTH}x{SCREEN_HEIGHT} 的屏幕，"
            f"截图区域的右边界和下边界分别为 {capture_right} 和 {capture_bottom}。"
        )


def capture_loop(output_dir: Path, interval: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with mss.mss() as sct:
        # monitors[0] 表示完整的虚拟桌面，包含所有显示器。
        monitor = sct.monitors[0]
        validate_region(monitor)

        region = {
            "left": CAPTURE_LEFT,
            "top": CAPTURE_TOP,
            "width": CAPTURE_WIDTH,
            "height": CAPTURE_HEIGHT,
        }

        print(
            f"Capturing {CAPTURE_WIDTH}x{CAPTURE_HEIGHT} at "
            f"({CAPTURE_LEFT}, {CAPTURE_TOP}) every {interval:g}s. "
            f"Saving to: {output_dir.resolve()}"
        )
        print("按 Ctrl+C 停止截图。")

        next_capture = time.monotonic()
        while True:
            now = time.monotonic()
            if now < next_capture:
                time.sleep(next_capture - now)

            screenshot = sct.grab(region)
            image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
            image.save(output_dir / filename, format="JPEG", quality=95)
            print(f"Saved: {filename}")

            # 即使保存图片耗费少量时间，也尽量保持固定截图间隔。
            # 如果程序执行落后，则从当前时间重新计时，避免连续截图。
            next_capture += interval
            if next_capture <= time.monotonic():
                next_capture = time.monotonic() + interval


def main() -> int:
    args = parse_args()
    try:
        validate_interval(args.interval)
        capture_loop(args.output_dir, args.interval)
    except KeyboardInterrupt:
        print("\n截图已停止。")
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
