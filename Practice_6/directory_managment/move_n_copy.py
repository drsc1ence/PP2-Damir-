import shutil

shutil.copy("find_ext.py", "find_ext_copy.py")

shutil.move("find_ext_copy.py", "folder_big/find_ext_copy.py")