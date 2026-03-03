import json
import re

with open("raw.txt", 'r', encoding='utf-8') as file:
    text = file.read()

receipt_dict = {}
items = []

# Extract basic receipt information
payment_method = re.search(r'(Банковская карта|Наличные)', text)
receipt_dict["Payment Method"] = payment_method.group() if payment_method else "Unknown"

date = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})', text)
receipt_dict["Date"] = date.group(1) if date else "Unknown"

time = re.search(r'Время:\s*\d{2}\.\d{2}\.\d{4}\s+(\d{2}:\d{2}:\d{2})', text)
receipt_dict["Time"] = time.group(1) if time else "Unknown"

# Extract pharmacy/company information
company = re.search(r'Филиал (.+?)\n', text)
receipt_dict["Company"] = company.group(1).strip() if company else "Unknown"

bin_number = re.search(r'БИН (\d+)', text)
receipt_dict["BIN"] = bin_number.group(1) if bin_number else "Unknown"

# Extract items using regex pattern
# Pattern matches: item number, name, quantity, price, and total
item_pattern = r'(\d+)\.\s*\n(.*?)\n(\d[\d\s]*,\d{3})\s*x\s*(\d[\d\s]*,\d{2})\s*\n(\d[\d\s]*,\d{2})'
item_matches = re.findall(item_pattern, text)

for match in item_matches:
    item_num, item_name, quantity, price, total = match
    
    # Clean up the item name (remove extra spaces and newlines)
    item_name = re.sub(r'\s+', ' ', item_name).strip()
    
    # Convert string numbers to float (replace comma with dot)
    quantity_float = float(quantity.replace(',', '.').replace(' ', ''))
    price_float = float(price.replace(',', '.').replace(' ', ''))
    total_float = float(total.replace(',', '.').replace(' ', ''))
    
    item = {
        "Item Number": int(item_num),
        "Name": item_name,
        "Quantity": quantity_float,
        "Unit Price": price_float,
        "Total": total_float
    }
    items.append(item)

receipt_dict["Items"] = items

# Extract total amount
total_amount = re.search(r'ИТОГО:\s*\n(\d[\d\s]*,\d{2})', text)
receipt_dict["Total Amount"] = float(total_amount.group(1).replace(',', '.').replace(' ', '')) if total_amount else 0.0

#Convert to JSON for pretty printing
receipt_json = json.dumps(receipt_dict, ensure_ascii=False, indent=2)

# Print results
print("\n" + "="*50)
print("EXTRACTED RECEIPT INFORMATION")
print("="*50)
print(f"Time: {receipt_dict['Time']}")
print(f"Date: {receipt_dict['Date']}")
print(f"Company: {receipt_dict['Company']}")
print(f"Total Amount: {receipt_dict['Total Amount']} KZT")
print(f"Payment Method: {receipt_dict['Payment Method']}")
print("\n items:")
for item in items:  # Show first all items
    print(f"  {item["Item Number"]}. {item['Name'][:30]}... - {item['Quantity']} x {item['Unit Price']} = {item['Total']}")

print("\n" + "="*50)
print("FULL JSON OUTPUT:")
print("="*50)
print(receipt_json)

# Optionally save to a file
with open("receipt_output.json", 'w', encoding='utf-8') as f:
    f.write(receipt_json)