# import os, sys, subprocess, platform
# from pathlib import Path

# REPO = Path(__file__).resolve().parent
# VENV = REPO / ".venvExm"
# PKG  = REPO.parent / "simEngine"
# # print(PKG)
# DEFAULT_SCRIPT = REPO / "desktopApp.py"
# # print(DEFAULT_SCRIPT)
# def venv_python():
#     if platform.system() == "Windows":
#         return VENV / "Scripts" / "python.exe"
#     return VENV / "bin" / "python"

# def run(cmd):
#     print("[*]", " ".join(map(str, cmd)))
#     subprocess.check_call(cmd)

# def main():
#     target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SCRIPT

#     # create venv if missing
#     if not venv_python().exists():
#         run([sys.executable, "-m", "venv", str(VENV)])

#     # upgrade pip tooling
#     run([str(venv_python()), "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])

#     # editable install of simEngine
#     run([str(venv_python()), "-m", "pip", "install", "-e", str(PKG)])

#     # optional: extra deps for examples
#     req = REPO / "requirements-examples.txt"
#     if req.exists():
#         run([str(venv_python()), "-m", "pip", "install", "-r", str(req)])

#     # run target example
#     run([str(venv_python()), str(target)])

# if __name__ == "__main__":
#     main()





import os
import sys
import platform
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent
VENV = REPO / ".venvExm"
PKG_DIR = REPO.parent / "simEngine"
IS_WIN = platform.system() == "Windows"

def venv_python():
    return VENV / ("Scripts/python.exe" if IS_WIN else "bin/python")

def run(cmd):
    print("[*]", " ".join(map(str, cmd)))
    subprocess.check_call(cmd)

def write_shims(py_exe):
    if IS_WIN:
        # py.bat shim -> uses venv python
        (REPO / "py.bat").write_text(f'@echo off\r\n"{py_exe}" %*\r\n', encoding="utf-8")
        # pip.bat shim (handy)
        pip_exe = VENV / "Scripts" / "pip.exe"
        (REPO / "pip.bat").write_text(f'@echo off\r\n"{pip_exe}" %*\r\n', encoding="utf-8")
    ## LINUX / MAC systems
    else:
        py_sh = REPO / "py"
        pip_sh = REPO / "pip"
        py_sh.write_text(f'#!/usr/bin/env bash\n"{py_exe}" "$@"\n', encoding="utf-8")
        pip_exe = VENV / "bin" / "pip"
        pip_sh.write_text(f'#!/usr/bin/env bash\n"{pip_exe}" "$@"\n', encoding="utf-8")
        os.chmod(py_sh, 0o755)
        os.chmod(pip_sh, 0o755)

def main():
    # 1) create venv if needed
    if not venv_python().exists():
        run([sys.executable, "-m", "venv", str(VENV)])

    # 2) upgrade tooling
    run([str(venv_python()), "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])

    # 3) editable-install simEngine
    run([str(venv_python()), "-m", "pip", "install", "-e", str(PKG_DIR)])

    # 4) optional extras for examples
    req = REPO / "requirements-examples.txt"
    if req.exists():
        run([str(venv_python()), "-m", "pip", "install", "-r", str(req)])

    # 5) write shims so `py ...` uses the venv
    write_shims(venv_python())

    print("\n✅ Environment ready.")
    if IS_WIN:
        print("Next, run your script with the local shim:")
        print("  py examples\\Game1.py")
        print("or:")
        print("  py examples\\desktopApp.py")
    else:
        print("Next, run your script with the local shim:")
        print("  ./py examples/Game1.py")
        print("or:")
        print("  ./py examples/desktopApp.py")

if __name__ == "__main__":
    main()
