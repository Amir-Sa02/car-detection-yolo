import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
mode = sys.argv[2]
if mode == "first":
    seen = set()
    for o in d["occurrences"]:
        for n in o["nums"]:
            if n not in seen:
                seen.add(n)
                print(f"OLD {n} | P{o['i']} | {o['text']}")
elif mode == "group":
    lo, hi = map(int, sys.argv[3:5])
    for n in range(lo, hi + 1):
        print(f"\n===== REF {n} =====")
        seen = set()
        for o in d["occurrences"]:
            if n in o["nums"] and o["text"] not in seen:
                seen.add(o["text"])
                print(f"P{o['i']} {o['style']} | {o['text']}")
elif mode == "range":
    lo, hi = map(int, sys.argv[3:5])
    for x in d.get("paragraphs", []):
        if lo <= x["i"] <= hi and x["text"].strip():
            print(f"P{x['i']} [{x['style']}] {x['text']}")
