from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
import random
import time
import sys
import os

bomb_x = ""
bomb_y = ""
delays = [0.03, 0.04, 0.05, 0.06, 0.4]
long_words = True
instant_typing = False
pyautogui.PAUSE = 0
used_words = set()

word_file_path = ''#path of ur worldlist | chemin d'accès de ta worldlist
if not os.path.exists(word_file_path):
    print("Le fichier de mots n'existe pas.")
    sys.exit(1)

with open(word_file_path) as word_file:
    valid_words = word_file.read().split()

used_words_file_path = 'used_words.txt'
if os.path.exists(used_words_file_path):
    with open(used_words_file_path) as used_file:
        used_words = set(used_file.read().split())

def save_used_words():
    with open(used_words_file_path, 'w') as used_file:
        used_file.write('\n'.join(used_words))

def release(key):
    global bomb_x, bomb_y, used_words
    if key == Key.f8:
        try:
            bomb_x, bomb_y = pyautogui.position()
        except Exception as err:
            print(f"Erreur lors de l'obtention de la position de la souris : {err}")
    if key == Key.f9:
        try:
            pyautogui.click(x=bomb_x, y=bomb_y, clicks=2)
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')
            pyautogui.click(x=bomb_x - 100, y=bomb_y)
            time.sleep(0.1)
            syllable = pyperclip.paste().lower().strip()
            pyperclip.copy('')
            
            found_words = [word for word in valid_words if syllable in word]
            
            if not found_words:
                print("Aucun mot trouvé.")
                return

            if long_words:
                found_words.sort(key=len, reverse=True)

            for word in found_words:
                if word not in used_words:
                    final_word = word
                    used_words.add(final_word)
                    save_used_words()  
                    
                    if instant_typing:
                        pyperclip.copy(final_word)
                        with pyautogui.hold('ctrl'):
                            pyautogui.press('v')
                    else:
                        for char in final_word:
                            delay = random.choice(delays)
                            pyautogui.write(char, delay)
                    time.sleep(0.1)
                    pyautogui.press('enter')
                    return

            print("Tous les mots ont été utilisés.")
        except Exception as e:
            print(f"Erreur : {e}")

with Listener(on_release=release) as listener:
    listener.join()