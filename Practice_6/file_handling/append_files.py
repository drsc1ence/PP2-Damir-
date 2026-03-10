with open("write_files.txt", "w") as file:
    text = "smth was good"
    file.write(text)

with open("write_files.txt", "a") as file:
    texts = ["\n but it was bad", "\n idk what to say"]
    file.writelines(texts)
    
with open("write_files.txt", "r") as file:
    text = file.read()
print(text)
