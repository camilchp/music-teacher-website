PITCH_START = 3


C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'
notes = [C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B]
#        0      2      4  5      7      9      11

notes_extended = [C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B]

chords = {
    "basic triads": ['0:4:7:maj', '0:3:7:min', '0:4:8:aug','0:3:6:dim'],
    "advanced triads": ['0:5:10:Q', '0:5:11:Q+', '0:6:11:+4Q'],
    "seventh chords": ['0:4:7:11:maj7', '0:3:7:10:min7', '0:4:7:10:7'],
    }

inversion_names = {
    'maj': ['maj root position', 'maj 1st inversion', 'maj 2nd inversion'],
    'min': ['min root position', 'min 1st inversion', 'min 2nd inversion'],
    'dim': ['dim', 'dim', 'dim'],
    'aug': ['aug', 'aug', 'aug'],
    'Q': ['Q', 'sus4', 'sus2'],
    'Q+': ['Q+', 'lyd', 'locr'],
    '+4Q': ['+4Q', 'sus4b5', 'phr'],
}

need_to_change_root = {
    'maj': False,
    'min': False,
    'dim': True,
    'aug': True,
    'Q': True,
    'Q+': True,
    '+4Q': True,
}

degrees = {
    "diatonic_triads": ['0:4:7:I', '2:5:9:ii', '4:7:11:iii', '5:9:0:IV', '7:11:2:V', '9:0:4:vi', '11:2:5:viidim'],
    "common_exotic_triads": ['2:6:9:II', '4:8:11:III', '5:8:0:iv'],
    "seventh_chords": ['0:4:7:11:I-maj7', '2:5:9:0:ii-min7', '4:7:11:2:iii-min7', '5:9:0:4:IV-maj7', '7:11:2:5:V7', '9:0:4:7:vi-min7', '11:2:5:9:vii-dim7'],
    }

intervals = ['0:1:m2', '0:2:M2', '0:3:m3', '0:4:M4', '0:5:p4', '0:6:#4', '0:7:p5', '0:8:m6', '0:9:M6', '0:10:b7', '0:11:M7', '0:12:oct', '0:13:b9', '0:14:9', '0:15:#9', '0:16:b11', '0:17:11', '0:18:#11', '0:19:d13', '0:20:m13', '0:21:M13', '0:21:A13']

def inversion(chord, n):
    s = chord.split(':')
    quality = s.pop(-1)
    for _ in range(n):
        note = s.pop(0)
        s.append(note)
    inv=''
    for n in s:
        inv+= n + ':'
    return inv + quality

def pitch_selector(l, n):
    m = len(l)
    octave = 0
    p = notes.index(l[0])
    l[0] += str(n)
    for i in range(1, m):
        if l[i][-1] == 'Ω':
            l[i] = l[i][:-1]
            octave +=1
        p2 = notes.index(l[i])
        if p2 <= p:
            octave += 1
        p = p2
        l[i] += str(n+octave)

def construct_chord(key, structure, n):
    str_inv = inversion(structure, n)
    s = str_inv.split(':')
    quality = s.pop(-1)
    i = notes.index(key)
    type_of_triad = quality
    try:
        if need_to_change_root[type_of_triad]:
            name = notes[(i+int(s[0]))%12] + inversion_names[type_of_triad][n]
            quality = inversion_names[type_of_triad][n]
        else:
            name = notes[i] + inversion_names[type_of_triad][n]
    except (KeyError, IndexError):
        name = key  + quality + ' {}-inversion'.format(n)
    note_list = []
    for j in s:
        j = int(j)
        if j>=12:
            note_list.append(notes[(i+int(j))%12]+'Ω')
        else:
             note_list.append(notes[(i+int(j))%12])
        
    pitch_selector(note_list, PITCH_START)
    return note_list, quality, type_of_triad, n, name