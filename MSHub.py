import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import numpy as np
import os
import glob 
import shutil
import PIL
from PIL import *
import time
from threading import *
import math
import subprocess


minecraft_version = "1.19.3"


output_stream = os.popen("whoami")


username = output_stream.read()[:-1]



#selection = input("pack: ")
selection = "Kori_Pack"

dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

def load_textures(asset):
    
    images = []
    for path in os.listdir(dir_path + asset):
        if path.endswith(".png"):
            images.append(path)
    
    return images

window = tk.Tk()

window.title("MSHub")

window.geometry("800x500")
window.minsize(800, 500)
window.maxsize(800, 500)

text = tk.Text(window, bg = 'lightgrey')
text.pack(side="left")
text.place(x=0, y=80, width= 384, height= 460)

textr = tk.Text(window, bg = 'lightgrey')
textr.pack(side="left")
textr.place(x=400, y=80, width= 384, height= 460)

def yview(*args):
    text.yview(*args)
    textr.yview(*args)

sb = tk.Scrollbar(window, command=yview)
sb.pack(side="right")
text.configure(yscrollcommand=sb.set)

photos = []
buttons = []
types = os.listdir(dir_path)
ctype = types[0]



header_button_size = math.ceil(800/len(types))*2


threads = []

def startGimp(tipe, texet):
    threads.append(Thread(target=openGimp(tipe, texet)))

    for x in threads:
        x.start()
        x.join()

def openGimp(tp, txt):
    os.system("gimp "+ dir_path + tp + txt)






def build_button(type, img):
    global photos
    photo = tk.PhotoImage(file = dir_path + type + img).zoom(4)
    photoimage = photo.subsample(1, 1)
    photos.append(photoimage)

    return tk.Button(window, text=img[:-4].replace(type, ''), height=80, width=350, bg='white', image=photoimage, command=lambda: startGimp(type, img), compound = LEFT)


buttons = []
header_buttons = []

#print(load_textures(ctype))

def build_buttons_list():
    for i in range(len(load_textures(ctype))):
        buttons.append(build_button(ctype + "/", load_textures(ctype)[i]))
        if (i % 2) == 0:
            text.window_create("end", window=buttons[i])
            text.insert("end", "\n")
        else:
            textr.window_create("end", window=buttons[i])
            textr.insert("end", "\n")
            #buttons[i].grid(row = i, column = 0, sticky = W, pady = 2)

    text.config(state=DISABLED)
    text.pack_forget()
    textr.config(state=DISABLED)
    textr.pack_forget() 

def changeType(ih):
    global ctype
    global buttons
    ctype = ih
    for v in buttons:
        v.destroy()

    buttons = []

    build_buttons_list()

def build_type_button(option):
    return tk.Button(window, text=option, bg='grey', command=lambda: changeType(option), compound = LEFT)
    


def build_header():
    u = 0
    row_swtch = False

    for a in range(len(types)):
        
        header_buttons.append(build_type_button(types[a]))
        header_buttons[a].pack(side="left")
        if a  < len(types)/2 and row_swtch == False:
            header_buttons[a].place(x=u*header_button_size, y=0, width= header_button_size, height= 40)
            u = u + 1
        else:
            if row_swtch == False:
                u = 0
            row_swtch = True
            header_buttons[a].place(x=u*header_button_size, y=40, width= header_button_size, height= 40)
            u = u + 1

build_buttons_list()
build_header()


print("starting main loop")
window.mainloop()