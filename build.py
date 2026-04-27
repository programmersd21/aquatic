import os
import sys
import zipfile
import shutil
from pathlib import Path

PACK_NAME = "aquatic"
OUTPUT_NAME = f"{PACK_NAME}.zip"

ROOT = Path(".")
BUILD_DIR = ROOT / "build"
ZIP_PATH = BUILD_DIR / OUTPUT_NAME

REQUIRED = ["assets", "pack.mcmeta", "pack.png"]

def get_mc_resourcepacks_path():
    home = Path.home()

    if sys.platform.startswith("win"):
        return Path(os.getenv("APPDATA")) / ".minecraft" / "resourcepacks"
    elif sys.platform == "darwin":
        return home / "Library" / "Application Support" / "minecraft" / "resourcepacks"
    else:
        return home / ".minecraft" / "resourcepacks"

def validate():
    for item in REQUIRED:
        if not (ROOT / item).exists():
            raise FileNotFoundError(f"Missing required: {item}")

def build_zip():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for path in REQUIRED:
            full = ROOT / path
            if full.is_file():
                z.write(full, arcname=full.name)
            else:
                for file in full.rglob("*"):
                    if file.is_file():
                        z.write(file, arcname=file.relative_to(ROOT))

def install():
    dest = get_mc_resourcepacks_path()
    dest.mkdir(parents=True, exist_ok=True)

    target = dest / OUTPUT_NAME
    shutil.copy2(ZIP_PATH, target)

    print(f"Installed to: {target}")

def main():
    validate()
    build_zip()
    install()
    print("Build + install complete")

if __name__ == "__main__":
    main()
    