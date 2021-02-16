import base64
from base64 import encode
import tkinter as tk
import tkinter.messagebox # ignore unused import warn
import threading
import os

def base64_btm(encode: bool) -> None:
    print('2')
    process_thread = threading.Thread(target=base64_process, args=(encode,))
    process_thread.start()

def base64_process(encode: bool) -> None:
    print('3')
    btm_encode.config(state='disabled')
    btm_decode.config(state='disabled')
    text = text_box.get(1.0, 'end').strip('\n')
    try:
        if encode:
            result = base64.encodebytes(text.encode()).decode()
        else:
            result = base64.b64decode(text.encode()).decode()
    except Exception:
        tk.messagebox.showerror('Error','Tried to Encode/Decode, but failed.')
        # tk.messagebox.showwarning('Donald Trump Warning','Be smarter next time, you fool like the President!')
        btm_encode.config(state='normal')
        btm_decode.config(state='normal')
        return
    if result == '' and text != '':
        tk.messagebox.showerror('Error','Tried to Encode/Decode, but failed.')
        # tk.messagebox.showwarning('Donald Trump Warning','Be smarter next time, you fool like the President!')
        btm_encode.config(state='normal')
        btm_decode.config(state='normal')
        return
    else:
        text_box.delete(1.0, 'end')
        text_box.insert('end', result.strip('\n'))
        if var_clip.get() == 1:
            pyperclip.copy(result.strip('\n').replace('\n', os.linesep))
        btm_encode.config(state='normal')
        btm_decode.config(state='normal')


if __name__ == "__main__":
    global trump_counter

    root_win = tk.Tk()
    root_win.title('Base64 GUI')
    frame_text_box = tk.Frame()
    text_box = tk.Text(frame_text_box, show=None, font=('Arial', 10), wrap='word', height=10, width=50)
    text_box.pack(side='left', expand=True, fill='both')
    sb_text_box = tk.Scrollbar(frame_text_box, orient="vertical")
    sb_text_box.config(command=text_box.yview)
    sb_text_box.pack(side='right', fill='y')
    text_box.config(yscrollcommand=sb_text_box.set)
    frame_text_box.pack(expand=True, side='top', fill='both', padx=20, pady=20)

    frame_cb = tk.Frame()
    var_clip = tk.IntVar()
    cb = tk.Checkbutton(frame_cb, text="Clipboard", variable=var_clip)
    try:
        import pyperclip
        var_clip.set(1)
    except ImportError:
        cb.config(state='disabled')

    cb.pack()
    frame_cb.pack(side='top')

    frame_btm = tk.Frame()
    btm_encode = tk.Button(frame_btm, text='Encode', command=lambda: base64_btm(True))
    btm_decode = tk.Button(frame_btm, text='Decode', command=lambda: base64_btm(False))
    btm_encode.pack(side='left', padx=5)
    btm_decode.pack(side='left', padx=5)
    frame_btm.pack(side='top', padx=10, pady=10)

    root_win.update()
    root_win.minsize(root_win.winfo_width(), root_win.winfo_height())
    root_win.mainloop()
