import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Generate Chord Progression",
    page_icon="🎵"
)

st.title("MIDI Melody Player")

sample_rate = 44_100
bpm = 72

notes = [
    48, 52, 57, 59, 52, 59, 60, 52, 60, 57, 53,
    50, 52, 48, 45, 48, 52, 48, 45, 43, 45, 45
]

durations = [
    0.5, 0.5, 0.5, 1, 0.5, 0.5, 1,
    0.5, 0.5, 0.5, 0.5, 1, 0.25, 0.25,
    0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.5, 1.5
]


def make_note(midi_note, beats):
    seconds = beats * 60 / bpm

    t = np.arange(
        int(seconds * sample_rate)
    ) / sample_rate

    frequency = 440 * 2 ** ((midi_note - 69) / 12)

    sound = np.sin(
        2 * np.pi * frequency * t
    )

    fade_samples = min(
        int(0.01 * sample_rate),
        len(sound) // 2
    )

    envelope = np.ones_like(sound)

    if fade_samples > 0:
        envelope[:fade_samples] = np.linspace(
            0,
            1,
            fade_samples
        )

        envelope[-fade_samples:] = np.linspace(
            1,
            0,
            fade_samples
        )

    return sound * envelope


def generate_audio():
    return np.concatenate([
        make_note(midi_note, beats)
        for midi_note, beats in zip(
            notes,
            durations,
            strict=True
        )
    ])


if st.button("Generate and play audio"):
    audio = generate_audio()

    st.audio(
        audio,
        sample_rate=sample_rate
    )

# #Modify tempo
# bpm = st.slider(
#     "Tempo",
#     min_value=40,
#     max_value=180,
#     value=72
# )