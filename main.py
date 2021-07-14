# from tkinter import *
from tkinter import (Tk, END, Menu)
from tkinter.filedialog import asksaveasfilename, askopenfilenames
import shelve
from weldapp import Application
import os

# NOTE: IN THIS PROGRAM, SECTION PROPERTIES ARE ALWAYS INPUTTED AND PROCESSED
# IN THE FOLLOWING ORDER: MOMENT-X, MOMENT-Y, SHEAR-X, SHEAR-Y, AXIAL, TORSION

VERSION = '0.91 Beta  -  DO NOT USE FOR DESIGN'
TITLE = 'Weld Group Strength Calculator'


def savedata():
    global filename
    global app

    if filename:
        with shelve.open(filename, 'c') as shelf:
            shelf['b'] = float(app.entry_b.get())
            shelf['d'] = float(app.entry_d.get())
            shelf['Mux'] = abs(float(app.entry_Mux.get()))
            shelf['Muy'] = abs(float(app.entry_Muy.get()))
            shelf['Vux'] = abs(float(app.entry_Vux.get()))
            shelf['Vuy'] = abs(float(app.entry_Vuy.get()))
            shelf['Au'] = abs(float(app.entry_Au.get()))
            shelf['Tu'] = abs(float(app.entry_Tu.get()))
            shelf['units'] = app.units.get()
            shelf['considerAngle'] = app.considerAngle.get()
            shelf['util_setting'] = app.util_setting.get()
            shelf['weldtype'] = app.weldtype.get()
            shelf['selected_throat'] = app.selected_throat.get()
            shelf['selected_hss_thickness'] = app.selected_hss_thickness.get()
            shelf['selected_weld_group'] = app.selected_weld_group.get()
            # shelf[''] =

        set_title(root, filename)

    else:
        saveasdata()


def saveasdata():
    global filename
    filename = asksaveasfilename(
        title='Choose Filename', defaultextension='.db', 
        filetypes=[('.db Files', '*.db')]).replace('.db', '')
    print(filename)
    if not filename:
        return
    savedata()


def loaddata():
    global app

    try:
        filename = askopenfilenames(title="Select Weld .txt File")[
            0].replace('.db', '')
        print(filename)
    except IndexError:
        print("No file opened")
        return
    print("loaded -> " + filename)

    if filename:
        with shelve.open(filename, 'r') as shelf:
            app.weldtype.set(shelf['weldtype'])
            app.selected_throat.set(shelf['selected_throat'])
            app.selected_hss_thickness.set(shelf['selected_hss_thickness'])
            app.selected_weld_group.set(shelf['selected_weld_group'])
            app.units.set(shelf['units'])
            app.considerAngle.set(shelf['considerAngle'])
            app.util_setting.set(shelf['util_setting'])

            app.entry_b.delete(0, END)
            app.entry_b.insert(0, shelf['b'])

            app.entry_d.delete(0, END)
            app.entry_d.insert(0, shelf['d'])

            app.entry_Mux.delete(0, END)
            app.entry_Mux.insert(0, shelf['Mux'])

            app.entry_Muy.delete(0, END)
            app.entry_Muy.insert(0, shelf['Muy'])

            app.entry_Vux.delete(0, END)
            app.entry_Vux.insert(0, shelf['Vux'])

            app.entry_Vuy.delete(0, END)
            app.entry_Vuy.insert(0, shelf['Vuy'])

            app.entry_Au.delete(0, END)
            app.entry_Au.insert(0, shelf['Au'])

            app.entry_Tu.delete(0, END)
            app.entry_Tu.insert(0, shelf['Tu'])

            app.recalc_full()
            set_title(root, filename)

    else:
        print("File not read")


def resetter(to_be_destroyed):
    global root
    to_be_destroyed.destroy()
    global app
    app = Application(root, VERSION)
    set_title(root)


def set_title(root, full_path=None):
    if full_path:
        root.title(
            f'Weld Group Strength Calculator - {os.path.split(full_path)[-1]}')
    else:
        root.title(f'Weld Group Strength Calculator')


if __name__ == '__main__':
    # set up root window with title
    root = Tk()
    root.geometry('900x475')
    root.minsize(width=850, height=450)
    root.title(TITLE)
    root.resizable(width=True, height=True)

    # working file name for save and open
    filename = None

    # set up menu bar
    menubar = Menu(root)

    # set up file menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New (Reset)", command=lambda: resetter(app))
    filemenu.add_command(label="Save", command=savedata)
    filemenu.add_command(label="Save As...", command=saveasdata)
    filemenu.add_command(label="Open...", command=loaddata)
    # filemenu.add_command(label="Exit", command=exit)

    # add file menu
    menubar.add_cascade(label="File", menu=filemenu)

    # set up edit menu

    # add edit menu

    root.config(menu=menubar)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    app = Application(root, VERSION)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app.grid(sticky='nsew')
    root.mainloop()
