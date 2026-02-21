import json

# Open the file in read mode ('r') using a 'with' statement for automatic closing
with open("sample-data.json", 'r') as file:
    # Use json.load() to deserialize the file content into a Python object
    data = json.load(file)

# You can now work with the data (e.g., print it)
print("Interface Status")
print("=" * 87)
print("DN                                                 Description           Speed    MTU ")
print("-------------------------------------------------- --------------------  ------  ------")

for i in data["imdata"]:
    attr = i["l1PhysIf"]["attributes"]
    dn = attr["dn"]
    desc = attr["descr"]
    mtu = attr["mtu"]
    speed = attr["speed"]
    print(f"{dn:50}{desc:23}{speed:10}{mtu}")