# from tkinter import *
from tkinter import (Tk, END, Menu)
from tkinter.filedialog import asksaveasfilename, askopenfilenames
import pickle
from weldapp import Application

# NOTE: IN THIS PROGRAM, SECTION PROPERTIES ARE ALWAYS INPUTTED AND PROCESSED
# IN THE FOLLOWING ORDER: MOMENT-X, MOMENT-Y, SHEAR-X, SHEAR-Y, AXIAL, TORSION

VERSION = '0.9 Beta  -  DO NOT USE FOR DESIGN'


def savedata():
    global filename
    global app

    if filename:
        # print("normal save -> " + filename)
        b = float(app.entry_b.get())
        d = float(app.entry_d.get())
        Mux = abs(float(app.entry_Mux.get()))
        Muy = abs(float(app.entry_Muy.get()))
        Vux = abs(float(app.entry_Vux.get()))
        Vuy = abs(float(app.entry_Vuy.get()))
        Au = abs(float(app.entry_Au.get()))
        Tu = abs(float(app.entry_Tu.get()))
        units = app.units.get()
        considerAngle = app.considerAngle.get()

        # assign variables that get saved
        vars = (app.weldtype.get(), app.selected_throat.get(), app.selected_hss_thickness.get(
        ), app.selected_weld_group.get(), b, d, Mux, Muy, Vux, Vuy, Au, Tu, units, considerAngle)

        with open(filename, "wb") as file:
            pickle.dump(vars, file)

    else:
        saveasdata()


def saveasdata():
    global filename
    filename = asksaveasfilename(
        title='Choose Filename', defaultextension='.txt', filetypes=[('Text Files', '*.txt')])
    if not filename:
        return
    # print("saving as -> " + filename)
    savedata()


def loaddata():
    global app

    try:
        filename = askopenfilenames(title="Select Weld .txt File")[0]
    except IndexError:
        print("No file opened")
        return
    print(type(filename))
    print("loaded -> " + filename)

    if filename:
        with open(filename, "rb") as file:
            var_weldtype, var_selected_throat, var_selected_hss_thickness, var_selected_weld_group, b, d, Mux, Muy, Vux, Vuy, Au, Tu, units, considerAngle = pickle.load(
                file)

            app.weldtype.set(var_weldtype)
            app.selected_throat.set(var_selected_throat)
            app.selected_hss_thickness.set(var_selected_hss_thickness)
            app.selected_weld_group.set(var_selected_weld_group)
            app.units.set(units)
            app.considerAngle.set(considerAngle)

            app.entry_b.delete(0, END)
            app.entry_b.insert(0, b)

            app.entry_d.delete(0, END)
            app.entry_d.insert(0, d)

            app.entry_Mux.delete(0, END)
            app.entry_Mux.insert(0, Mux)

            app.entry_Muy.delete(0, END)
            app.entry_Muy.insert(0, Muy)

            app.entry_Vux.delete(0, END)
            app.entry_Vux.insert(0, Vux)

            app.entry_Vuy.delete(0, END)
            app.entry_Vuy.insert(0, Vuy)

            app.entry_Au.delete(0, END)
            app.entry_Au.insert(0, Au)

            app.entry_Tu.delete(0, END)
            app.entry_Tu.insert(0, Tu)

            app.recalc_full()

    else:
        print("File not read")


def resetter(to_be_destroyed):
    global root
    to_be_destroyed.destroy()
    global app
    app = Application(root, VERSION)


if __name__ == '__main__':
    ################################# DRAW GUI #################################
    # set up root window with title
    root = Tk()
    root.geometry('900x465')
    root.minsize(width=900, height=465)
    root.title("Weld Group Strength Calculator")
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
    filemenu.add_command(label="Exit", command=exit)

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
