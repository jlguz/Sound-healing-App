"""
Frequency data for SoundHealer.
Icons use Material Design icon names (rendered via MDIcon — works on Android).
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
        "md_icon": "shield-check",
    },
    {
        "freq":    285,
        "name":    "285 Hz",
        "note":    "Restoration",
        "benefit": "Tissue Healing",
        "detail":  "Influences energy fields, aids in healing wounds and regenerating damaged tissues.",
        "color":   "#FF9A5C",
        "md_icon": "leaf",
    },
    {
        "freq":    396,
        "name":    "396 Hz",
        "note":    "UT",
        "benefit": "Liberation from Fear & Guilt",
        "detail":  "Transforms grief into joy, liberates from subconscious negative beliefs and fear.",
        "color":   "#FFD166",
        "md_icon": "lock-open-variant",
    },
    {
        "freq":    417,
        "name":    "417 Hz",
        "note":    "RE",
        "benefit": "Undoing Situations & Change",
        "detail":  "Facilitates change, clears traumatic experiences, dissolves crystallised negative patterns.",
        "color":   "#FFB347",
        "md_icon": "refresh",
    },
    {
        "freq":    432,
        "name":    "432 Hz",
        "note":    "Universal",
        "benefit": "Natural Tuning & Harmony",
        "detail":  "Mathematically consistent with patterns of the universe. Natural alternative to 440 Hz.",
        "color":   "#C0C0E0",
        "md_icon": "earth",
    },
    {
        "freq":    528,
        "name":    "528 Hz",
        "note":    "MI",
        "benefit": "DNA Repair & Love",
        "detail":  "Known as the Love Frequency. Associated with transformation, DNA repair and life energy.",
        "color":   "#06D6A0",
        "md_icon": "dna",
    },
    {
        "freq":    639,
        "name":    "639 Hz",
        "note":    "FA",
        "benefit": "Connecting Relationships",
        "detail":  "Enhances communication, understanding and tolerance. Promotes harmonious relationships.",
        "color":   "#48CAE4",
        "md_icon": "account-group",
    },
    {
        "freq":    741,
        "name":    "741 Hz",
        "note":    "SOL",
        "benefit": "Awakening Intuition",
        "detail":  "Cleans cells from toxins and electromagnetic radiations. Awakens intuition.",
        "color":   "#7B2FBE",
        "md_icon": "eye-outline",
    },
    {
        "freq":    852,
        "name":    "852 Hz",
        "note":    "LA",
        "benefit": "Returning to Spiritual Order",
        "detail":  "Raises awareness and returns you to spiritual order. Replaces negative thoughts.",
        "color":   "#C77DFF",
        "md_icon": "flower-tulip",
    },
    {
        "freq":    963,
        "name":    "963 Hz",
        "note":    "SI",
        "benefit": "Divine Consciousness",
        "detail":  "Activates the pineal gland and connects to non-vibratory energy of spirit.",
        "color":   "#F0E6FF",
        "md_icon": "star-circle",
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
        "md_icon":  "square",
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
        "symbol":   "☽",
        "md_icon":  "moon-waning-crescent",
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
        "md_icon":  "white-balance-sunny",
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
        "md_icon":  "heart",
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
        "symbol":   "○",
        "md_icon":  "microphone-outline",
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
        "md_icon":  "eye-circle",
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
        "md_icon":  "crown",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM PRESETS
# ─────────────────────────────────────────────────────────────────────────────
PRESETS = [
    {"freq":  7.83,  "name": "Schumann Resonance", "benefit": "Earth's heartbeat"},
    {"freq": 40.0,   "name": "Gamma 40 Hz",         "benefit": "Focus & memory"},
    {"freq": 111.0,  "name": "Cell Regeneration",   "benefit": "Ancient healing"},
    {"freq": 136.10, "name": "OM Frequency",
        "benefit": "Universal harmonic"},
    {"freq": 256.0,  "name": "Pure Middle C",
        "benefit": "Binaural reference"},
    {"freq": 432.0,  "name": "432 Hz Concert A",     "benefit": "Natural tuning"},
]


# ─────────────────────────────────────────────────────────────────────────────
# ORGAN FREQUENCIES
# Sourced from sound healing research and vibroacoustic therapy literature.
# References: ISO 2631 whole-body vibration studies, Tainio Technology
# bioenergetic research, and established sound therapy frequency tables.
# Note: These are used as therapeutic resonance targets in sound healing
# practice. Individual variation applies — always combine with professional
# healthcare guidance.
# ─────────────────────────────────────────────────────────────────────────────
ORGANS = [
    {
        "freq":    315.8,
        "name":    "Brain",
        "benefit": "Clarity · Focus · Neural Balance",
        "detail":  "Supports cognitive function, mental clarity and neural coherence. Used in sound therapy for focus and memory enhancement.",
        "color":   "#FF6B9D",
        "md_icon": "brain",
        "system":  "Nervous",
    },
    {
        "freq":    319.88,
        "name":    "Heart",
        "benefit": "Circulation · Vitality · Rhythm",
        "detail":  "Supports cardiovascular health and heart coherence. The heart's electromagnetic field is the strongest in the body.",
        "color":   "#FF4444",
        "md_icon": "heart-pulse",
        "system":  "Cardiovascular",
    },
    {
        "freq":    220.0,
        "name":    "Lungs",
        "benefit": "Breath · Oxygenation · Release",
        "detail":  "Supports respiratory function and deep breathing. Encourages release of stagnant energy and emotional holding.",
        "color":   "#48CAE4",
        "md_icon": "air-filter",
        "system":  "Respiratory",
    },
    {
        "freq":    317.83,
        "name":    "Liver",
        "benefit": "Detox · Regeneration · Vitality",
        "detail":  "Supports liver detoxification and regenerative processes. The liver is the body's primary metabolic organ.",
        "color":   "#FF8C42",
        "md_icon": "water",
        "system":  "Digestive",
    },
    {
        "freq":    319.88,
        "name":    "Kidneys",
        "benefit": "Filtration · Balance · Vitality",
        "detail":  "Supports kidney filtration and fluid balance. In traditional medicine, kidneys are considered the seat of life force.",
        "color":   "#F4A460",
        "md_icon": "water-circle",
        "system":  "Urinary",
    },
    {
        "freq":    110.0,
        "name":    "Stomach",
        "benefit": "Digestion · Nourishment · Grounding",
        "detail":  "Supports digestive function and nutrient absorption. Helps calm digestive discomfort and nervous tension in the gut.",
        "color":   "#FFD166",
        "md_icon": "stomach",
        "system":  "Digestive",
    },
    {
        "freq":    281.0,
        "name":    "Intestines",
        "benefit": "Processing · Absorption · Flow",
        "detail":  "Supports intestinal motility and nutrient absorption. The gut-brain axis makes intestinal health vital for mood.",
        "color":   "#06D6A0",
        "md_icon": "transit-connection",
        "system":  "Digestive",
    },
    {
        "freq":    352.0,
        "name":    "Bladder",
        "benefit": "Release · Cleansing · Flow",
        "detail":  "Supports bladder function and healthy fluid release. Encourages letting go of emotional and physical tension.",
        "color":   "#4FC3F7",
        "md_icon": "water-pump",
        "system":  "Urinary",
    },
    {
        "freq":    117.3,
        "name":    "Pancreas",
        "benefit": "Balance · Regulation · Sweetness",
        "detail":  "Supports pancreatic function and blood sugar regulation. Connected to how we process the sweetness of life.",
        "color":   "#F06292",
        "md_icon": "candy-outline",
        "system":  "Endocrine",
    },
    {
        "freq":    176.0,
        "name":    "Colon",
        "benefit": "Elimination · Release · Renewal",
        "detail":  "Supports healthy bowel function and waste elimination. Releasing what no longer serves — physically and emotionally.",
        "color":   "#A5D6A7",
        "md_icon": "recycle",
        "system":  "Digestive",
    },
    {
        "freq":    492.8,
        "name":    "Adrenals",
        "benefit": "Energy · Stress Response · Resilience",
        "detail":  "Supports adrenal gland function and cortisol balance. Helps regulate the body's response to stress and fatigue.",
        "color":   "#FFB300",
        "md_icon": "lightning-bolt",
        "system":  "Endocrine",
    },
    {
        "freq":    321.9,
        "name":    "Blood",
        "benefit": "Circulation · Oxygen · Life Force",
        "detail":  "Supports healthy blood flow and oxygen delivery. Blood carries nutrients, immune cells and life force throughout the body.",
        "color":   "#EF5350",
        "md_icon": "water-drop",
        "system":  "Cardiovascular",
    },
    {
        "freq":    324.0,
        "name":    "Muscles",
        "benefit": "Strength · Recovery · Flexibility",
        "detail":  "Supports muscle repair and recovery. Used in vibroacoustic therapy to ease tension and support physical rehabilitation.",
        "color":   "#7E57C2",
        "md_icon": "arm-flex-outline",
        "system":  "Musculoskeletal",
    },
    {
        "freq":    418.3,
        "name":    "Bones",
        "benefit": "Structure · Density · Foundation",
        "detail":  "Supports bone density and structural integrity. Low-frequency vibration (35-50 Hz) has shown bone healing effects in research.",
        "color":   "#90A4AE",
        "md_icon": "bone",
        "system":  "Musculoskeletal",
    },
]

# Body systems for filtering
ORGAN_SYSTEMS = sorted(set(o['system'] for o in ORGANS))


# ─────────────────────────────────────────────────────────────────────────────
# MUSICAL NOTES — equal temperament
# ─────────────────────────────────────────────────────────────────────────────
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_ALIASES = {
    'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'
}
NOTE_COLORS = {
    'C':  '#FF4455', 'C#': '#FF6644', 'D':  '#FF8833', 'D#': '#FFAA22',
    'E':  '#FFDD11', 'F':  '#88DD33', 'F#': '#33DD88', 'G':  '#22CCBB',
    'G#': '#33AAEE', 'A':  '#4477FF', 'A#': '#8844FF', 'B':  '#CC44FF',
}
NOTE_CHAKRA = {
    'C': 'Root', 'D': 'Sacral', 'E': 'Solar Plexus',
    'F': 'Heart', 'G': 'Throat', 'A': 'Third Eye', 'B': 'Crown',
}


def note_freq(semitone_index: int, octave: int, tuning: float = 440.0) -> float:
    midi = (octave + 1) * 12 + semitone_index
    return tuning * (2.0 ** ((midi - 69) / 12.0))


def generate_notes(octave_range=range(2, 8), tuning: float = 440.0) -> list:
    notes = []
    for octave in octave_range:
        for idx, name in enumerate(NOTE_NAMES):
            freq = note_freq(idx, octave, tuning)
            natural = '#' not in name
            base = name[0]
            alias = NOTE_ALIASES.get(name, '')
            chakra = NOTE_CHAKRA.get(base, '')
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
            })
    return notes


NOTES_440 = generate_notes(tuning=440.0)
NOTES_432 = generate_notes(tuning=432.0)


def get_notes(tuning: float = 440.0) -> list:
    return NOTES_440 if abs(tuning - 440.0) < 0.01 else NOTES_432
