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
company = re.search(r'Филиал ТОО (.+?)\n', text)
receipt_dict["Company"] = company.group(1).strip() if company else "Unknown"

bin_number = re.search(r'БИН (\d+)', text)
receipt_dict["BIN"] = bin_number.group(1) if bin_number else "Unknown"

vat_series = re.search(r'НДС Серия (\d+)', text)
receipt_dict["VAT Series"] = vat_series.group(1) if vat_series else "Unknown"

receipt_number = re.search(r'№ (\d+)', text)
receipt_dict["Receipt Number"] = receipt_number.group(1) if receipt_number else "Unknown"

cash_reg = re.search(r'Касса (\d+-\d+)', text)
receipt_dict["Cash Register"] = cash_reg.group(1) if cash_reg else "Unknown"

shift = re.search(r'Смена (\d+)', text)
receipt_dict["Shift"] = shift.group(1) if shift else "Unknown"

check_number = re.search(r'Чек №(\d+)', text)
receipt_dict["Check Number"] = check_number.group(1) if check_number else "Unknown"

cashier = re.search(r'Кассир (.+?)(?:\n|$)', text)
receipt_dict["Cashier"] = cashier.group(1).strip() if cashier else "Unknown"

# Extract items using regex pattern
# Pattern matches: item number, name, quantity, price, and total
item_pattern = r'(\d+)\.\s*\n(.*?)\n(\d+,\d{3})\s*x\s*(\d+,\d{2})\s*\n(\d+,\d{2})'
item_matches = re.findall(item_pattern, text, re.DOTALL)

for match in item_matches:
    item_num, item_name, quantity, price, total = match
    
    # Clean up the item name (remove extra spaces and newlines)
    item_name = re.sub(r'\s+', ' ', item_name).strip()
    
    # Convert string numbers to float (replace comma with dot)
    quantity_float = float(quantity.replace(',', '.'))
    price_float = float(price.replace(',', '.'))
    total_float = float(total.replace(',', '.'))
    
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
total_amount = re.search(r'ИТОГО:\s*(\d+,\d{2})', text)
receipt_dict["Total Amount"] = float(total_amount.group(1).replace(',', '.')) if total_amount else 0.0

# Extract VAT (if any)
vat = re.search(r'в т\.ч\. НДС 12%:\s*(\d+,\d{2})', text)
receipt_dict["VAT 12%"] = float(vat.group(1).replace(',', '.')) if vat else 0.0

# Extract fiscal information
fiscal_sign = re.search(r'Фискальный признак:\s*(\d+)', text)
receipt_dict["Fiscal Sign"] = fiscal_sign.group(1) if fiscal_sign else "Unknown"

# Extract location
location = re.search(r'г\.\s*(.+?),\s*Казахстан,\s*(.+?),\s*(\d+),\s*нп-\d+', text)
if location:
    receipt_dict["Location"] = {
        "City": location.group(1).strip(),
        "Street": location.group(2).strip(),
        "Building": location.group(3).strip()
    }

# Extract fiscal data operator
fdo = re.search(r'Оператор фискальных данных:\s*(.+?)(?:\n|$)', text)
receipt_dict["Fiscal Data Operator"] = fdo.group(1).strip() if fdo else "Unknown"

# Extract verification info
verification_site = re.search(r'Для проверки чека зайдите на сайт:\s*(\S+)', text)
receipt_dict["Verification Site"] = verification_site.group(1) if verification_site else "Unknown"

# Extract fiscal registration numbers
fiscal_number = re.search(r'ФП\s*\nИНК ОФД:\s*(\d+)', text)
receipt_dict["INK OFD"] = fiscal_number.group(1) if fiscal_number else "Unknown"

rnm = re.search(r'Код ККМ КГД \(РНМ\):\s*(\d+)', text)
receipt_dict["RNM Code"] = rnm.group(1) if rnm else "Unknown"

znm = re.search(r'ЗНМ:\s*(\S+)', text)
receipt_dict["ZNM"] = znm.group(1) if znm else "Unknown"

# Calculate summary statistics
total_items = len(items)
total_quantity = sum(item["Quantity"] for item in items)
total_sum = sum(item["Total"] for item in items)

receipt_dict["Summary"] = {
    "Total Items": total_items,
    "Total Quantity": round(total_quantity, 3),
    "Calculated Sum": round(total_sum, 2),
    "Matches Total": abs(round(total_sum - receipt_dict["Total Amount"], 2)) < 0.01
}

# Convert to JSON for pretty printing
receipt_json = json.dumps(receipt_dict, ensure_ascii=False, indent=2)

# Print results
print("\n" + "="*50)
print("EXTRACTED RECEIPT INFORMATION")
print("="*50)
print(f"Time: {receipt_dict['Time']}")
print(f"Date: {receipt_dict['Date']}")
print(f"Company: {receipt_dict['Company']}")
print(f"Total Amount: {receipt_dict['Total Amount']} KZT")
print(f"Number of Items: {total_items}")
print(f"Payment Method: {receipt_dict['Payment Method']}")
print("\nFirst few items:")
for i, item in enumerate(items[:3]):  # Show first 3 items
    print(f"  {i+1}. {item['Name'][:30]}... - {item['Quantity']} x {item['Unit Price']} = {item['Total']}")

print("\n" + "="*50)
print("FULL JSON OUTPUT:")
print("="*50)
print(receipt_json)

# Optionally save to a file
with open("receipt_output.json", 'w', encoding='utf-8') as f:
    f.write(receipt_json)
print("\n✅ Receipt data saved to 'receipt_output.json'")