import json, os, re, shutil, sys

SDK = '../renpy-8.5.3-sdk'
OUT = '../build/bio_demo'
VID = '../assets/video'
HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
BS = chr(92)
GUISUPPORT = 'init -100 python in gui:' + NL + NL + '    def scale(n):' + NL + '        return int(n)' + NL


def esc(s):
    s = s.replace(BS, BS + BS).replace('"', BS + '"')
    return s.replace('%', '%%').replace('[', '[[').replace('{', '{{')


def gen(spec_path):
    spec = json.load(open(spec_path))
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SDK + '/gui', OUT)
    g = OUT + '/game'
    for d in ('images', 'audio', 'movies'):
        os.makedirs(g + '/' + d, exist_ok=True)

    # packaged games cannot import the launcher-only gui7 module: replace the support file with a stub
    open(g + '/guisupport.rpy', 'w').write(GUISUPPORT)
    for f in ('guisupport.rpyc', 'testcases.rpy'):
        if os.path.exists(g + '/' + f):
            os.remove(g + '/' + f)
    shutil.copy(HERE + '/templates/quiz.rpy', g + '/quiz.rpy')

    videos = {}
    for s in spec['scenes']:
        sid = s['scene_id']
        shutil.copy('../assets/' + sid + '.png', g + '/images/' + sid + '.png')
        shutil.copy('../assets/audio/' + sid + '.ogg', g + '/audio/' + sid + '.ogg')
        v = VID + '/' + sid + '.webm'
        if os.path.exists(v):
            shutil.copy(v, g + '/movies/' + sid + '.webm')
            videos[sid] = 'movies/' + sid + '.webm'
        else:
            print('WARNING: no video for ' + sid + '; falling back to static image')

    o = open(g + '/options.rpy').read()
    o = o.replace('define config.name = _("Ren' + chr(39) + 'Py 7 Default GUI")', 'define config.name = _("Cell: The Unit of Life (Demo)")')
    o = o.replace('define gui.show_name = True', 'define gui.show_name = False')
    o = re.sub(r'define build[.]name = ".*"', 'define build.name = "bio_demo"', o)
    open(g + '/options.rpy', 'w').write(o)

    quiz = {s['checkpoint']['q_id']: s['checkpoint'] for s in spec['scenes']}
    L = ['# AUTO-GENERATED from lesson_spec - do not edit by hand',
         'define narrator = Character(None, what_size=34)',
         'default persistent.completed = set()',
         'default persistent.attempts = {}',
         'default mastery = {}',
         'init python:',
         '    QUIZ = ' + repr(quiz),
         '    def record(qid, ok):',
         '        persistent.attempts[qid] = persistent.attempts.get(qid, 0) + 1',
         '        if ok:',
         '            persistent.completed.add(qid)',
         '            mastery[qid] = True']
    for sid, mv in videos.items():
        L.append('image ' + sid + '_video = Movie(size=(1920, 1080), play="' + mv + '", loop=True)')
    L += ['label start:', '    scene black', '    window auto',
          '    narrator "Welcome. This demo covers cell theory and prokaryotic vs eukaryotic cells."']
    for s in spec['scenes']:
        sid = s['scene_id']
        img = sid + '_video' if sid in videos else sid
        L += ['    # ' + sid + ': ' + s['objective'],
              '    scene black',
              '    show ' + img,
              '    voice "audio/' + sid + '.ogg"',
              '    narrator "' + esc(s['narration']) + '"',
              '    call run_quiz("' + s['checkpoint']['q_id'] + '")']
    L += ['    scene black',
          '    $ n = len(persistent.completed)',
          '    $ a = sum(persistent.attempts.values())',
          '    narrator "Section complete. Checkpoints passed: [n] of ' + str(len(spec['scenes'])) + '. Total attempts: [a]."',
          '    return']
    open(g + '/script.rpy', 'w').write(NL.join(L) + NL)
    print('generated: ' + str(len(videos)) + '/' + str(len(spec['scenes'])) + ' scenes use video')


if __name__ == '__main__':
    gen(sys.argv[1])
