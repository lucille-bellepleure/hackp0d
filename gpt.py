import subprocess
import pulsectl
from tkinter import *

# the Spotify track URIs to play
track_uris = ['spotify:track:4iV5W9uYEdYUVa79Axb7Rh', 'spotify:track:3eZEiV7w8Q0MVjVXRvvZtX', 'spotify:track:3qXpX7tK4fNkwJF8Y4WtSA']

# start Raspotify as a subprocess
raspotify_process = subprocess.Popen(['raspotify', '--backend', 'pipe', '--onevent', 'python /path/to/your/program.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# create a PulseAudio client
pulse = pulsectl.Pulse('raspotify-client')

# set the default sink to the Bluetooth speaker
default_sink = pulse.sink_list()[1] # adjust index as needed
pulse.default_set(default_sink)

# create the Tkinter window
root = Tk()
root.title('Raspotify')

# create a header label
header_label = Label(root, text='Raspotify', font=('Courier', 16), fg='green', bg='black')
header_label.pack(side=TOP, fill=X)

# create a listbox to display the track options
track_listbox = Listbox(root, font=('Courier', 14), fg='green', bg='black', selectmode=SINGLE, highlightcolor='green', highlightbackground='green')
for track_uri in track_uris:
    track_listbox.insert(END, track_uri)
track_listbox.pack(side=TOP, fill=BOTH, expand=YES)

# create a play button to start the playback
def play_track():
    selection = track_listbox.curselection()
    if selection:
        track_uri = track_uris[selection[0]]
        raspotify_process.stdin.write(f'play {track_uri}\n'.encode())

play_button = Button(root, text='Play', font=('Courier', 14), fg='green', bg='black', command=play_track)
play_button.pack(side=TOP, pady=10)

# create a stop button to stop the playback
def stop_track():
    raspotify_process.stdin.write(b'stop\n')

stop_button = Button(root, text='Stop', font=('Courier', 14), fg='green', bg='black', command=stop_track)
stop_button.pack(side=TOP, pady=10)

# run the Tkinter event loop
root.mainloop()

# reset the default sink to the internal speakers
default_sink = pulse.sink_list()[0] # adjust index as needed
pulse.default_set(default_sink)
