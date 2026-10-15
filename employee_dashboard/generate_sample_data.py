"""Creates data/employees.xlsx with sample rows; the dashboard uses Employee_data.xlsx."""
import random
from pathlib import Path

import pandas as pd

random.seed(42)
first = ["Arun", "Kumar", "Priya", "Kavya", "Vivek", "Chandran", "Meena", "Divya",
         "Karthik", "Sanjay", "Anitha", "Rahul", "Deepa", "Naveen", "Lakshmi"]
last = ["S", "R", "K", "M", "P", "V", "N", "G"]
locations = ["Chennai", "Bangalore", "Mumbai", "Hyderabad"]

rows = []
for i in range(1, 61):
    rows.append({
        "S.no": i,
        "Employee ID": f"E{i:03d}",
        "Employee Name": f"{random.choice(first)} {random.choice(last)}",
        "Email": f"employee{i}@example.com",
        "Mapped to Project": random.choice(["Y", "N"]),
        "Location": random.choice(locations),
        "Contact Number": f"{9000000000 + i}",
    })

Path("data").mkdir(exist_ok=True)
pd.DataFrame(rows).to_excel("data/employees.xlsx", index=False)
print("Created data/employees.xlsx with", len(rows), "rows")
