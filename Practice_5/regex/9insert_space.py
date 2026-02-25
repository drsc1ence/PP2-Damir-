import re

text = "HelloMyNameIsDamirAndIamAStudentOfKbtu"
words = re.findall(r'[A-Z][^A-Z]*', text)
spaced = ' '.join(words)
print(spaced)