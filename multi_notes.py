import asyncio
import random
import rtmidi
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON
import keyboard

class MidiGenerator:
    def __init__(self, port_name):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        if available_ports:
            try:
                self.midiout.open_port(available_ports.index(port_name))
            except ValueError:
                print("Port not found, creating a new one.")
                self.midiout.open_virtual_port(port_name)

    async def play_note(self, note, velocity, duration, start_time):
        await asyncio.sleep(start_time)

        # Send Note On message
        self.midiout.send_message([NOTE_ON, note, velocity])

        await asyncio.sleep(duration)

        # Send Note Off message
        self.midiout.send_message([NOTE_OFF, note, 0])

    def generate_notes(self, num_notes, interval):
        notes = []
        start_time = 0.0

        # MIDI numbers for the C Major scale in the 4th octave
        c_major_scale = [60, 62, 64, 65, 67, 69, 71]
        start_multipliers = [1, 2, 4]
        duration_multipliers = [2, 4, 8]

        for _ in range(num_notes):
            note = random.choice(c_major_scale)  # Select a random note from the C Major scale
            velocity = random.randint(50, 100)  # MIDI velocity range from 0 to 127
            duration = interval * random.choice(duration_multipliers)  # Duration in seconds
            notes.append((note, velocity, duration, start_time))

            start_time += interval * random.choice(start_multipliers)  # Increase start time by the defined interval

        return notes

    def add_note_on_keydown(self, notes, interval):
        note = random.choice([60, 62, 64, 65, 67, 69, 71])  # Select a random note from the C Major scale
        velocity = random.randint(50, 100)  # MIDI velocity range from 0 to 127
        duration = random.uniform(0.1, 1)  # Duration in seconds
        start_time = len(notes) * interval

        notes.append((note, velocity, duration, start_time))

# Using the script
midi_gen = MidiGenerator("loopMIDI Port 1")  # Replace with your MIDI port name

notes = midi_gen.generate_notes(100, 0.5)  # Generate 100 notes with 0.4 second intervals

# Bind the spacebar keydown event to the add_note_on_keydown function
keyboard.on_press_key("space", lambda _: midi_gen.add_note_on_keydown(notes, 0.4))

# Schedule each note
loop = asyncio.get_event_loop()
tasks = [loop.create_task(midi_gen.play_note(*note)) for note in notes]
loop.run_until_complete(asyncio.gather(*tasks))

