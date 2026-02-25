import re

pattern = re.compile(r"[a-z]+_[a-z]+")
print(pattern.findall("damir_ishappy_NOT"))