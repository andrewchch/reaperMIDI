import time
import rtmidi
import sys

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

with midiout:
    # channel 1, middle C, velocity 112
    note_on = [0x90, 60, 112]
    note_off = [0x80, 60, 0]
    midiout.send_message(note_on)
    time.sleep(0.5)
    midiout.send_message(note_off)
    time.sleep(0.1)

del midiout
