import shutil

shutil.copy("write_files.txt", "write_files_copy.txt")

with open("write_files_copy.txt", "r") as file:
    text = file.read()
    print(text)