import pyperclip
import time
import os

def log(log_str: str):
    print(log_str)

if __name__ == "__main__":
    old_clip = pyperclip.paste()
    while True:
        try: 
            time.sleep(1)
            new_clip = pyperclip.paste()
            if new_clip != old_clip:
                text_list = new_clip.split(os.linesep)
                text = ''
                for i in range(0, len(text_list)):
                    text_list[i] = text_list[i].strip(' ')
                    text += text_list[i]
                    text += ' '
                print('[PDF HELPER] {} lineseps removed'.format(str(len(text_list) - 1)))
                pyperclip.copy(text.replace('\n', os.linesep))
                old_clip = pyperclip.paste()
        except Exception:
            continue
