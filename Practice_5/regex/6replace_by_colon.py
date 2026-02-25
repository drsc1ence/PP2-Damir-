import re

text = "Hello My name, is. Smth, but you can call me Idk"
replacedText = re.sub(r'[ ,.]', ':', text)
print(replacedText)