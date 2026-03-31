[app]

# ── Identity ──────────────────────────────────────────────────────────────────
title           = SoundHealer
package.name    = soundhealer
package.domain  = org.soundhealer
version         = 1.0.0
source.dir      = .
source.exclude_dirs = Appvenv, __pycache__
source.include_exts = py,png,jpg,kv,atlas,wav

# ── Entry point ───────────────────────────────────────────────────────────────
# main.py is used automatically by Buildozer when present in source.dir

# ── Python requirements ───────────────────────────────────────────────────────
# numpy  : waveform generation (must be listed here; compiled for Android)
# kivy   : UI framework (automatically included)
requirements = python3,kivy==2.2.1,kivymd==1.2.0,numpy

# ── Android permissions ───────────────────────────────────────────────────────
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS

# ── Orientation & display ─────────────────────────────────────────────────────
orientation = portrait
fullscreen   = 0

# ── Android build settings ────────────────────────────────────────────────────
android.minapi     = 21
android.targetapi  = 33
android.ndk        = 25b
android.sdk        = 33
android.archs      = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

# ── Icons & splash (replace with your own 512×512 and 1024×500 images) ────────
# icon.filename     = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

# ── Log level ─────────────────────────────────────────────────────────────────
log_level = 2

# ── p4a (python-for-android) branch ──────────────────────────────────────────
p4a.branch = master


[buildozer]
log_level = 2
warn_on_root = 1
