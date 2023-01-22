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
import zipfile






output_stream = os.popen("whoami")


username = output_stream.read()[:-1]






base_files = ["assets", "launcher", "resourcepacks", "server-resource-packs", "bin", "libraries", "runtime", "shaderpacks", "crash-reports", "logs", "saves", "versions", "profilekeys", "screenshots", "webcache2"]


pack_options = []
types = ["notapack"]

def scan_packs():
    global pack_options
    print("scanning packs")
    all_packs = next(os.walk(f"/home/{username}/.minecraft/"))[1]

    pack_options = []

    for f in all_packs:
        if f not in base_files:
            pack_options.append(f)


scan_packs()


selection = "packnotfound"


#selection = input("pack: ")

if pack_options != []:
    selection = pack_options[0]



minecraft_version =  0

for z in next(os.walk(f"/home/{username}/.minecraft/versions/"))[1]:
    if "." in z:
        minecraft_version = z



print(minecraft_version)


print(minecraft_version)

#########################################################################################

dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

def create_first():
    global types
    global selection
    global dir_path

    if selection == "packnotfound":

        pname = f"{username}_texture_pack"


        os.system(f"mkdir '/home/{username}/.minecraft/{pname}'")
        os.system(f"cp '/home/{username}/.minecraft/versions/{minecraft_version}/{minecraft_version}.jar' '/home/{username}/.minecraft/{pname}'")


        os.chdir(f"/home/{username}/.minecraft/{pname}/")


        os.system(f"mkdir '/home/{username}/.minecraft/{pname}/{minecraft_version}'")

        os.chdir(f"/home/{username}/.minecraft/{pname}/{minecraft_version}")
        os.system(f"unzip '/home/{username}/.minecraft/{pname}/{minecraft_version}.jar'")

        with open('pack.mcmeta', 'w') as f:

            f.write("""
            {
    "pack": {
        "pack_format": 12,
        "description": "A texture pack made using MSHub"
    }
    }
            """)
        

        

        scan_packs()

        selection = pack_options[0]

        dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

        types = os.listdir(dir_path)
        print(pname)


create_first()




def load_textures(asset):
    global images
    
    images = []

    

    if selection != "packnotfound":
        dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"
        for paths in os.listdir(dir_path + asset):
            if paths.endswith(".png"):
                images.append(paths)
        
        
        fpath = next(os.walk(dir_path + asset))[1]

        if fpath != []:
            for subdir in fpath:
                for pathc in os.listdir(dir_path + asset + "/" + subdir):
                    if pathc.endswith(".png"):
                        images.append(subdir + "/" + pathc)

        
        print(fpath)

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


if selection != "packnotfound":
    types = os.listdir(dir_path)

ctype = types[0]

ccmages = []



header_buttons = []

#print(load_textures(ctype))
ctextures = []

header_button_size = math.ceil(800/(len(types)*0.5))




def startGimp(tipe, texet):
    if selection != "packnotfound":
        Thread(target=openGimp(tipe, texet)).start()
    

def openGimp(tp, txt):
    if selection != "packnotfound":

        dir_path = f"/home/{username}/.minecraft/{selection}/{minecraft_version}/assets/minecraft/textures/"

        if selection != "packnotfound":
            os.system("gimp "+ dir_path + tp + txt)







searchbar = tk.Entry(window, font=('Georgia 30'))

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
        


searchButton = tk.Button(window, text="SEARCH", command=searchCmd, bg="lightgreen")

searchButton.pack(side="right")

searchButton.place(x=720, y=0, width=80, height=40)


cutex = load_textures(ctype)




def export():

    os.system(f"rm '/home/{username}/.minecraft/{selection}/{minecraft_version}/{selection}.zip'")

    os.chdir(f"/home/{username}/.minecraft/{selection}/{minecraft_version}/")

    os.system(f"zip -r '/home/{username}/.minecraft/{selection}/{minecraft_version}/{selection}.zip' 'pack.mcmeta'")

    os.system(f"zip -ur '/home/{username}/.minecraft/{selection}/{minecraft_version}/{selection}.zip' 'assets'")



    os.system(f"cp '/home/{username}/.minecraft/{selection}/{minecraft_version}/{selection}.zip' '/home/{username}/.minecraft/resourcepacks/'")



name_entry_reference = ""

top = ""

uitems = []

def drop_updater():
    pack_drop["menu"].delete(0, "end")
    for item in pack_options:
        print(item)
        uitems.append(item)
        pack_drop["menu"].add_command(label=uitems[pack_options.index(item)], command=lambda value=item: clicked.set(value))

def newpack():
    global name_entry_reference
    global pack_drop
    global pack_options


    pname = name_entry_reference.get()


    os.system(f"mkdir '/home/{username}/.minecraft/{pname}'")
    os.system(f"cp '/home/{username}/.minecraft/versions/{minecraft_version}/{minecraft_version}.jar' '/home/{username}/.minecraft/{pname}'")


    os.chdir(f"/home/{username}/.minecraft/{pname}/")


    os.system(f"mkdir '/home/{username}/.minecraft/{pname}/{minecraft_version}'")

    os.chdir(f"/home/{username}/.minecraft/{pname}/{minecraft_version}")
    os.system(f"unzip '/home/{username}/.minecraft/{pname}/{minecraft_version}.jar'")

    with open('pack.mcmeta', 'w') as f:

        f.write("""
        {
  "pack": {
    "pack_format": 12,
    "description": "A texture pack made using MSHub"
  }
}
        """)
    
    scan_packs()
    drop_updater()
    print(pname)

    top.destroy()






def newpackwindow():
    global name_entry_reference
    global top

    top= Toplevel(window)
    top.geometry("300x150")
    top.title("New pack")


    npn = tk.Label(top, text="New pack name:", font=('Georgia 30'))
    npn.pack()

    name_entry = tk.Entry(top, font=('Georgia 30'))
    name_entry.pack()
    name_entry.place(x=0, y=40)

    name_entry_reference = name_entry

    create_button = tk.Button(top, text="Create", command=newpack)
    create_button.pack()
    create_button.place(x=100, y=100, width=100, height=40)
    

    


export_button = tk.Button(window, text="EXPORT", bg="yellow", command=export)

export_button.pack(side="left")

export_button.place(x=0, y=0, width=header_button_size, height=40)




new_button = tk.Button(window, text="NEW PACK", bg="pink", command=newpackwindow)

new_button.pack(side="left")

new_button.place(x=header_button_size, y=0, width=header_button_size, height=40)





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
            but.destroy()
        buttons.clear()
            

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


def callback(selektion, huhu, ioi):
    global selection
    global minecraft_version
    selection = clicked.get()
    print(selektion, huhu, ioi)
    #minecraft_version = next(os.walk(f"/home/{username}/.minecraft/{clicked}/"))[1][0]
    scan_packs()
    build_buttons_list()
    build_header()

clicked = StringVar()


clicked.trace_add("write", callback)






if pack_options != []:
    clicked.set(pack_options[0])
else:
    clicked.set("No custom texture pack")



pack_drop = tk.OptionMenu(window, clicked, *pack_options)


pack_drop.pack(side="right")

pack_drop.place(x=header_button_size*2, y=0, width= 170, height= 40)
build_buttons_list()
build_header()


print("starting main loop")



window.bind("<KeyRelease>", updatee)
mainLoop = Thread(target=window.mainloop())
mainLoop.start()