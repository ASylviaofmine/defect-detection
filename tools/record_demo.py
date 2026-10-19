"""Record the demo video (screen + microphone) with ffmpeg.

Why this exists: Xbox Game Bar produced a silent audio track on this machine
even though the microphone itself works (verified: ffmpeg direct capture gives
-18 dB). This script bypasses Game Bar entirely.

Usage
-----
    python tools/record_demo.py s1          # countdown, record, press Enter to stop
    python tools/record_demo.py s1 --seconds 20   # fixed length, auto stop
    python tools/record_demo.py --list      # show detected microphones

Output: %USERPROFILE%\\Videos\\Captures\\<name>.mp4

After each recording the script measures the audio and prints the level, so
"did it actually record sound?" is answered by a number instead of by ear.
"""

import argparse
import datetime as _dt
import os
import re
import subprocess
import sys
import time
from pathlib import Path

FFMPEG = None
OUT_DIR = Path(os.environ.get("USERPROFILE", ".")) / "Videos" / "Captures"


def ffmpeg_exe() -> str:
    global FFMPEG
    if FFMPEG:
        return FFMPEG
    try:
        import imageio_ffmpeg
        FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("缺少 imageio-ffmpeg,先运行:\n    pip install --user imageio-ffmpeg")
    return FFMPEG


def list_audio_devices() -> list:
    """Return the DirectShow audio capture device names ffmpeg can see."""
    p = subprocess.run(
        [ffmpeg_exe(), "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return re.findall(r'"([^"]+)"\s+\(audio\)', p.stderr)


def pick_microphone() -> str:
    """Prefer the built-in array; skip disconnected USB / bluetooth endpoints."""
    devices = list_audio_devices()
    if not devices:
        sys.exit("没有找到可用的麦克风。检查系统声音设置里是否有输入设备。")
    for key in ("麦克风阵列", "Microphone Array", "Realtek"):
        for d in devices:
            if key.lower() in d.lower():
                return d
    return devices[0]


def measure_audio(path: Path) -> None:
    """Print mean/max volume so silence is impossible to miss."""
    p = subprocess.run(
        [ffmpeg_exe(), "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", p.stderr)
    peak = re.search(r"max_volume:\s*(-?[\d.]+) dB", p.stderr)
    if not mean:
        print("  ⚠ 测不到音轨 —— 这个文件可能没有声音")
        return
    m, pk = float(mean.group(1)), float(peak.group(1)) if peak else -99.0
    if m < -70:
        print(f"  ⚠ 音量 {m:.1f} dB —— 这是静音,重录(检查麦克风是否被占用)")
    elif m > -8:
        print(f"  ⚠ 音量 {m:.1f} dB —— 太响,可能爆音,建议离麦远一点")
    else:
        print(f"  ✓ 音量 {m:.1f} dB(峰值 {pk:.1f} dB)—— 有声音")


def _console_hwnd():
    try:
        import ctypes
        return ctypes.windll.kernel32.GetConsoleWindow()
    except Exception:
        return 0


def _set_console(show: bool) -> None:
    """Hide the console while recording so it is not in the frame."""
    hwnd = _console_hwnd()
    if not hwnd:
        return
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(hwnd, 9 if show else 6)   # 9 = restore, 6 = minimize
    except Exception:
        pass


def main() -> None:
    ap = argparse.ArgumentParser(description="Record screen + microphone to mp4")
    ap.add_argument("name", nargs="?", help="output file name, e.g. s1")
    ap.add_argument("--seconds", type=float, default=0, help="auto-stop after N seconds")
    ap.add_argument("--list", action="store_true", help="list microphones and exit")
    ap.add_argument("--mic", default=None, help="microphone name (default: built-in array)")
    ap.add_argument("--keep-console", action="store_true",
                    help="do not minimise the terminal while recording")
    args = ap.parse_args()

    if args.list:
        print("可用麦克风:")
        for d in list_audio_devices():
            print("  -", d)
        return

    if not args.name:
        ap.error("需要给一个名字,例如: python tools/record_demo.py s1")

    mic = args.mic or pick_microphone()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.name}.mp4"

    print(f"麦克风: {mic}")
    print(f"输出  : {out}")
    for i in (3, 2, 1):
        print(f"  {i}...", end="", flush=True)
        time.sleep(1)
    print(" 开始录制" + (f"(录 {args.seconds:.0f} 秒)" if args.seconds else "(按 Enter 停止)") + "\n")

    # Auto-stop recordings minimise the console so the terminal is not in frame.
    hide_console = args.seconds > 0 and not args.keep_console

    cmd = [
        ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
        "-f", "gdigrab", "-framerate", "30", "-draw_mouse", "1", "-i", "desktop",
        "-f", "dshow", "-i", f"audio={mic}",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "21", "-pix_fmt", "yuv420p",
        "-r", "30", "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart",
    ]
    if args.seconds > 0:
        cmd += ["-t", str(args.seconds)]
    cmd.append(str(out))

    t0 = time.time()
    if hide_console:
        _set_console(False)                       # minimised *before* ffmpeg grabs the screen
        time.sleep(0.3)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
    try:
        if args.seconds > 0:
            proc.wait()
        else:
            input()
            proc.communicate(b"q\n", timeout=20)
    except KeyboardInterrupt:
        proc.communicate(b"q\n", timeout=20)
    finally:
        if proc.poll() is None:
            proc.kill()
        if hide_console:
            _set_console(True)                    # bring the terminal back

    secs = time.time() - t0
    if not out.exists():
        err = (proc.stderr.read().decode("utf-8", "replace") if proc.stderr else "")
        sys.exit(f"录制失败,ffmpeg 没有产出文件。\n{err[-600:]}")

    size_mb = out.stat().st_size / 1024 / 1024
    print(f"\n完成: {secs:.1f} 秒,{size_mb:.1f} MB")
    print(f"文件: {out}")
    measure_audio(out)


if __name__ == "__main__":
    main()
