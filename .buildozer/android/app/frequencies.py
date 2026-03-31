"""
Frequency data for SoundHealer.
Includes Solfeggio, Chakra, Presets, and Musical Notes (440 Hz & 432 Hz).
"""

import math

# ─────────────────────────────────────────────────────────────────────────────
# SOLFEGGIO FREQUENCIES
# ─────────────────────────────────────────────────────────────────────────────
SOLFEGGIO = [
    {
        "freq":    174,
        "name":    "174 Hz",
        "note":    "Foundation",
        "benefit": "Pain Relief & Security",
        "detail":  "The lowest Solfeggio frequency. Reduces physical and energetic pain, provides a sense of safety and grounding.",
        "color":   "#FF6B6B",
        "icon":    "🔴",
    },
    {
        "freq":    285,
        "name":    "285 Hz",
        "note":    "Restoration",
        "benefit": "Tissue Healing",
        "detail":  "Influences energy fields, aids in healing wounds and regenerating damaged tissues.",
        "color":   "#FF9A5C",
        "icon":    "🟠",
    },
    {
        "freq":    396,
        "name":    "396 Hz",
        "note":    "UT",
        "benefit": "Liberation from Fear & Guilt",
        "detail":  "Transforms grief into joy, liberates from subconscious negative beliefs and fear.",
        "color":   "#FFD166",
        "icon":    "🟡",
    },
    {
        "freq":    417,
        "name":    "417 Hz",
        "note":    "RE",
        "benefit": "Undoing Situations & Change",
        "detail":  "Facilitates change, clears traumatic experiences, dissolves crystallised negative patterns.",
        "color":   "#FFB347",
        "icon":    "✨",
    },
    {
        "freq":    432,
        "name":    "432 Hz",
        "note":    "Universal",
        "benefit": "Natural Tuning & Harmony",
        "detail":  "Mathematically consistent with patterns of the universe. Natural alternative to 440 Hz.",
        "color":   "#C0C0E0",
        "icon":    "🌐",
    },
    {
        "freq":    528,
        "name":    "528 Hz",
        "note":    "MI",
        "benefit": "DNA Repair & Love",
        "detail":  "Known as the Love Frequency. Associated with transformation, DNA repair and life energy.",
        "color":   "#06D6A0",
        "icon":    "💚",
    },
    {
        "freq":    639,
        "name":    "639 Hz",
        "note":    "FA",
        "benefit": "Connecting Relationships",
        "detail":  "Enhances communication, understanding and tolerance. Promotes harmonious relationships.",
        "color":   "#48CAE4",
        "icon":    "💙",
    },
    {
        "freq":    741,
        "name":    "741 Hz",
        "note":    "SOL",
        "benefit": "Awakening Intuition",
        "detail":  "Cleans cells from toxins and electromagnetic radiations. Awakens intuition.",
        "color":   "#7B2FBE",
        "icon":    "🔮",
    },
    {
        "freq":    852,
        "name":    "852 Hz",
        "note":    "LA",
        "benefit": "Returning to Spiritual Order",
        "detail":  "Raises awareness and returns you to spiritual order. Replaces negative thoughts.",
        "color":   "#C77DFF",
        "icon":    "🪷",
    },
    {
        "freq":    963,
        "name":    "963 Hz",
        "note":    "SI",
        "benefit": "Divine Consciousness",
        "detail":  "Activates the pineal gland and connects to non-vibratory energy of spirit.",
        "color":   "#F0E6FF",
        "icon":    "⭐",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# CHAKRA FREQUENCIES (Solfeggio-aligned)
# ─────────────────────────────────────────────────────────────────────────────
CHAKRA = [
    {
        "freq":     396,
        "name":     "Root Chakra",
        "sanskrit": "Mūlādhāra",
        "number":   1,
        "benefit":  "Grounding · Safety · Survival",
        "detail":   "The foundation of the energy body. Provides security, stability and earth connection.",
        "color":    "#CC0000",
        "glow":     "#FF4444",
        "location": "Base of spine",
        "element":  "Earth",
        "symbol":   "◼",
        "icon":     "◼",
    },
    {
        "freq":     417,
        "name":     "Sacral Chakra",
        "sanskrit": "Svādhiṣṭhāna",
        "number":   2,
        "benefit":  "Creativity · Pleasure · Emotion",
        "detail":   "Centre of creativity and sensuality. Emotional intelligence and joyful expression.",
        "color":    "#FF6600",
        "glow":     "#FF8C42",
        "location": "Lower abdomen",
        "element":  "Water",
        "symbol":   "🌙",
        "icon":     "🌙",
    },
    {
        "freq":     528,
        "name":     "Solar Plexus",
        "sanskrit": "Maṇipūra",
        "number":   3,
        "benefit":  "Power · Confidence · Will",
        "detail":   "Seat of personal power. Confidence, motivation and strong sense of identity.",
        "color":    "#FFD700",
        "glow":     "#FFEC6E",
        "location": "Upper abdomen",
        "element":  "Fire",
        "symbol":   "☀",
        "icon":     "☀",
    },
    {
        "freq":     639,
        "name":     "Heart Chakra",
        "sanskrit": "Anāhata",
        "number":   4,
        "benefit":  "Love · Compassion · Healing",
        "detail":   "Bridge between lower and upper chakras. Unconditional love and deep inner peace.",
        "color":    "#00BB44",
        "glow":     "#00FF7F",
        "location": "Centre of chest",
        "element":  "Air",
        "symbol":   "♥",
        "icon":     "♥",
    },
    {
        "freq":     741,
        "name":     "Throat Chakra",
        "sanskrit": "Viśuddha",
        "number":   5,
        "benefit":  "Truth · Expression · Communication",
        "detail":   "The voice of the body. Authentic self-expression and clear communication.",
        "color":    "#0088FF",
        "glow":     "#44AAFF",
        "location": "Throat",
        "element":  "Sound / Ether",
        "symbol":   "◯",
        "icon":     "◯",
    },
    {
        "freq":     852,
        "name":     "Third Eye",
        "sanskrit": "Ājñā",
        "number":   6,
        "benefit":  "Intuition · Clarity · Insight",
        "detail":   "Seat of intuition and higher knowledge. Strong intuition and expanded awareness.",
        "color":    "#5500BB",
        "glow":     "#8844EE",
        "location": "Forehead, between eyes",
        "element":  "Light",
        "symbol":   "◉",
        "icon":     "◉",
    },
    {
        "freq":     963,
        "name":     "Crown Chakra",
        "sanskrit": "Sahasrāra",
        "number":   7,
        "benefit":  "Unity · Enlightenment · Spirit",
        "detail":   "Highest chakra, connecting to universal consciousness. Bliss and Oneness.",
        "color":    "#AA44FF",
        "glow":     "#DD99FF",
        "location": "Top of head",
        "element":  "Thought / Cosmic energy",
        "symbol":   "✦",
        "icon":     "✦",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM PRESETS
# ─────────────────────────────────────────────────────────────────────────────
PRESETS = [
    {"freq":  7.83,  "name": "Schumann Resonance", "benefit": "Earth's heartbeat"},
    {"freq": 40.0,   "name": "Gamma 40 Hz",         "benefit": "Focus & memory"},
    {"freq": 111.0,  "name": "Cell Regeneration",   "benefit": "Ancient healing"},
    {"freq": 136.10, "name": "OM Frequency",         "benefit": "Universal harmonic"},
    {"freq": 256.0,  "name": "Pure Middle C",        "benefit": "Binaural reference"},
    {"freq": 432.0,  "name": "432 Hz Concert A",     "benefit": "Natural tuning"},
]


# ─────────────────────────────────────────────────────────────────────────────
# MUSICAL NOTES — equal temperament
# Formula: freq = tuning * 2^((midi - 69) / 12)
# MIDI 69 = A4.  At 432 Hz all notes shift by ratio 432/440 (mathematically
# exact — the whole scale moves together).
# ─────────────────────────────────────────────────────────────────────────────

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

NOTE_ALIASES = {
    'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'
}

NOTE_COLORS = {
    'C':  '#FF4455',
    'C#': '#FF6644',
    'D':  '#FF8833',
    'D#': '#FFAA22',
    'E':  '#FFDD11',
    'F':  '#88DD33',
    'F#': '#33DD88',
    'G':  '#22CCBB',
    'G#': '#33AAEE',
    'A':  '#4477FF',
    'A#': '#8844FF',
    'B':  '#CC44FF',
}

# Traditional Western note → chakra associations
NOTE_CHAKRA = {
    'C': 'Root',
    'D': 'Sacral',
    'E': 'Solar Plexus',
    'F': 'Heart',
    'G': 'Throat',
    'A': 'Third Eye',
    'B': 'Crown',
}


def note_freq(semitone_index: int, octave: int, tuning: float = 440.0) -> float:
    """
    Return the frequency of a note in equal temperament.
    semitone_index : 0 = C, 1 = C#, …, 11 = B
    octave         : integer (standard range 0–8)
    tuning         : A4 reference Hz (440.0 or 432.0)
    MIDI: C-1=0, C0=12, C4=60, A4=69
    """
    midi = (octave + 1) * 12 + semitone_index
    return tuning * (2.0 ** ((midi - 69) / 12.0))


def generate_notes(octave_range=range(2, 8), tuning: float = 440.0) -> list:
    """Build a note list for the given octave range and tuning."""
    notes = []
    for octave in octave_range:
        for idx, name in enumerate(NOTE_NAMES):
            freq    = note_freq(idx, octave, tuning)
            natural = '#' not in name
            base    = name[0]
            alias   = NOTE_ALIASES.get(name, '')
            chakra  = NOTE_CHAKRA.get(base, '')

            notes.append({
                'name':       name,
                'alias':      alias,
                'octave':     octave,
                'display':    f'{name}{octave}',
                'full':       f'{name}{octave}' + (f' / {alias}{octave}' if alias else ''),
                'freq':       round(freq, 2),
                'freq_str':   f'{freq:.2f}',
                'is_natural': natural,
                'color':      NOTE_COLORS[name],
                'chakra':     chakra,
                'icon':       name[0],
            })
    return notes


# Pre-built tables — generated once at import time
NOTES_440 = generate_notes(tuning=440.0)
NOTES_432 = generate_notes(tuning=432.0)


def get_notes(tuning: float = 440.0) -> list:
    return NOTES_440 if abs(tuning - 440.0) < 0.01 else NOTES_432
