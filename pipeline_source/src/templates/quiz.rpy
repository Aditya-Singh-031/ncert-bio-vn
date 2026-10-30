screen quiz(q, locked=None, picked=None):
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
            textbutton "Continue" action Return(True) text_size 38

label run_quiz(qid):
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
    return
