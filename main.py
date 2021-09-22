# from tkinter import *
from tkinter import (Tk, END, Menu)
from tkinter.filedialog import asksaveasfilename, askopenfilenames
import json
from weldapp import Application
import os

# NOTE: IN THIS PROGRAM, SECTION PROPERTIES ARE ALWAYS INPUTTED AND PROCESSED
# IN THE FOLLOWING ORDER: MOMENT-X, MOMENT-Y, SHEAR-X, SHEAR-Y, AXIAL, TORSION

VERSION = '0.92 Beta  -  DO NOT USE FOR DESIGN'
TITLE = 'Weld Group Strength Calculator'


def savedata():
    global filename
    global app

    if filename:
        vars = {
            'b': float(app.entry_b.get()) if app.entry_b.get() != "" else 0,
            'd': float(app.entry_d.get()) if app.entry_d.get() != "" else 0,
            'Mux': float(app.entry_Mux.get()) if app.entry_Mux.get() != "" else 0,
            'Muy': float(app.entry_Muy.get()) if app.entry_Muy.get() != "" else 0,
            'Vux': float(app.entry_Vux.get()) if app.entry_Vux.get() != "" else 0,
            'Vuy': float(app.entry_Vuy.get()) if app.entry_Vuy.get() != "" else 0,
            'Au': float(app.entry_Au.get()) if app.entry_Au.get() != "" else 0,
            'Tu': float(app.entry_Tu.get()) if app.entry_Tu.get() != "" else 0,
            'units': app.units.get(),
            'considerAngle': app.considerAngle.get(),
            'util_setting': app.util_setting.get(),
            'weldtype': app.weldtype.get(),
            'selected_throat': app.selected_throat.get(),
            'selected_hss_thickness': app.selected_hss_thickness.get(),
            'selected_weld_group': app.selected_weld_group.get(),
        }

        with open(filename, 'w') as f:
            json.dump(vars, f, indent=4)
        set_title(root, filename)

    else:
        saveasdata()


def saveasdata():
    global filename
    filename = asksaveasfilename(
        title='Choose Filename', defaultextension='.txt',
        filetypes=[('.txt Files', '*.txt')])
    print(filename)
    if not filename:
        return
    savedata()


def loaddata():
    global app
    global filename

    try:
        filename = askopenfilenames(title="Select Weld .txt File")[0]
        print(filename)
    except IndexError:
        print("No file opened")
        return
    print("loaded -> " + filename)

    if filename:
        with open(filename, 'r') as f:
            vars = json.load(f)

            app.weldtype.set(vars['weldtype'])
            app.selected_throat.set(vars['selected_throat'])
            app.selected_hss_thickness.set(vars['selected_hss_thickness'])
            app.selected_weld_group.set(vars['selected_weld_group'])
            app.units.set(vars['units'])
            app.considerAngle.set(vars['considerAngle'])
            app.util_setting.set(vars['util_setting'])

            app.entry_b.delete(0, END)
            app.entry_b.insert(0, vars['b'])

            app.entry_d.delete(0, END)
            app.entry_d.insert(0, vars['d'])

            app.entry_Mux.delete(0, END)
            app.entry_Mux.insert(0, vars['Mux'])

            app.entry_Muy.delete(0, END)
            app.entry_Muy.insert(0, vars['Muy'])

            app.entry_Vux.delete(0, END)
            app.entry_Vux.insert(0, vars['Vux'])

            app.entry_Vuy.delete(0, END)
            app.entry_Vuy.insert(0, vars['Vuy'])

            app.entry_Au.delete(0, END)
            app.entry_Au.insert(0, vars['Au'])

            app.entry_Tu.delete(0, END)
            app.entry_Tu.insert(0, vars['Tu'])

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
