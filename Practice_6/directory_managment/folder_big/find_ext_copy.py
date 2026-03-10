from pathlib import Path

files = Path(".").glob("*.py")
for file in files:
    print(file.name)