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
