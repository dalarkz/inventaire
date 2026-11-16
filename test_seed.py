import json

with open("seed_full_database.py", "r", encoding="utf-8") as f:
    py_code = f.read()

print("Seed file loaded, length:", len(py_code))

