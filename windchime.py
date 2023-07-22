import time
import rtmidi
import sys
import random

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

print(available_ports)

port_num = None
for port in available_ports:
    if port.startswith('loopMIDI Port'):
        port_num = int(port.split(' ')[-1])
        print('Found port: %s' % port)
        break

if port_num is None:
    print('No loopMidi port found')
    sys.exit(1)

midiout.open_port(port_num)

# Define the C Major scale (middle octave) in MIDI note numbers
c_major = [60, 62, 64, 65, 67, 69, 71]

# Time delay ranges (in seconds) between notes to simulate random wind
delay_min, delay_max = 0.5, 2.0

try:
    while True:
        # Pick a random note from the scale
        note = random.choice(c_major)

        # Velocity and duration can also be randomized for a more natural feel
        velocity = random.randint(50, 100)  # MIDI note velocity (volume)
        duration = random.uniform(0.5, 1.5)  # Note duration in seconds

        # Send the NoteOn event
        midiout.send_message([0x90, note, velocity])
        time.sleep(duration)

        # Send the NoteOff event for the same note
        midiout.send_message([0x80, note, 0])

        # Wait a random amount of time before the next note
        time.sleep(random.uniform(delay_min, delay_max))

except KeyboardInterrupt:
    del midiout
