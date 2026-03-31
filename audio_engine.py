"""
SoundHealer Audio Engine
Generates precise sine-wave tones at exact frequencies.
Uses Android AudioTrack (via pyjnius) on device, sounddevice on desktop.
Phase is preserved across chunks to eliminate clicks/discontinuities.
"""

import numpy as np
import threading
import time
import math


SAMPLE_RATE = 44100   # Hz — CD quality
CHANNELS = 1          # Mono (sufficient for pure tones)
BIT_DEPTH = 16        # 16-bit PCM


class FrequencyEngine:

    def __init__(self):
        self.sample_rate   = SAMPLE_RATE
        self.volume        = 0.70          # 0.0 – 1.0
        self.is_playing    = False
        self.current_freq  = 0.0

        self._stop_event   = threading.Event()
        self._thread       = None
        self._phase        = 0.0           # continuous phase accumulator (radians)

        self._backend      = self._detect_backend()

    # ------------------------------------------------------------------ #
    # Backend detection
    # ------------------------------------------------------------------ #
    def _detect_backend(self):
        """Return 'android', 'sounddevice', or 'wave_file'."""
        try:
            from jnius import autoclass  # noqa
            autoclass('android.media.AudioTrack')
            return 'android'
        except Exception:
            pass
        try:
            import sounddevice as sd  # noqa
            return 'sounddevice'
        except Exception:
            pass
        return 'wave_file'

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def play(self, frequency: float):
        """Start playing the given frequency (Hz). Stops any current tone."""
        self.stop()
        if frequency <= 0:
            return
        self.current_freq  = frequency
        self._phase        = 0.0
        self._stop_event.clear()
        self.is_playing    = True

        target = {
            'android':     self._stream_android,
            'sounddevice': self._stream_sounddevice,
            'wave_file':   self._stream_wave_file,
        }[self._backend]

        self._thread = threading.Thread(target=target, args=(frequency,), daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the currently playing tone immediately."""
        self._stop_event.set()
        self.is_playing   = False
        self.current_freq = 0.0
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.5)
        self._thread = None

    def set_volume(self, volume: float):
        """Set playback volume. 0.0 = silent, 1.0 = full."""
        self.volume = max(0.0, min(1.0, volume))

    # ------------------------------------------------------------------ #
    # Sample generation (phase-continuous)
    # ------------------------------------------------------------------ #
    def _generate_chunk(self, frequency: float, n_samples: int) -> np.ndarray:
        """
        Return n_samples of a sine wave at `frequency` Hz as int16.
        The internal phase accumulator ensures seamless chunk concatenation
        — no pops, no clicks, no pitch artifacts.
        """
        indices = np.arange(n_samples, dtype=np.float64)
        phase_inc = 2.0 * math.pi * frequency / self.sample_rate

        # Phase of each sample relative to the current accumulator
        phases  = self._phase + phase_inc * indices
        samples = np.sin(phases) * self.volume

        # Advance the accumulator, keep in [0, 2π) to avoid float drift
        self._phase = (self._phase + phase_inc * n_samples) % (2.0 * math.pi)

        return (samples * 32767.0).astype(np.int16)

    # ------------------------------------------------------------------ #
    # Android backend — AudioTrack streaming
    # ------------------------------------------------------------------ #
    def _stream_android(self, frequency: float):
        try:
            from jnius import autoclass
            AudioTrack  = autoclass('android.media.AudioTrack')
            AudioFormat = autoclass('android.media.AudioFormat')
            AudioManager = autoclass('android.media.AudioManager')

            buf_size = AudioTrack.getMinBufferSize(
                self.sample_rate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
            )
            # Use 4× min buffer to avoid underruns
            buf_size = max(buf_size * 4, 4096)

            track = AudioTrack(
                AudioManager.STREAM_MUSIC,
                self.sample_rate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
                buf_size,
                AudioTrack.MODE_STREAM,
            )
            track.play()

            chunk_samples = buf_size // 2  # 2 bytes per int16 sample

            while not self._stop_event.is_set():
                pcm = self._generate_chunk(frequency, chunk_samples)
                raw = pcm.tobytes()
                track.write(raw, 0, len(raw))

            # Fade out to prevent click on stop
            fade_len = min(self.sample_rate // 10, chunk_samples)
            fade = (np.linspace(1.0, 0.0, fade_len) *
                    np.sin(np.linspace(0, 2 * math.pi, fade_len))).astype(np.float32)
            silent = (fade * 0).astype(np.int16)
            track.write(silent.tobytes(), 0, len(silent.tobytes()))

            track.stop()
            track.release()
        except Exception as e:
            print(f"[AudioEngine] Android error: {e}")
            self.is_playing = False

    # ------------------------------------------------------------------ #
    # sounddevice backend (desktop)
    # ------------------------------------------------------------------ #
    def _stream_sounddevice(self, frequency: float):
        try:
            import sounddevice as sd

            chunk_samples = self.sample_rate // 10   # 100 ms chunks

            def callback(outdata, frames, time_info, status):
                if self._stop_event.is_set():
                    outdata[:] = 0
                    raise sd.CallbackStop()
                pcm = self._generate_chunk(frequency, frames)
                outdata[:, 0] = pcm.astype(np.float32) / 32767.0

            with sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                callback=callback,
                blocksize=chunk_samples,
            ):
                while not self._stop_event.is_set():
                    time.sleep(0.05)

        except Exception as e:
            print(f"[AudioEngine] sounddevice error: {e}")
            self.is_playing = False

    # ------------------------------------------------------------------ #
    # Fallback: write WAV to temp file, loop-play via Kivy SoundLoader
    # ------------------------------------------------------------------ #
    def _stream_wave_file(self, frequency: float):
        import wave, tempfile, os
        try:
            from kivy.core.audio import SoundLoader
        except Exception:
            print("[AudioEngine] No audio backend available.")
            self.is_playing = False
            return

        duration = 5.0   # seconds per WAV file (looped)
        n_samples = int(self.sample_rate * duration)
        pcm = self._generate_chunk(frequency, n_samples)

        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        with wave.open(tmp.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm.tobytes())

        sound = SoundLoader.load(tmp.name)
        if sound:
            sound.loop  = True
            sound.volume = self.volume
            sound.play()

            while not self._stop_event.is_set():
                time.sleep(0.1)

            sound.stop()
            sound.unload()
        os.unlink(tmp.name)
        self.is_playing = False
