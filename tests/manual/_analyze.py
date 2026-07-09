import json
from collections import Counter

data = json.load(open("D:/Codigo/cdpwave/tests/manual/_all_test_results.json"))
c = Counter(r["status"] for r in data)
print("TOTAL:", len(data))
for k, v in sorted(c.items()):
    print(f"  {k}: {v}")

fails = [r for r in data if r["status"] == "FAIL"]
errors = [r for r in data if r["status"] == "ERROR"]

print(f"\nFAILS: {len(fails)}")
not_found = [r for r in fails if "wasn't found" in r.get("detail", "")]
invalid_params = [r for r in fails if "Invalid parameters" in r.get("detail", "")]
other = [r for r in fails if "wasn't found" not in r.get("detail", "") and "Invalid parameters" not in r.get("detail", "")]

print(f"  wasn't found: {len(not_found)}")
print(f"  Invalid parameters: {len(invalid_params)}")
print(f"  Other: {len(other)}")

print("\n--- Invalid parameters ---")
for r in invalid_params:
    print(f"  {r['tc']}: {r['name']} -> {r['detail'][:120]}")

print("\n--- Other FAILs ---")
for r in other:
    print(f"  {r['tc']}: {r['name']} -> {r['detail'][:120]}")

print(f"\nERRORS: {len(errors)}")
for r in errors:
    print(f"  {r['tc']}: {r['name']} -> {r['detail'][:120]}")
