#!/usr/bin/env python3
"""Build the Windows recovery shell with Zig 0.13.0 (Windows or Linux host)."""
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
ZIG = os.environ.get("ZIG", "zig")
OUTPUT = ROOT / "release" / "Nexida-Recovery.exe"


def run(*args, cwd):
    print("+", " ".join(map(str, args)), flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def main():
    png = (ROOT / "recovered-resources" / "icon.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Recovered icon is not a PNG")
    with tempfile.TemporaryDirectory(prefix="nexida-build-") as temporary:
        temp = Path(temporary)
        # ICO container with one 256x256 PNG entry. The image itself is unchanged.
        ico = struct.pack("<HHHBBBBHHII", 0, 1, 1, 0, 0, 0, 0, 1, 32, len(png), 22) + png
        (temp / "icon.ico").write_bytes(ico)
        shutil.copyfile(ROOT / "recovered-resources" / "app.manifest", temp / "app.manifest")
        (temp / "resources.rc").write_text(
            '1 ICON "icon.ico"\n1 24 "app.manifest"\n', encoding="ascii"
        )
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        run(ZIG, "rc", "/fo", "resources.res", "resources.rc", cwd=temp)
        run(ZIG, "cc", "-target", "x86_64-windows-gnu", "-std=c11", "-O2",
            "-Wall", "-Wextra", "-Werror", "-s", "-municode", "-Wl,--subsystem,windows",
            str(ROOT / "windows-shell" / "main.c"), "resources.res", "-lgdi32", "-luser32",
            "-o", str(OUTPUT), cwd=temp)
    print("Built:", OUTPUT)


if __name__ == "__main__":
    main()
