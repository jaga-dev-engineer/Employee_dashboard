"""Creates a synthetic workbook for the public demo deployment."""
import random
from pathlib import Path

import pandas as pd

random.seed(42)
first = ["Arun", "Kumar", "Priya", "Kavya", "Vivek", "Chandran", "Meena", "Divya",
         "Karthik", "Sanjay", "Anitha", "Rahul", "Deepa", "Naveen", "Lakshmi"]
last = ["S", "R", "K", "M", "P", "V", "N", "G"]
locations = ["Chennai", "Bangalore", "Mumbai", "Hyderabad"]
skills = ["Python, SQL", "Java, Spring", "Azure, Databricks", "AWS, PySpark"]
clients = ["Client A", "Client B", "Client C"]

rows = []
for i in range(1, 61):
    rows.append({
        "#": i,
        "Employee ID": f"E{i:03d}",
        "Employee Name": f"{random.choice(first)} {random.choice(last)}",
        "Technical Skills": random.choice(skills),
        "YOE": str(random.randint(1, 12)),
        "Email": f"employee{i}@example.com",
        "DOJ DEP": f"20{random.randint(16, 24)}-01-01",
        "Internal/External": random.choice(["Internal", "External"]),
        "Mapped to Project": random.choice(["Project A", "Project B", ""]),
        "Billable from": "2024-01-01",
        "Client Name": random.choice(clients),
        "Certification Name": random.choice(["", "Cloud Practitioner", "Data Engineer"]),
        "Date of Completion": "",
        "Expected Date of Completion": "",
        "Profiles Uploaded": random.choice(["Yes", "No"]),
        "Contact Number": f"{9000000000 + i}",
    })

Path("data").mkdir(exist_ok=True)
pd.DataFrame(rows).to_excel(
    "data/employees.xlsx", sheet_name="Data Practice Resources", index=False
)
print("Created data/employees.xlsx with", len(rows), "rows")
