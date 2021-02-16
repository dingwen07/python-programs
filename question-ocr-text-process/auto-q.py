import time
import tkinter as tk
import tkinter.messagebox
import os
import threading
import qprocess

clipboard_enabled = True
try:
    import pyperclip 
except ImportError:
    print('pyperclip not installed, clipboard feature disabled')
    clipboard_enabled = False


def pcs(text_box):
    text = text_box.get(1.0, 'end').strip('\n')
    qresult = qprocess.question_process(text)
    text = qresult[0]
    if qresult[1]:
        warn_msg = ''
        for _warn_msg in qresult[2]:
            warn_msg += _warn_msg + '\n'
        tkinter.messagebox.showwarning('Warning', warn_msg)
    text_box.delete(1.0, 'end')
    text_box.insert('end', text)
    if clipboard_enabled:
        pyperclip.copy(text.replace('\n', os.linesep))
    text_box.tag_add('sel', "1.0", 'end')
    text_box.focus_set()

def clip_monitor(text_box):
    old_clip = pyperclip.paste()
    while True:
        time.sleep(1)
        new_clip = pyperclip.paste()
        if new_clip != old_clip:
            text = text_box.get(1.0, 'end').strip('\n')
            if len(new_clip) > 16 and text.replace('\n', os.linesep) != new_clip.strip('\n'):
                text_box.delete(1.0, 'end')
                text_box.insert('end', new_clip.replace(os.linesep, '\n'))
            old_clip = new_clip


if __name__ == "__main__":
    root_win = tk.Tk()
    text_box = tk.Text(root_win, show=None, font=('Arial', 10), height=12, width=75)
    text_box.pack(expand=True, fill='both')
    btm = tk.Button(root_win, text='OK', command=lambda: pcs(text_box))
    btm.pack(side='bottom', pady=10)

    if clipboard_enabled: 
        t = threading.Thread(target=clip_monitor, args=(text_box,))
        t.daemon = True
        t.start()

    root_win.mainloop()
    exit()
