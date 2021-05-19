from browser import document, console, alert, html, timer
from random import randint, choice
from music import *
from copy import copy

def difficulty():
    if document.body.classList.contains('easy'):
        return 'easy'
    else:
        return 'hard'
PARAMETERS = {
    "triads": {
        "type":'',
        "quality":'',
        "n":'',
        "note_list":[],
    },
    "progressions": {
        "full_progression":[],
        "unguessed":[],
    },
    "intervals": {
        "sim": False,
        "interval": ''
    },
}

def update_settings(e):
    game = e.target.id.split('_')[0]

    try:

        if document[game+'_easy'].checked:
            document.body.classList.add('easy')
        else:
            document.body.classList.remove('easy')

    except KeyError:
        pass

    if e.target.name == 'degrees':
        for dom in document.querySelectorAll('#pr_available_degrees input:checked'):
            document['pr_'+dom.id].style.display = 'block'
        for dom in document.querySelectorAll('#pr_available_degrees input:not(:checked)'):
            document['pr_'+dom.id].style.display = 'none'

    elif e.target.name == 'ints':
        for dom in document.querySelectorAll('#available_intervals input:checked'):
            document['in_'+dom.id].style.display = 'inline'
        for dom in document.querySelectorAll('#available_intervals input:not(:checked)'):
            document['in_'+dom.id].style.display = 'none'

    PARAMETERS["intervals"]["sim"] = document['in_sim'].checked

for dom in document.querySelectorAll(".settings input"):
        dom.bind('change', update_settings)
document.bind('load', update_settings)
def reveal_answer(e):
    document.body.classList.add('revealed')
for dom in document.querySelectorAll(".answer"):
        dom.bind('click', reveal_answer)

def play_chord(l):
    console.log(l)
    for i,note in enumerate(l):
        x = document[str(i)]
        adress = "notes/" + str(note[0]) + '/' +str(note) +'.ogg'
        x.src = adress
        x.play()

def arpegiate(l):
    ll = copy(l)
    console.log(l)
    def aux():
        if ll == []:
            return None
        else:
            i = len(ll)
            n = ll.pop(0)
            x = document[str(i)]
            adress = "notes/" + n[0] + '/' +n +'.ogg'
            x.src = adress
            x.play()
            timer.set_timeout(aux, 300)
    aux()

def play_progression(p):
    pp = copy(p)
    console.log(p)
    def aux():
        if pp == []:
            return None
        else:
            i = len(pp)
            chord = pp.pop(0)[0]
            play_chord(chord)
            timer.set_timeout(aux, 1000)
    aux()

def arpegiate_progression(p):
    pp = copy(p)
    console.log(p)
    def aux():
        if pp == []:
            return None
        else:
            i = len(pp)
            chord = pp.pop(0)[0]
            arpegiate(chord)
            timer.set_timeout(aux, len(chord)*400)
    aux()
#-------------triads----------------------------

def tr_play(e):
    global PARAMETERS
    document.body.classList.remove('revealed')
    document['triads'].classList.remove('show_inversions')
    diff = difficulty()
    document['tr_inversion_result'].textContent = ''
    document['tr_quality_result'].textContent = ''
    root = choice(notes)
    n = randint(0, 2)
    if diff == 'easy':
        structure = choice(chords["basic triads"])
    if diff =='hard':
        structure = choice(chords["basic triads"]+chords["advanced triads"])
    note_list, PARAMETERS["triads"]["quality"], PARAMETERS["triads"]["type"],  _, name = construct_chord(root, structure, n)
    console.log(root)
    console.log(n)
    console.log(structure)
    play_chord(note_list)
    PARAMETERS["triads"]["n"] = n
    PARAMETERS["triads"]["note_list"] = note_list
    document['tr_name'].textContent = name
document['tr_play'].bind('click', tr_play)

def tr_replay(e):
    play_chord(PARAMETERS["triads"]["note_list"])
document['tr_replay'].bind('click', tr_replay)

def tr_slow(e):
    arpegiate(PARAMETERS["triads"]["note_list"])
document['tr_slow'].bind('click', tr_slow)

def tr_test_quality(e):
    if PARAMETERS["triads"]["quality"] == e.target.id[3:]:
        document['tr_quality_result'].textContent = 'YES !'
        if not(need_to_change_root[PARAMETERS["triads"]["type"]]):
            document['triads'].classList.add('show_inversions')
    else:
        document['tr_quality_result'].textContent = 'NO'
for dom in document.querySelectorAll("#tr_quality button"):
    dom.bind('click', tr_test_quality)

def tr_test_inversion(e):
    if str(PARAMETERS["triads"]["n"]) == e.target.id[3:]:
        document['tr_inversion_result'].textContent = 'YES !'
    else:
        document['tr_inversion_result'].textContent = 'NO'
for dom in document.querySelectorAll("#tr_inversion button"):
    dom.bind('click', tr_test_inversion)

#-------------progressions----------------------------

def pr_play(e):
    global PARAMETERS
    document.body.classList.remove('revealed')
    diff = difficulty()
    document['pr_result'].textContent = ''
    document['pr_so_far'].textContent = ''
    document['pr_name'].textContent = ''
    key = choice(notes)
    choices_degree = []
    for dom in document.querySelectorAll('#pr_available_degrees input:checked'):
        choices_degree += degrees[dom.id]
    progression = [construct_chord(key, '0:4:7:I', randint(0,2))]
    for _ in range(4):
        structure = choice(choices_degree)
        n =  choice([i for i in range(len(structure.split(':'))-1)])
        progression.append(construct_chord(key, structure, n))
    play_progression(progression)
    PARAMETERS["progressions"]["full_progression"] = progression
    PARAMETERS["progressions"]["unguessed"] = copy(progression)
    for chord in progression:
        document['pr_name'].textContent += ' / '+chord[1]
document['pr_play'].bind('click', pr_play)

def pr_replay(e):
    play_progression(PARAMETERS["progressions"]["full_progression"])
document['pr_replay'].bind('click', pr_replay)

def pr_slow(e):
    arpegiate_progression(PARAMETERS["progressions"]["full_progression"])
document['pr_slow'].bind('click', pr_slow)

def pr_test(e):
    global PARAMETERS
    goal = e.target.id[3:]
    if PARAMETERS["progressions"]["unguessed"][0][1] == goal:
        document['pr_result'].textContent = 'YES !'
        document['pr_so_far'].textContent += ' / '+goal
        PARAMETERS["progressions"]["unguessed"].pop(0)
    else:
        document['pr_result'].textContent = 'NO'
for dom in document.querySelectorAll("#pr_degree button"):
    dom.bind('click', pr_test)

#-------------intervals----------------------------
def in_play(e):
    global PARAMETERS
    document.body.classList.remove('revealed')
    diff = difficulty()
    document['in_result'].textContent = ''
    root = choice(notes)
    choices_interval = [dom.id for dom in document.querySelectorAll('#available_intervals input:checked')]
    console.log(choices_interval)
    interval= ''
    while not(interval in choices_interval):
        note_list, interval, _, _, _ = construct_chord(root, choice(intervals), 0)
    PARAMETERS['intervals']['interval'] = interval
    PARAMETERS['intervals']['note list'] = note_list
    if PARAMETERS['intervals']['sim']:
        play_chord(note_list)
    else:
        arpegiate(note_list)
    document['in_name'].textContent = interval
    
document['in_play'].bind('click', in_play)

def in_replay(e):
    note_list = PARAMETERS['intervals']['note list']
    if PARAMETERS['intervals']['sim']:
        play_chord(note_list)
    else:
        arpegiate(note_list)
document['in_replay'].bind('click', in_replay)

def in_sim(e):
    PARAMETERS['intervals']['sim'] = not(PARAMETERS['intervals']['sim'])
document['in_sim'].bind('change', in_sim)

def in_test(e):
    global PARAMETERS
    goal = e.target.id[3:]
    if PARAMETERS["intervals"]["interval"] == goal:
        document['in_result'].textContent = 'YES !'
    else:
        document['in_result'].textContent = 'NO'
for dom in document.querySelectorAll("#in button"):
    dom.bind('click', in_test)
