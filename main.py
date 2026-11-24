from pathlib import Path
from shutil import copyfile


if __name__ == "__main__":
    source = Path(__file__).with_name("asset.png")
    output = Path("/output/entry.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    copyfile(source, output)
