import asyncio,json,hashlib,os,subprocess,edge_tts
VOICE="en-IN-NeerjaNeural";RATE="-5%"
async def one(text,mp3):await edge_tts.Communicate(text,VOICE,rate=RATE).save(mp3)
def build(spec,outdir):
    os.makedirs(outdir,exist_ok=True);led=[]
    for s in spec["scenes"]:
        h=hashlib.sha256((VOICE+RATE+s["narration"]).encode()).hexdigest()[:12]
        ogg=f"{outdir}/{s['scene_id']}.ogg"
        if not os.path.exists(ogg) or open(ogg+".hash").read()!=h:
            mp3=f"{outdir}/{s['scene_id']}.mp3";asyncio.run(one(s["narration"],mp3))
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp3,"-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","libvorbis","-ar","44100",ogg],check=True);os.remove(mp3)
            open(ogg+".hash","w").write(h);cached=False
        else:cached=True
        led.append({"scene":s["scene_id"],"chars":len(s["narration"]),"hash":h,"cached":cached})
    return led
if __name__=="__main__":
    spec=json.load(open("../specs/ch8_s82_demo.json"));print(json.dumps(build(spec,"../assets/audio"),indent=1))
