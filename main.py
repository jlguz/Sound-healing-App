"""
SoundHealer — Healing Through Sound
KivyMD-based Android app.

All visual styling is in soundhealer.kv.
This file contains only logic, widget construction, and audio wiring.

Run:   python main.py
Build: buildozer android debug
"""

from kivymd.uix.button import MDRaisedButton, MDFlatButton

from kivy.config import Config
Config.set('graphics', 'width',     '420')   # logical pixels wide
Config.set('graphics', 'height',    '909')   # logical pixels tall
Config.set('graphics', 'resizable', '0')     # lock — no accidental resizing
Config.set('graphics', 'dpi',       '480')   # base Android mdpi density

import math


from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.properties import BooleanProperty, ListProperty

from audio_engine import FrequencyEngine
from frequencies import SOLFEGGIO, CHAKRA, PRESETS, get_notes

# ── Colour mirrors (for Python canvas ops) ─────────────────────────────────────
BG      = (0.039, 0.039, 0.102, 1)
CARD    = (0.102, 0.102, 0.208, 1)
CARD2   = (0.118, 0.118, 0.235, 1)
BORDER  = (0.165, 0.165, 0.314, 1)
TEAL    = (0.024, 0.839, 0.627, 1)
GOLD    = (0.957, 0.769, 0.188, 1)
PINK    = (0.969, 0.145, 0.522, 1)
PURPLE  = (0.482, 0.184, 0.745, 1)
TEXT1   = (0.941, 0.941, 1.000, 1)
TEXT2   = (0.565, 0.565, 0.690, 1)
TEXT3   = (0.314, 0.314, 0.627, 1)

# Single shared audio engine
_engine = FrequencyEngine()


# ══════════════════════════════════════════════════════════════════════════════
#  WAVEFORM WIDGET  (pure canvas — no KivyMD equivalent)
# ══════════════════════════════════════════════════════════════════════════════
class WaveformWidget(Widget):
    active     = BooleanProperty(False)
    wave_color = ListProperty([*TEAL[:3], 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._phase = 0.0
        self._event = None
        self.bind(size=self._redraw, pos=self._redraw, active=self._on_active)

    def _on_active(self, *_):
        if self.active:
            self._event = Clock.schedule_interval(self._tick, 1 / 30)
        else:
            if self._event:
                self._event.cancel()
            self._phase = 0.0
            self._draw()

    def _tick(self, dt):
        self._phase = (self._phase + 0.12) % (2 * math.pi)
        self._draw()

    def _redraw(self, *_):
        self._draw()

    def _draw(self):
        self.canvas.clear()
        with self.canvas:
            w, h = self.width, self.height
            cx   = self.x
            cy   = self.y + h / 2

            if not self.active:
                Color(*TEXT3)
                Line(points=[self.x, cy, self.x + w, cy], width=dp(1.5))
                return

            r, g, b, _ = self.wave_color
            Color(r, g, b, 0.12)
            pts = self._pts(cx, cy, w, h * 0.50, 3, 0.0)
            if pts:
                Line(points=pts, width=dp(9))

            Color(r, g, b, 0.90)
            pts = self._pts(cx, cy, w, h * 0.36, 3, 0.0)
            if pts:
                Line(points=pts, width=dp(2.5))

            Color(1, 1, 1, 0.28)
            pts = self._pts(cx, cy, w, h * 0.20, 3, 0.45)
            if pts:
                Line(points=pts, width=dp(1.2))

    def _pts(self, cx, cy, width, amp, cycles, phase_off):
        steps = max(int(width / 2), 2)
        pts   = []
        for i in range(steps + 1):
            x = cx + (i / steps) * width
            y = cy + amp * math.sin(
                2 * math.pi * cycles * (i / steps) + self._phase + phase_off
            )
            pts.extend([x, y])
        return pts


# ══════════════════════════════════════════════════════════════════════════════
#  FREQUENCY CARD  (MDCard base, accent colour applied dynamically)
# ══════════════════════════════════════════════════════════════════════════════
class FrequencyCard(MDCard):
    """
    KV rule sets the card frame (radius, elevation, size).
    Python __init__ builds internal MDLabel/MDRaisedButton content
    and applies the per-frequency accent colour.
    """

    def __init__(self, data: dict, engine: FrequencyEngine,
                 on_play_callback=None, **kwargs):
        super().__init__(**kwargs)
        self._data    = data
        self._engine  = engine
        self._playing = False
        self._on_play = on_play_callback
        self._accent  = get_color_from_hex(data.get('color', '#7B2FBE'))

        # Card background — accent tint over dark base
        r, g, b, _ = self._accent
        self.md_bg_color = (
            CARD[0] + r * 0.08,
            CARD[1] + g * 0.08,
            CARD[2] + b * 0.08,
            1
        )

        self._build()

    def _build(self):
        d = self._data

        # ── Row 1: icon · name · note badge ──────────────────────────────────
        top = BoxLayout(orientation='horizontal',
                        size_hint_y=None, height=dp(28), spacing=dp(4))

        icon_l = MDLabel(
            text=d.get('icon', '◉'),
            theme_text_color='Custom', text_color=self._accent,
            font_style='H6',
            size_hint_x=None, width=dp(32),
            halign='left', valign='middle'
        )
        icon_l.bind(size=icon_l.setter('text_size'))

        name_l = MDLabel(
            text=d['name'],
            theme_text_color='Custom', text_color=TEXT1,
            font_style='Subtitle1',
            halign='left', valign='middle'
        )
        name_l.bind(size=name_l.setter('text_size'))

        badge_text = d.get('note') or d.get('sanskrit') or ''
        badge = MDLabel(
            text=badge_text,
            theme_text_color='Custom', text_color=self._accent,
            font_style='Caption',
            size_hint_x=None, width=dp(90),
            halign='right', valign='middle'
        )
        badge.bind(size=badge.setter('text_size'))

        top.add_widget(icon_l)
        top.add_widget(name_l)
        top.add_widget(badge)
        self.add_widget(top)

        # ── Row 2: benefit ────────────────────────────────────────────────────
        bft = MDLabel(
            text=d.get('benefit', ''),
            theme_text_color='Custom', text_color=TEXT2,
            font_style='Caption',
            halign='left', valign='top'
        )
        bft.bind(size=bft.setter('text_size'))
        self.add_widget(bft)

        # ── Row 3: play btn + Hz label ────────────────────────────────────────
        bottom = BoxLayout(orientation='horizontal',
                           size_hint_y=None, height=dp(38), spacing=dp(8))

        self._play_btn = MDRaisedButton(
            text='PLAY',
            elevation=0,
            font_size=sp(12),
            md_bg_color=(*self._accent[:3], 0.9),
            text_color=BG,
            size_hint_x=0.46,
        )
        self._play_btn.bind(on_release=self._toggle)

        hz_l = MDLabel(
            text=f"{d['freq']} Hz",
            theme_text_color='Custom',
            text_color=(*self._accent[:3], 1),
            font_style='H6',
            halign='right', valign='middle'
        )
        hz_l.bind(size=hz_l.setter('text_size'))

        bottom.add_widget(self._play_btn)
        bottom.add_widget(hz_l)
        self.add_widget(bottom)

    def _toggle(self, *_):
        self._stop() if self._playing else self._play()

    def _play(self):
        if self._on_play:
            self._on_play(self)
        self._playing = True
        self._play_btn.text = 'STOP'
        self._engine.play(self._data['freq'])

    def _stop(self):
        self._playing = False
        self._play_btn.text = 'PLAY'
        self._engine.stop()

    def force_stop(self):
        if self._playing:
            self._playing = False
            self._play_btn.text = 'PLAY'


# ══════════════════════════════════════════════════════════════════════════════
#  NOTE CARD  (compact 3-col grid card for Notes screen)
# ══════════════════════════════════════════════════════════════════════════════
class NoteCard(MDCard):

    def __init__(self, data: dict, engine: FrequencyEngine,
                 on_play_callback=None, **kwargs):
        super().__init__(**kwargs)
        self._data    = data
        self._engine  = engine
        self._playing = False
        self._on_play = on_play_callback
        self._accent  = get_color_from_hex(data.get('color', '#7B2FBE'))

        r, g, b, _ = self._accent
        self.md_bg_color = (
            CARD[0] + r * 0.06,
            CARD[1] + g * 0.06,
            CARD[2] + b * 0.06,
            1
        )
        self._build()

    def _build(self):
        d = self._data

        name_l = MDLabel(
            text=d['full'],
            theme_text_color='Custom',
            text_color=(*self._accent[:3], 1),
            font_style='Subtitle2',
            halign='center', valign='middle',
            size_hint_y=None, height=dp(22)
        )
        name_l.bind(size=name_l.setter('text_size'))
        self.add_widget(name_l)

        freq_l = MDLabel(
            text=f"{d['freq_str']} Hz",
            theme_text_color='Custom', text_color=TEXT2,
            font_style='Caption',
            halign='center', valign='middle',
            size_hint_y=None, height=dp(16)
        )
        freq_l.bind(size=freq_l.setter('text_size'))
        self.add_widget(freq_l)

        chakra_text = d.get('chakra', '')
        ck_l = MDLabel(
            text=chakra_text if chakra_text else '',
            theme_text_color='Custom', text_color=TEXT3,
            font_style='Caption',
            halign='center', valign='middle',
            size_hint_y=None, height=dp(14)
        )
        ck_l.bind(size=ck_l.setter('text_size'))
        self.add_widget(ck_l)

        self._play_btn = MDRaisedButton(
            text='▶',
            elevation=0,
            font_size=sp(12),
            md_bg_color=(*self._accent[:3], 0.85),
            text_color=BG,
            size_hint_y=None,
            height=dp(28)
        )
        self._play_btn.bind(on_release=self._toggle)
        self.add_widget(self._play_btn)

    def _toggle(self, *_):
        self._stop() if self._playing else self._play()

    def _play(self):
        if self._on_play:
            self._on_play(self)
        self._playing = True
        self._play_btn.text = '■'
        self._engine.play(self._data['freq'])

    def _stop(self):
        self._playing = False
        self._play_btn.text = '▶'
        self._engine.stop()

    def force_stop(self):
        if self._playing:
            self._playing = False
            self._play_btn.text = '▶'


# ══════════════════════════════════════════════════════════════════════════════
#  APP
# ══════════════════════════════════════════════════════════════════════════════
class SoundHealerApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title         = 'Sound Healer'
        self._sol_cards    = []
        self._cha_cards    = []
        self._note_cards   = []
        self._tuning       = 432.0
        self._note_filt    = 'all'
        self._oct_filt     = 'all'

    # ── Theme setup ───────────────────────────────────────────────────────────
    def build(self):
        self.theme_cls.theme_style      = 'Dark'
        self.theme_cls.primary_palette  = 'DeepPurple'
        self.theme_cls.accent_palette   = 'Teal'
        return Builder.load_file('soundhealer.kv')

    # ── Populate all dynamic content after KV is ready ────────────────────────
    def on_start(self):
        ids = self.root.ids
        self._build_home_grid(ids)
        self._build_solfeggio(ids)
        self._build_chakra(ids)
        self._build_notes(ids)
        self._wire_custom(ids)
        Clock.schedule_interval(self._update_home_status, 0.4)

    # ── Switch tab programmatically ───────────────────────────────────────────
    def switch_tab(self, name):
        self.root.switch_tab(name)

    # ══════════════════════════════════════════════════════════════════════════
    #  HOME
    # ══════════════════════════════════════════════════════════════════════════
    def _build_home_grid(self, ids):
        grid = ids.home_grid
        sections = [
            ('✦',  'Solfeggio\nFrequencies', '#F4C430', 'solfeggio', '10 ancient healing tones'),
            ('◉',  'Chakra\nFrequencies',    '#7B2FBE', 'chakra',    '7 energy centres'),
            ('〰',  'Custom\nGenerator',      '#06D6A0', 'custom',    'Any frequency'),
            ('♪',  'Musical\nNotes',          '#F72585', 'notes',     'All 12 · 432 Hz'),
        ]
        for icon, label, color, screen, desc in sections:
            grid.add_widget(self._make_home_tile(icon, label, color, screen, desc))

    def _make_home_tile(self, icon, label, color, screen, desc):
        accent = get_color_from_hex(color)
        r, g, b, _ = accent

        tile = MDCard(
            elevation=0,
            radius=[dp(14)],
            ripple_behavior=True,
            orientation='vertical',
            padding=[dp(12), dp(10)],
            spacing=dp(4),
            md_bg_color=(
                CARD[0] + r * 0.06,
                CARD[1] + g * 0.06,
                CARD[2] + b * 0.06,
                1
            )
        )

        icon_l = MDLabel(
            text=icon,
            theme_text_color='Custom', text_color=accent,
            font_style='H5',
            size_hint_y=None, height=dp(38),
            halign='center'
        )
        name_l = MDLabel(
            text=label,
            theme_text_color='Custom', text_color=TEXT1,
            font_style='Subtitle2',
            halign='center', valign='top'
        )
        name_l.bind(size=name_l.setter('text_size'))
        desc_l = MDLabel(
            text=desc,
            theme_text_color='Custom', text_color=TEXT2,
            font_style='Caption',
            halign='center', valign='top'
        )
        desc_l.bind(size=desc_l.setter('text_size'))

        tile.add_widget(icon_l)
        tile.add_widget(name_l)
        tile.add_widget(desc_l)

        def on_release(*_):
            self.switch_tab(screen)
        tile.bind(on_release=on_release)
        return tile

    def _update_home_status(self, *_):
        lbl  = self.root.ids.home_status
        wave = self.root.ids.home_wave
        if _engine.is_playing:
            lbl.text       = f'▶  {_engine.current_freq:.2f} Hz'
            lbl.text_color = TEAL
            wave.wave_color = [*TEAL[:3], 1]
            wave.active    = True
        else:
            lbl.text       = 'Nothing playing'
            lbl.text_color = TEXT2
            wave.active    = False

    # ══════════════════════════════════════════════════════════════════════════
    #  CUSTOM GENERATOR
    # ══════════════════════════════════════════════════════════════════════════
    def _wire_custom(self, ids):
        ids.freq_slider.bind(value=self._on_freq_slider)
        ids.freq_input.bind(text=self._on_freq_text)
        ids.vol_slider.bind(value=self._on_volume)
        ids.play_btn.bind(on_release=self._custom_play)
        ids.stop_btn.bind(on_release=self._custom_stop)
        self._build_presets(ids)

    def _build_presets(self, ids):
        grid = ids.preset_grid
        for p in PRESETS:
            btn = Button(
                text=f"{p['freq']} Hz\n{p['name'].split()[0]}",
                font_size=sp(10),
                background_normal='', background_color=(0, 0, 0, 0),
                color=TEXT2
            )
            with btn.canvas.before:
                Color(*BORDER)
                rr = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(8)])
            btn.bind(
                pos=lambda b, _, rr=rr: setattr(rr, 'pos', b.pos),
                size=lambda b, _, rr=rr: setattr(rr, 'size', b.size),
                on_release=lambda b, freq=p['freq']: self._set_custom_freq(freq)
            )
            grid.add_widget(btn)

    def _on_freq_text(self, instance, value):
        try:
            freq = float(value)
            ids  = self.root.ids
            ids.freq_display.text  = f'{freq:.2f} Hz'
            ids.freq_slider.value  = max(20.0, min(2000.0, freq))
        except ValueError:
            pass

    def _on_freq_slider(self, instance, value):
        ids = self.root.ids
        ids.freq_input.text       = f'{value:.1f}'
        ids.freq_display.text     = f'{value:.2f} Hz'

    def _on_volume(self, instance, value):
        _engine.set_volume(value)
        self.root.ids.vol_pct.text = f'{int(value * 100)}%'

    def _set_custom_freq(self, freq):
        ids = self.root.ids
        ids.freq_input.text   = str(freq)
        ids.freq_display.text = f'{freq:.2f} Hz'
        ids.freq_slider.value = max(20.0, min(2000.0, float(freq)))

    def _custom_play(self, *_):
        try:
            freq = float(self.root.ids.freq_input.text)
            _engine.play(freq)
            self.root.ids.custom_wave.wave_color = [*TEAL[:3], 1]
            self.root.ids.custom_wave.active     = True
        except ValueError:
            pass

    def _custom_stop(self, *_):
        _engine.stop()
        self.root.ids.custom_wave.active = False

    # ══════════════════════════════════════════════════════════════════════════
    #  SOLFEGGIO
    # ══════════════════════════════════════════════════════════════════════════
    def _build_solfeggio(self, ids):
        container = ids.solfeggio_cards
        for data in SOLFEGGIO:
            card = FrequencyCard(
                data=data, engine=_engine,
                on_play_callback=self._on_solfeggio_play
            )
            self._sol_cards.append(card)
            container.add_widget(card)

    def _on_solfeggio_play(self, active_card):
        for c in self._sol_cards:
            if c is not active_card:
                c.force_stop()
        freq  = active_card._data['freq']
        color = get_color_from_hex(active_card._data['color'])
        ids   = self.root.ids
        ids.solfeggio_status.text       = f'▶  {freq} Hz  —  {active_card._data["benefit"]}'
        ids.solfeggio_status.text_color = color
        ids.solfeggio_wave.wave_color   = [*color[:3], 1]
        ids.solfeggio_wave.active       = True

    # ══════════════════════════════════════════════════════════════════════════
    #  CHAKRA
    # ══════════════════════════════════════════════════════════════════════════
    def _build_chakra(self, ids):
        self._build_chakra_spine(ids.chakra_spine)
        container = ids.chakra_cards
        for data in CHAKRA:
            card = FrequencyCard(
                data=data, engine=_engine,
                on_play_callback=self._on_chakra_play
            )
            self._cha_cards.append(card)
            container.add_widget(card)

    def _build_chakra_spine(self, spine):
        for ch in CHAKRA:
            col = get_color_from_hex(ch['color'])
            dot = BoxLayout(orientation='vertical')
            with dot.canvas:
                Color(*col[:3], 0.85)
                e = Ellipse(size=(dp(30), dp(30)), pos=dot.pos)

            def upd(inst, _, e=e):
                e.pos = (inst.center_x - dp(15), inst.center_y - dp(15))

            dot.bind(pos=upd, size=upd)
            dot.add_widget(Label(text=ch['symbol'], font_size=sp(12), color=TEXT1))
            spine.add_widget(dot)

    def _on_chakra_play(self, active_card):
        for c in self._cha_cards:
            if c is not active_card:
                c.force_stop()
        freq  = active_card._data['freq']
        name  = active_card._data['name']
        color = get_color_from_hex(active_card._data['color'])
        ids   = self.root.ids
        ids.chakra_status.text       = f'▶  {name}  ·  {freq} Hz'
        ids.chakra_status.text_color = color
        ids.chakra_wave.wave_color   = [*color[:3], 1]
        ids.chakra_wave.active       = True

    # ══════════════════════════════════════════════════════════════════════════
    #  MUSICAL NOTES
    # ══════════════════════════════════════════════════════════════════════════
    def _build_notes(self, ids):
        # Wire tuning toggles
        ids.btn_440.bind(on_release=lambda *_: self._set_tuning(440.0))
        ids.btn_432.bind(on_release=lambda *_: self._set_tuning(432.0))

        # Wire note-type filters
        ids.filter_all.bind(    on_release=lambda *_: self._set_note_filt('all'))
        ids.filter_natural.bind(on_release=lambda *_: self._set_note_filt('natural'))
        ids.filter_sharps.bind( on_release=lambda *_: self._set_note_filt('sharps'))

        # Wire octave filters
        ids.oct_all.bind(on_release=lambda *_: self._set_oct_filt('all'))
        for n in [3, 4, 5, 6]:
            ids[f'oct_{n}'].bind(
                on_release=lambda b, v=str(n): self._set_oct_filt(v)
            )

        self._rebuild_notes_grid()

    def _set_tuning(self, tuning: float):
        if tuning == self._tuning:
            return
        self._tuning = tuning
        self._rebuild_notes_grid()

    def _set_note_filt(self, filt: str):
        self._note_filt = filt
        self._rebuild_notes_grid()

    def _set_oct_filt(self, filt: str):
        self._oct_filt = filt
        self._rebuild_notes_grid()

    def _rebuild_notes_grid(self):
        _engine.stop()
        for c in self._note_cards:
            c.force_stop()
        self._note_cards.clear()

        ids  = self.root.ids
        grid = ids.notes_grid
        grid.clear_widgets()

        notes = get_notes(self._tuning)

        if self._note_filt == 'natural':
            notes = [n for n in notes if n['is_natural']]
        elif self._note_filt == 'sharps':
            notes = [n for n in notes if not n['is_natural']]

        if self._oct_filt != 'all':
            oct_n = int(self._oct_filt)
            notes = [n for n in notes if n['octave'] == oct_n]

        tuning_str = f'{int(self._tuning)} Hz'
        ids.notes_status.text       = f'A4 = {tuning_str}  ·  {len(notes)} notes shown'
        ids.notes_status.text_color = GOLD if self._tuning == 432.0 else PINK

        wave_col = GOLD if self._tuning == 432.0 else PINK
        ids.notes_wave.wave_color = [*wave_col[:3], 1]
        ids.notes_wave.active     = False

        for data in notes:
            card = NoteCard(
                data=data, engine=_engine,
                on_play_callback=self._on_note_play
            )
            self._note_cards.append(card)
            grid.add_widget(card)

    def _on_note_play(self, active_card):
        for c in self._note_cards:
            if c is not active_card:
                c.force_stop()
        d     = active_card._data
        color = get_color_from_hex(d['color'])
        ids   = self.root.ids
        ids.notes_status.text       = f'▶  {d["full"]}  —  {d["freq_str"]} Hz'
        ids.notes_status.text_color = color
        ids.notes_wave.wave_color   = [*color[:3], 1]
        ids.notes_wave.active       = True

    # ── Cleanup ───────────────────────────────────────────────────────────────
    def on_stop(self):
        _engine.stop()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    SoundHealerApp().run()
