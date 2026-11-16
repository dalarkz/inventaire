import re

# Read the full seed dataset from seed_full_database.py to ensure identical data
with open("seed_full_database.py", "r", encoding="utf-8") as f:
    seed_py = f.read()

print("Loaded seed_full_database.py")

