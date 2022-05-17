//-----Global constants and variables ------------------

const FREQ = {
    'C2':   65.41, 'D♭2':  69.30, 'D2':   73.42, 'E♭2':  77.78, 'E2':   82.41, 'F2':   87.31, 'G♭2':  92.50, 'G2':   98.00, 'A♭2':  103.83, 'A2':   110.00, 'B♭2':  116.54, 'B2':   123.47,
    'C3':   130.81, 'D♭3':  138.59, 'D3':   146.83, 'E♭3':  155.56, 'E3':   164.81, 'F3':   174.61, 'G♭3':  185.00, 'G3':   196.00, 'A♭3':  207.65, 'A3':   220.00, 'B♭3':  233.08, 'B3':   246.94,
    'C4':   261.63, 'D♭4':  277.18, 'D4':   293.66, 'E♭4':  311.13, 'E4':   329.63, 'F4':   349.23, 'G♭4':  369.99, 'G4':   392.00, 'A♭4':  415.30, 'A4':   440.00, 'B♭4':  466.16, 'B4':   493.88,
    'C5': 523.25, 'D♭5':  554.37, 'D5': 587.33, 'E♭5':  622.25, 'E5': 659.25, 'F5': 698.46, 'G♭5':  739.99, 'G5': 783.99, 'A♭5':  830.61, 'A5': 880.00, 'B♭5':  932.33, 'B5': 987.77,
    'C6': 1046.50, 'D♭6':  1108.73, 'D6': 1174.66, 'E♭6':  1244.51, 'E6': 1318.51, 'F6': 1396.91, 'G♭6':  1479.98, 'G6': 1567.98, 'A♭6':  1661.22, 'A6': 1760.00, 'B♭6':  1864.66, 'B6': 1975.53,
};

const NOTES = ['C4','D♭4', 'D4','E♭4', 'E4', 'F4','G♭4', 'G4', 'A♭4','A4','B♭4', 'B4', 'C5','D♭5', 'D5','E♭5', 'E5', 'F5','G♭5', 'G5', 'A♭5', 'A5','B♭5', 'B5', 'C6','D♭6', 'D6','E♭6', 'E6', 'F6','G♭6', 'G6', 'A♭6', 'A6','B♭6', 'B6']

const unison = 0;
const b2 = 1;
const m3 = 3;
const M3 = 4;
const p4 = 5;
const b5 = 6;
const p5 = 7;
const m6 = 8;
const M6 = 9;
const m7 = 10;
const M7 = 11;
const oct = 12;

const ANSWERS = {

    'maj7' : ['maj7', 'M7', '+7'],
    'min7' : ['min7', 'm7', '-7'],
    '7' : ['dom7', 'dom', '7'],

    'unison' : ['unison', '0', 'u'],
    '♭2' : ['b2', 'm2', 'min2', '-2', 's1', '+1'],
    '2nd' : ['2', 'M2', 'maj2', '+2'],
    'min3' : ['min3', 'b3', '-3', 'm3', 'aug2'],
    '3rd' : ['maj3', '+3', '3', 'b4'],
    '4th' : ['p4', '4th', '4'],
    'tritone' : ['triton', 'tri', 'b5', 's4', '+4', 'aug4'],
    '5th' : ['5th', 'p5', '5'],
    'min6' : ['min6', 'm6', 'b6'],
    'maj6' : ['6', 'M6', 'maj6'],
    '♭7' : ['m7', 'b7', 'min7'],
    '7' : ['7', 'M7', '+7'],
    'octave' : ['8', 'octave', 'oct'],

    'Do' : ['do'],
    'Re' : ['re'],
    'Mi': ['mi'] ,
    'Fa' : ['fa'],
    'So' : ['so', 'sol'],
    'La' : ['la'],
    'Ti' : ['ti', 'si'],
}


const ACTX = new (AudioContext || webkitAudioContext)();
if (!ACTX) throw 'Not supported :()';

var GAMEMODE = 'chords';
const GAIN = 0.2;

//----- Functions -----------------------------------

function newOscillator() {
    const gain = ACTX.createGain();
    gain.gain.value = GAIN;
    gain.connect(ACTX.destination);
    const osc = ACTX.createOscillator();
    osc.type = 'sine';
    osc.connect(gain);
    return osc
};

function playChord(noteList) {
    const ct = ACTX.currentTime;
    noteList.forEach(note => {
        const osc = newOscillator();
        osc.frequency.value = FREQ[note];
        osc.start(ct);
        osc.stop(ct+1);
    });
};

function playArpegio(noteList) {
    const ct = ACTX.currentTime;
    var t = ct;
    noteList.forEach(note => {
        const osc = newOscillator();
        osc.frequency.value = FREQ[note];
        osc.start(t);
        osc.stop(t+0.5);
        t = t+0.5;
    });
};


function generateChoices() {
    return [{'maj7':[0, M3, p5, M7], 'min7':[0, m3, p5, m7], '7':[0, M3, p5, m7]},
            {'unison':[0,0], '♭2':[0, b2], '2nd':[0, 2], 'min3':[0,m3], '3rd':[0, M3], '4th':[0,p4], 'tritone':[0,b5], '5th':[0,p5], 'min6':[0,m6], 'maj6':[0,M6], '♭7':[0,m7], '7':[0,M7], 'octave':[0,oct]},
            {'Do':[0], 'Re':[2], 'Mi':[M3], 'Fa':[p4], 'So':[p5], 'La':[M6], 'Ti':[M7]}
           ]
};

function randomChoice(obj) {
    var keys = Object.keys(obj);
    var key = keys[ keys.length * Math.random() << 0];
    return [key, obj[key]]
};

function randomNotes(obj) {
    var rootIndex = 12 * Math.random() << 0;
    let goal, intervals;
    [goal, intervals] = randomChoice(obj);
    return [goal, intervals.map((n) => NOTES[rootIndex + n])]
};

function randomNotesInC(obj) {
    let goal, intervals;
    [goal, intervals] = randomChoice(obj);
    return [goal, intervals.map((n) => NOTES[n])]
}

//------- Bindings ------------------------------------

[chordChoices, intervalChoices, solfegeChoices] = generateChoices();

var userInput = document.querySelector('.entry-bar input');

goal = 'TYPE YOUR ANSWER'
answer = []
notes = []

function resetEntry() {
    userInput.value = '';
    const entry = document.querySelector('#entry');
    entry.setSelectionRange(0,0);
    entry.focus();
}


function newChord() {
    document.querySelector('.goal').innerText = goal;
    //document.querySelector('.goal').style.filter = "blur(1.5rem)";
    [quality, notes] = randomNotes(chordChoices);
    goal = notes[0].slice(0,-1) + quality
    answer = ANSWERS[quality];
    //console.log(notes);
    playChord(notes);
};

function newInterval() {
    document.querySelector('.goal').innerText = goal;
    [quality, notes] = randomNotes(intervalChoices);
    goal = quality;
    answer = ANSWERS[quality];
    playChord(notes);
};

function newSolfege() {
    document.querySelector('.goal').innerText = goal;
    [quality, notes] = randomNotesInC(solfegeChoices);
    goal = quality;
    answer = ANSWERS[quality];
    playChord(notes);
};


function newGoal() {
    switch (GAMEMODE) {
    case 'chords':
        newChord();
        break;
    case 'intervals':
        newInterval();
        break;
    case 'solfege':
        newSolfege();
    }
    resetEntry();
}

function replay() {
    playChord(notes);
};

function spell() {
    switch (GAMEMODE) {
    case 'solfege':
        playChord(['C4', 'E4', 'G4', 'C5']);
        break;
    default:
        replay();
    }
};

document.querySelector('#play').addEventListener('click', () => {
    newGoal();

});

//TODO: figure out how to get rid of that god dammned space !!!
document.onkeydown = function(e) {
    switch (e.key) {
    case 'Backspace':
        resetEntry();
        break;
    case ' ':
        e.preventDefault();
        newGoal();
        break;
    case 'r':
        if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            replay();
        }
        break;
    case 's':
        if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            spell();
        }
        break;
    }
};

document.querySelector('#replay').addEventListener('click', () => {
    replay();

});

document.querySelector('#spell').addEventListener('click', () => {
    spell();

});

userInput.addEventListener('input', function(e) {
    if (answer.includes(userInput.value)) {
            newGoal();
        }
});

function hashHandler() {

    newMode = location.hash.slice(1);

    document.querySelectorAll('.current-mode div').forEach(item => {item.style.display = 'none';});
    document.querySelectorAll('.current-mode .' + newMode).forEach(item => {item.style.display = 'flex';});

    document.querySelectorAll('.game-modes a').forEach(item => {item.style.color = 'black';});
    document.querySelectorAll('.game-modes .' + newMode).forEach(item => {item.style.color = 'purple';});

    GAMEMODE = newMode;

    console.log('New Game-mode : ' + GAMEMODE)
    resetEntry();

    switch (GAMEMODE) {
    case 'solfege':
        playChord(['C4', 'E4', 'G4', 'C5']);
        document.querySelector('.goal').innerText = "PLAYING REFERENCE\nPRESS SPACE";
        break;
    }
}

window.addEventListener('hashchange', hashHandler);
window.addEventListener('load', hashHandler);
