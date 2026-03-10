import os

file_name = "write_files_copy.txt"

if os.path.exists(file_name):
    os.remove(file_name)
else:
    print("File does not exists")