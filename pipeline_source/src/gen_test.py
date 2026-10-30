import json,sys
spec=json.load(open(sys.argv[1]));out=sys.argv[2]
L=["testcase traverse:","    advance until screen quiz"]
for k,s in enumerate(spec["scenes"]):
    c=s["checkpoint"];ok=c["options"][c["answer"]];wrong=c["options"][(c["answer"]+1)%4]
    if k==0:L+=[f'    click "{wrong}"',"    advance until screen feedback","    click \"Continue\""]
    L+=[f'    click "{ok}"',"    advance until screen feedback","    click \"Continue\""]
    L.append("    advance until screen quiz" if k<len(spec["scenes"])-1 else "    advance")
L+=["    pause 1.0","    $ renpy.quit()" if False else "    pause 0.5"]
open(out,"w").write("\n".join(L)+"\n")
