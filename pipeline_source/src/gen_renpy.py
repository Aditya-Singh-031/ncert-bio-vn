import json,os,shutil,sys
SDK="../renpy-8.5.3-sdk";OUT="../build/bio_demo";MOTION={"s04":"movies/s04_motion.webm"}
def esc(s):return s.replace("\\","\\\\").replace('"','\\"').replace("%","%%").replace("[","[[").replace("{","{{")
def gen(spec_path):
    spec=json.load(open(spec_path))
    if os.path.exists(OUT):shutil.rmtree(OUT)
    shutil.copytree(f"{SDK}/gui",OUT);shutil.copy(f"{SDK}/gui/project.json",OUT) if os.path.exists(f"{SDK}/gui/project.json") else None
    g=f"{OUT}/game";os.makedirs(f"{g}/images",exist_ok=True);os.makedirs(f"{g}/audio",exist_ok=True);os.makedirs(f"{g}/movies",exist_ok=True)
    for s in spec["scenes"]:
        sid=s["scene_id"];shutil.copy(f"../assets/{sid}.png",f"{g}/images/{sid}.png");shutil.copy(f"../assets/audio/{sid}.ogg",f"{g}/audio/{sid}.ogg")
    shutil.copy("../assets/s04_motion.webm",f"{g}/movies/s04_motion.webm")
    o=open(f"{g}/options.rpy").read()
    o=o.replace('define config.name = _("Ren\'Py 7 Default GUI")','define config.name = _("Cell: The Unit of Life (Demo)")').replace('define gui.show_name = True','define gui.show_name = False')
    open(f"{g}/options.rpy","w").write(o)
    quiz = {s["checkpoint"]["q_id"]: s["checkpoint"] for s in spec["scenes"]}
    L=['# AUTO-GENERATED from lesson_spec - do not edit by hand','define narrator = Character(None, what_size=34)','default persistent.completed = set()','default persistent.attempts = {}','default mastery = {}']
    L.append("init python:\n    QUIZ = "+repr(quiz)+"\n    def record(qid, ok):\n        persistent.attempts[qid] = persistent.attempts.get(qid, 0) + 1\n        if ok:\n            persistent.completed.add(qid)\n            mastery[qid] = True")
    for sid,mv in MOTION.items():L.append(f'image {sid}_motion = Movie(size=(1920, 1080), play="{mv}", loop=True)')
    L.append('''screen quiz(q, locked=None, picked=None):
    modal True
    add Solid("#0F1B2Dd8")
    frame:
        align (0.5, 0.5)
        xsize 1500
        padding (60, 50)
        background Solid("#16263D")
        vbox:
            spacing 24
            text "Checkpoint" size 28 color "#F4B942"
            text q["stem"] size 44 color "#F2F5FA"
            for i, opt in enumerate(q["options"]):
                textbutton opt:
                    xfill True
                    text_size 36
                    sensitive (locked is None)
                    action Return(i)
                    selected (picked == i)
                    alt "Option " + str(i + 1) + ": " + opt

screen feedback(msg, ok):
    modal True
    add Solid("#0F1B2Dd8")
    frame:
        align (0.5, 0.5)
        xsize 1500
        padding (60, 50)
        background Solid("#16263D")
        vbox:
            spacing 30
            text ("Correct" if ok else "Not quite") size 52 color ("#6FCF97" if ok else "#FF6B6B")
            text msg size 38 color "#F2F5FA"
            textbutton "Continue" action Return(True) text_size 38''')
    L.append('''label run_quiz(qid):
    $ q = QUIZ[qid]
    $ tries = 0
    $ done = False
    while not done:
        $ pick = renpy.call_screen("quiz", q)
        $ tries += 1
        $ ok = (pick == q["answer"])
        $ record(qid, ok)
        if ok:
            call screen feedback(q["explanations"][pick], True)
            $ done = True
        else:
            call screen feedback(q["explanations"][pick] + "  Hint: " + q["remediation"], False)
            if tries >= 2:
                call screen feedback("Answer: " + q["options"][q["answer"]] + ". " + q["explanations"][q["answer"]], True)
                $ done = True
    return''')
    L.append('label start:\n    scene black\n    window auto\n    narrator "Welcome. This demo covers cell theory and prokaryotic vs eukaryotic cells."')
    for s in spec["scenes"]:
        sid=s["scene_id"];img=f"{sid}_motion" if sid in MOTION else sid
        L.append(f'    # {sid}: {s["objective"]}\n    scene black\n    show {img}\n    voice "audio/{sid}.ogg"\n    narrator "{esc(s["narration"])}"\n    call run_quiz("{s["checkpoint"]["q_id"]}")')
    L.append('    scene black\n    $ n = len(persistent.completed)\n    $ a = sum(persistent.attempts.values())\n    narrator "Section complete. Checkpoints passed: [n] of '+str(len(spec["scenes"]))+'. Total attempts: [a]."\n    return')
    open(f"{g}/script.rpy","w").write("\n".join(L)+"\n")
    for f in ("testcases.rpy",):
        p=f"{g}/{f}"
        if os.path.exists(p):os.remove(p)
if __name__=="__main__":gen(sys.argv[1]);print("generated")
