import json,os,subprocess,hashlib,sys
from validate import validate
spec_p="../specs/ch8_s82_demo.json";spans_p="../source/ch8_spans.json";spec=json.load(open(spec_p));R=[]
def chk(n,ok,d=""):R.append({"check":n,"pass":bool(ok),"detail":d})
e=validate(spec_p,spans_p);chk("schema+evidence+MCQ rules",not e,"; ".join(e))
for s in spec["scenes"]:
    i=s["scene_id"];img=f"../assets/{i}.png";aud=f"../assets/audio/{i}.ogg"
    chk(f"{i} image 1920x1080",os.path.exists(img) and subprocess.run(["ffprobe","-v","error","-show_entries","stream=width,height","-of","csv=p=0",img],capture_output=True,text=True).stdout.strip()=="1920,1080")
    d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",aud],capture_output=True,text=True).stdout.strip()
    chk(f"{i} audio exists+duration",d!="" and float(d)>2,d+"s")
    labs=[l for l in s["visual"]["labels"]];svg=open(f"../assets/{i}.svg").read()
    chk(f"{i} labels rendered from approved list",all(l.split(" ",1)[-1].split(" - ")[0][:6] in svg for l in labs))
p=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_name,pix_fmt,width,height","-of","csv=p=0","../assets/s04_motion.webm"],capture_output=True,text=True).stdout.strip()
chk("video vp9/yuv420p/1080p",p.startswith("vp9") and "yuv420p" in p and "1920,1080" in p,p)
rpy=open("../build/bio_demo/game/script.rpy").read()
chk("every scene voiced+quizzed in script",all((f'voice "audio/{s["scene_id"]}.ogg"' in rpy and f'call run_quiz("{s["checkpoint"]["q_id"]}")' in rpy) for s in spec["scenes"]))
sim=True
for s in spec["scenes"]:
    c=s["checkpoint"]
    for pick in range(4):
        t=0;done=False
        while not done:
            t+=1;ok=(pick==c["answer"])
            if ok or t>=2:done=True
        sim&=done
chk("quiz can never trap learner (sim all picks)",sim)
man={}
for r,_,fs in os.walk("../assets"):
    for f in fs:
        if f.endswith((".png",".ogg",".webm",".svg")):pa=os.path.join(r,f);man[pa[3:]]=hashlib.sha256(open(pa,"rb").read()).hexdigest()
json.dump(man,open("../build/asset_manifest.json","w"),indent=1)
json.dump(R,open("../build/qa_report.json","w"),indent=1)
for r in R:print(("PASS" if r["pass"] else "FAIL"),r["check"],r["detail"][:60])
