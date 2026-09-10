"""Reference-song playback through the real FCEUmm APU and controller interface."""
import json
import struct
import retro_harness as h
from play_helpers import read as r, start_from_intro
from generate_music import midi

report = []

def check(ok, label):
    line = ('PASS ' if ok else 'FAIL ') + label
    report.append(line); print(line, flush=True)
    (h.root / 'build/reference-music-tests.txt').write_text('\n'.join(report) + '\n')
    assert ok, label

scores = json.loads((h.root / 'assets/song-arrangements.json').read_text(encoding='utf-8'))['scores']

for score, track, tempo in zip(scores, [0, 2], [18, 15]):
    h.core.retro_reset(); h.frames(90)
    if track:
        h.press(7); h.press(8); start_from_intro()
    check(r('music_track') == track, score['id'] + ' selects its reference arrangement')
    for _ in range(600):
        if r('song_step') == 0 and r('song_tick') == 0: break
        h.frames(1)
    else: raise AssertionError('No loop boundary')
    expected = []
    for note, duration in score['lead_sixteenths']:
        expected.extend([0 if note == 'R' else midi(note) - 35] * duration)
    h.audio_samples.clear(); h.capture_audio = True
    bad_pitch = bad_clock = 0
    cycles = []
    for loop in range(3):
        state = []
        for frame in range(tempo * 32):
            tick, step = r('song_tick'), r('song_step')
            bad_clock += (step, tick) != (frame // tempo, frame % tempo)
            h.frames(1)
            pitch = r('reference_pitch')
            bad_pitch += pitch != expected[step * 2 + (tick >= tempo // 2)]
            state.append(pitch)
        cycles.append(state)
    h.capture_audio = False
    check(not bad_clock, score['id'] + ' repeats exactly every four bars without clock drift')
    check(not bad_pitch, score['id'] + ' plays the entire scored phrase, including sixteenth notes and rests')
    check(cycles[0] == cycles[1] == cycles[2], score['id'] + ' preserves every note over three loop boundaries')
    samples = struct.unpack('<' + 'h' * (len(h.audio_samples) // 2), h.audio_samples)
    check(len(samples) > 100000 and max(map(abs, samples)) > 100, score['id'] + ' produces audible emulator PCM')
    check(max(map(abs, samples)) < 32767, score['id'] + ' PCM has no full-scale clipping')
    check(r('misses') == 0 and not r('paused'), score['id'] + ' playback does not consume gameplay input')
h.close()
