from pathlib import Path
import os
import logging

files = [
    "src/helper.py",
    "src/__init__.py",
    "src/prompt.py",
    "requirements.txt",
    "research/snippets.ipynb",
    "app.py",
    ".env",
    "setup.py"
]

logging.basicConfig(level=logging.INFO, format='[%(asctime)s: %(message)s]')

for filepath in files:
    filepath = Path(filepath)
    dir, file =  os.path.split(filepath)

    if dir != "":
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
            logging.info(f"Directory Created: {dir}")
        else:
            logging.info(f"Directory Already Exists {dir}")

    if not filepath.exists():
        with open(filepath, "w") as f:
            pass
        logging.info(f"File Created: {filepath}")
    
    elif os.path.getsize(str(filepath)) == 0:
        logging.info(f"File Exists But Empty: {filepath}")
    
    else:
        logging.info(f"File Path Already exist: {filepath}")