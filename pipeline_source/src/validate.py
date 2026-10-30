import json,sys
from jsonschema import Draft202012Validator
from schema import LESSON_SCHEMA
def validate(spec_path,spans_path):
    spec=json.load(open(spec_path));sp={s["id"]:s for s in json.load(open(spans_path))["spans"]}
    errs=[f"schema: {'/'.join(map(str,e.path))}: {e.message}" for e in Draft202012Validator(LESSON_SCHEMA).iter_errors(spec)]
    seen=set()
    for s in spec.get("scenes",[]):
        sid=s.get("scene_id","?")
        if sid in seen:errs.append(f"{sid}: duplicate scene id")
        seen.add(sid)
        for c in s.get("claims",[]):
            for i in c["span_ids"]:
                if i not in sp:errs.append(f"{sid}: unknown span {i}")
        for i in s["checkpoint"]["span_ids"]:
            if i not in sp:errs.append(f"{sid}: MCQ unknown span {i}")
        o=s["checkpoint"]["options"]
        if len(set(x.strip().lower() for x in o))!=4:errs.append(f"{sid}: duplicate MCQ options")
        ex=s["checkpoint"]["explanations"];a=s["checkpoint"]["answer"]
        if not ex[a].startswith("Correct"):errs.append(f"{sid}: keyed explanation must start with 'Correct'")
        if sum(e.startswith("Correct") for e in ex)!=1:errs.append(f"{sid}: exactly one correct explanation required")
        if s["visual"]["render_tier"]!="A_deterministic" and not s["visual"].get("approved_reference"):errs.append(f"{sid}: generative tier needs approved reference")
    return errs
if __name__=="__main__":
    e=validate(sys.argv[1],sys.argv[2]);print("\n".join(e) if e else "VALID");sys.exit(1 if e else 0)
