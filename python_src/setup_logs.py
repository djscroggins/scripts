from pathlib import Path
from os import mkdir

log_dir = Path(__file__).resolve().parent.joinpath("logs")
if not log_dir.exists():
    mkdir(log_dir)
