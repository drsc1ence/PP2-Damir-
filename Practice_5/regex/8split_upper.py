import re

text = "MyNameIsDamir"

words = re.findall(r'[A-Z][^A-Z]*', text)
print(words)