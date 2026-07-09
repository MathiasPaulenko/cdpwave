import json

d = json.load(open("_all_test_results.json"))
fails = [r for r in d if r["status"] in ("FAIL", "ERROR")]
with open("_fails_list.txt", "w", encoding="utf-8") as f:
    for r in fails:
        detail = r["detail"][:200].replace("\n", " ")
        f.write(f"{r['tc']}|{r['name']}|{detail}\n")
print(f"Wrote {len(fails)} failures to _fails_list.txt")
