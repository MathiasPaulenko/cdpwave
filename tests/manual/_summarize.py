import json
from collections import Counter

d = json.load(open("_all_test_results.json"))
c = Counter(r["status"] for r in d)
print(f"TOTAL: {len(d)}")
for k, v in sorted(c.items()):
    print(f"  {k}: {v}")

fails = [r for r in d if r["status"] in ("FAIL", "ERROR")]
print(f"\nFAILED/ERROR: {len(fails)}")
for r in fails:
    detail = r["detail"][:150].replace("\n", " ")
    print(f"  {r['tc']}: {r['name']} -> {detail}")
