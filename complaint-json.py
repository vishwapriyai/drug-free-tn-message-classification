import pandas as pd
import json

# 📌 Load Excel file
file_path = r"D:\Drug free TN\dashboard\complaint-address.xlsx"  # update your path

df = pd.read_excel(file_path)

# ✅ Rename columns if needed
# Example:
# df.columns = ["complaint", "address"]

# 📌 Convert to required JSON format
data = {
    "complaints": []
}

for _, row in df.iterrows():
    complaint_obj = {
        "complaint": str(row["complaint"]),
        "address": str(row["address"])
    }
    data["complaints"].append(complaint_obj)

# 📌 Save to JSON file
with open("complaints.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ JSON file created successfully!")