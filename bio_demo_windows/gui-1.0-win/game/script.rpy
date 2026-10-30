# AUTO-GENERATED from lesson_spec - do not edit by hand
define narrator = Character(None, what_size=34)
default persistent.completed = set()
default persistent.attempts = {}
default mastery = {}
init python:
    QUIZ = {'s01': {'q_id': 'q01', 'stem': 'Which statement best describes a cell?', 'options': ['A tissue made of many organs', 'The fundamental structural and functional unit of living organisms', 'A structure found only in animals', 'The largest part of a plant'], 'answer': 1, 'explanations': ['Incorrect: tissues are made of cells, not the reverse.', 'Correct: the cell is the basic structural and functional unit of life.', 'Incorrect: plants, fungi and bacteria also have cells.', 'Incorrect: cells are the basic unit, not a plant part.'], 'span_ids': ['sp_087_01'], 'remediation': 'Revisit: all organisms are composed of cells.'}, 's02': {'q_id': 'q02', 'stem': 'Who explained that new cells are formed from pre-existing cells?', 'options': ['Schleiden', 'Schwann', 'Virchow', 'Robert Brown'], 'answer': 2, 'explanations': ['Incorrect: Schleiden studied plant cells.', 'Incorrect: Schwann studied animal cells.', 'Correct: Virchow (1855) explained cell division gives new cells.', 'Incorrect: Robert Brown discovered the nucleus.'], 'span_ids': ['sp_088_03'], 'remediation': 'Revisit the timeline: 1838, 1839, 1855.'}, 's03': {'q_id': 'q03', 'stem': 'Which is NOT part of cell theory as understood today?', 'options': ['All organisms are composed of cells and products of cells', 'All cells arise from pre-existing cells', 'Cells form de novo from non-living matter', 'Cells are the unit of living organisms'], 'answer': 2, 'explanations': ['Part of the theory.', 'Part of the theory.', 'Correct: cells arise from pre-existing cells, not from abiotic matter.', 'Consistent with the theory.'], 'span_ids': ['sp_088_04', 'sp_088_05'], 'remediation': 'Revisit the two points of cell theory.'}, 's04': {'q_id': 'q04', 'stem': 'A cell has no membrane bound nucleus. It is most likely:', 'options': ['Eukaryotic', 'Prokaryotic', 'A plant cell', 'An animal cell'], 'answer': 1, 'explanations': ['Incorrect: eukaryotes have a membrane bound nucleus.', 'Correct: prokaryotes lack a membrane bound nucleus.', 'Incorrect: plant cells are eukaryotic.', 'Incorrect: animal cells are eukaryotic.'], 'span_ids': ['sp_088_06'], 'remediation': 'Revisit: eukaryotic = membrane bound nucleus.'}, 's05': {'q_id': 'q05', 'stem': 'Which structure is found in BOTH prokaryotic and eukaryotic cells?', 'options': ['Mitochondria', 'Golgi complex', 'Ribosomes', 'Endoplasmic reticulum'], 'answer': 2, 'explanations': ['Incorrect: mitochondria are membrane bound organelles of eukaryotes.', 'Incorrect: Golgi is a membrane bound organelle.', 'Correct: ribosomes occur in all cells.', 'Incorrect: ER is a membrane bound organelle.'], 'span_ids': ['sp_088_08', 'sp_088_07'], 'remediation': 'Revisit the organelle comparison.'}, 's06': {'q_id': 'q06', 'stem': 'Which is present in plant cells but absent in animal cells?', 'options': ['Plasma membrane', 'Ribosomes', 'Nucleus', 'Cell wall'], 'answer': 3, 'explanations': ['Incorrect: both have a plasma membrane.', 'Incorrect: both have ribosomes.', 'Incorrect: both are eukaryotic with a nucleus.', 'Correct: cell wall, plastids and a large central vacuole are plant features.'], 'span_ids': ['sp_091_02'], 'remediation': 'Revisit plant vs animal differences.'}}
    def record(qid, ok):
        persistent.attempts[qid] = persistent.attempts.get(qid, 0) + 1
        if ok:
            persistent.completed.add(qid)
            mastery[qid] = True
image s04_motion = Movie(size=(1920, 1080), play="movies/s04_motion.webm", loop=True)
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
    $ q = next(item for item in QUIZ.values() if item["q_id"] == qid)
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
label start:
    scene black
    window auto
    narrator "Welcome. This demo covers cell theory and prokaryotic vs eukaryotic cells."
    # s01: State what a cell is.
    scene black
    show s01
    voice "audio/s01.ogg"
    narrator "Every living thing is built from cells. The cell is the fundamental structural and functional unit of all living organisms."
    call run_quiz("q01")
    # s02: Trace the development of cell theory.
    scene black
    show s02
    voice "audio/s02.ogg"
    narrator "In 1838 Schleiden found that plants are made of cells. In 1839 Schwann studied animal cells. In 1855 Virchow explained that new cells form from pre-existing cells."
    call run_quiz("q02")
    # s03: Know the two points of modern cell theory.
    scene black
    show s03
    voice "audio/s03.ogg"
    narrator "Cell theory as understood today has two points. All living organisms are composed of cells and products of cells. And all cells arise from pre-existing cells."
    call run_quiz("q03")
    # s04: Distinguish prokaryotic and eukaryotic cells by the nucleus.
    scene black
    show s04_motion
    voice "audio/s04.ogg"
    narrator "Cells with a membrane bound nucleus are eukaryotic. Cells that lack one are prokaryotic, where the genetic material is naked and not enveloped by a nuclear membrane."
    call run_quiz("q04")
    # s05: Recall organelle differences and what both cell types share.
    scene black
    show s05
    voice "audio/s05.ogg"
    narrator "Eukaryotic cells have membrane bound organelles that compartmentalise the cytoplasm. Prokaryotic cells lack them. Ribosomes are found in all cells, and are not membrane bound."
    call run_quiz("q05")
    # s06: Differentiate plant and animal cells.
    scene black
    show s06
    voice "audio/s06.ogg"
    narrator "Plant and animal cells differ. Plant cells possess cell walls, plastids and a large central vacuole, which are absent in animal cells."
    call run_quiz("q06")
    scene black
    $ n = len(persistent.completed)
    $ a = sum(persistent.attempts.values())
    narrator "Section complete. Checkpoints passed: [n] of 6. Total attempts: [a]."
    return
