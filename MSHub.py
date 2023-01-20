import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import numpy as np
import os
import glob 
import shutil
import PIL.Image
from PIL import ImageTk
from PIL import *
import time
from threading import *
import math
import subprocess
import copy
import sys






output_stream = os.popen("whoami")


username = output_stream.read()[:-1]



base_files = ['versions', 'launcher_accounts.json', 'bootstrap_log.txt', 'launcher', 'window_settings_launcher.conf', 'libraries', 'webcache2', 'launcher_msa_credentials.bin', 'assets', 'treatment_tags.json', 'resourcepacks', 'logs', 'launcher_product_state.json', 'runtime', 'launcher_gamer_pics.json', 'window_settings_xal_login.conf', 'launcher_settings.json', 'launcher_cef_log.txt', 'launcher_log.txt', 'launcher_entitlements.json', 'launcher_ui_state.json', 'launcher_profiles.json', 'saves', 'realms_persistence.json']

pack_options = []

def scan_packs():
    global pack_options
    all_packs = os.listdir(f"/home/{username}/.minecraft/")

    pack_options = []

    for f in all_packs:
        if f not in base_files:
            pack_options.append(f)

scan_packs()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



selection = "packnotfound"

#selection = input("pack: ")

if pack_options != []:
    selection = pack_options[0]


minecraft_version = next(os.walk(f"/home/{username}/.minecraft/{selection}/"))[1][0]



print(minecraft_version)

dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

def load_textures(asset):
    
    images = []

    dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

    if selection != "packnotfound":
        for path in os.listdir(dir_path + asset):
            if path.endswith(".png"):
                images.append(path)

    print("loading images")
    
    return images

window = tk.Tk()

window.title("MSHub")

window.configure(bg="#a1a1a1")

window.geometry("800x1000")
window.minsize(800, 800)
window.maxsize(800, 800)

text = tk.Text(window, bg = 'lightgrey')
text.pack(side="left")
text.place(x=0, y=120, width= 384, height= 680)

textr = tk.Text(window, bg = 'lightgrey')
textr.pack(side="left")
textr.place(x=400, y=120, width= 384, height= 680)

def yview(*args):
    text.yview(*args)
    textr.yview(*args)

sb = tk.Scrollbar(window, command=yview)
sb.pack(side="right")
text.configure(yscrollcommand=sb.set)

photos = []
buttons = []
types = ["notapack"]

if selection != "packnotfound":
    types = os.listdir(dir_path)

ctype = types[0]

ccmages = []



header_buttons = []

#print(load_textures(ctype))
ctextures = []

header_button_size = math.ceil(800/(len(types)*0.5))








def callback(selektion):
    global selection
    global minecraft_version
    selection = selektion
    minecraft_version = next(os.walk(f"/home/{username}/.minecraft/{selection}/"))[1][0]
    scan_packs()
    build_buttons_list()
    build_header()





clicked = StringVar()


if pack_options != []:
    clicked.set(pack_options[0])
else:
    clicked.set("No custom texture pack")



pack_drop = tk.OptionMenu(window, clicked, *pack_options, command=callback)


pack_drop.pack(side="right")

pack_drop.place(x=200, y=0, width= 200, height= 40)





def startGimp(tipe, texet):
    Thread(target=openGimp(tipe, texet)).start()
    

def openGimp(tp, txt):

    dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

    if selection != "packnotfound":
        os.system("gimp "+ dir_path + tp + txt)



mag = tk.PhotoImage(file = resource_path("/home/abris/Desktop/Programok/MSHub/magni2.png")).zoom(2)




searchbar = Entry(window, font=('Georgia 30'))

searchbar.pack(side="right")

searchbar.place(x=400, y=0, width=320)

def searchCmd():
    global cutex
    cutex = load_textures(ctype)
    stext = searchbar.get()
    
    cutexer = copy.copy(cutex)
    
    if stext != "":
        for z in range(len(cutex)):
            if stext not in cutex[z]:
                print(len(cutex), cutex[z])
                cutexer.remove(cutex[z])
    cutex = cutexer
    build_buttons_list()
        


searchButton = tk.Button(window, image=mag, command=searchCmd)

searchButton.pack(side="right")

searchButton.place(x=720, y=0, width=80, height=40)


cutex = load_textures(ctype)




def export():
    os.system(f"zip '/home/{username}/.minecraft/{selection}/{minecraft_version}/{selection}.zip' '/home/{username}/.minecraft/{selection}/{minecraft_version}/pack.mcmeta' '/home/{username}/.minecraft/{selection}/{minecraft_version}/assets'")

    os.system(f"cp '/home/{username}/.minecraft/{selection}/{minecraft_version}/{selection}.zip' '/home/{username}/.minecraft/resourcepacks/'")




export_button = tk.Button(window, text="EXPORT", bg="yellow", command=export)

export_button.pack(side="left")

export_button.place(x=0, y=0, width=header_button_size, height=40)




def updatee(event):
    sbcn = searchbar.get()

    if event.keysym == "BackSpace":
        if sbcn == "":
            #build_buttons_list()
            pass

    if event.keysym == "Return":
        searchCmd()
        


def build_button(type, img):
    global photos

    dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"
    
    newsize = (64, 64)
    photo = ImageTk.PhotoImage(PIL.Image.open(dir_path + type + img).resize(newsize, resample=Image.NEAREST))
    photos.append(photo)

    return tk.Button(window, text=img[:-4].replace(type, ''), height=80, width=350, bg="lightgrey", image=photo, command=lambda: startGimp(type, img), compound = LEFT)





def build_buttons_list(): 
    global ctextures
    if selection != "packnotfound":
        ctextures = load_textures(ctype)

        for but in buttons:
            print(but)
            but.destroy()
        buttons.clear()
            
        print(buttons)

        for i in range(len(cutex)):
            buttons.append(build_button(ctype + "/", cutex[i]))
            if (i % 2) == 0:
                text.window_create("end", window=buttons[i])

            else:
                textr.window_create("end", window=buttons[i])
                #buttons[i].grid(row = i, column = 0, sticky = W, pady = 2)

        text.config(state=DISABLED)
        text.pack_forget()
        textr.config(state=DISABLED)
        textr.pack_forget() 

def changeType(ih):
    global ctype
    global buttons
    global cutex
    ctype = ih
    for v in buttons:
        v.destroy()

    buttons = []

    cutex = load_textures(ctype)

    build_buttons_list()

def build_type_button(option):
    return tk.Button(window, text=option, bg='grey', command=lambda: changeType(option), compound = LEFT)
    


def build_header():
    u = 0
    row_swtch = False

    if selection != "packnotfound":
        for a in range(len(types)):
            
            header_buttons.append(build_type_button(types[a]))
            header_buttons[a].pack(side="left")
            if a  < len(types)/2 and row_swtch == False:
                header_buttons[a].place(x=u*header_button_size, y=40, width= header_button_size, height= 40)
                u = u + 1
            else:
                if row_swtch == False:
                    u = 0
                row_swtch = True
                header_buttons[a].place(x=u*header_button_size, y=80, width= header_button_size, height= 40)
                u = u + 1

build_buttons_list()
build_header()


print("starting main loop")



window.bind("<KeyRelease>", updatee)
mainLoop = Thread(target=window.mainloop())
mainLoop.start()

