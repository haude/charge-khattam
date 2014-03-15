#!/usr/bin/python
# -*- coding: utf-8 -*-
# ^^^ needed for py2

import os, sys

try:
    from subprocess import check_output
except:
    pass

try: # py2/3 compatibility
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk
    from tkinter.ttk import *
    from tkinter.simpledialog import askstring
except:
    import Tkinter as tk
    from Tkinter import *
    import ttk
    from ttk import *
    from tkSimpleDialog import askstring


def_font=[ "DejaVuSansMono", 11, "normal" ]

filepath = os.path.abspath(__file__)
fullpath = os.path.dirname(filepath)
sys.path.append(fullpath)

from vtk100_colors import main as vt100
vt100.def_font = def_font

PATH_batti=fullpath+'/batti/main.sh'

#   ____ _   _ ___
#  / ___| | | |_ _|
# | |  _| | | || |
# | |_| | |_| || |
#  \____|\___/|___|

class GUI(Frame):
    def __init__(self, ):
        Frame.__init__(self, parent=None)
        self.makeWidgets()
        self.bindWidgets()
        self.pack(expand=NO, fill=X, side=TOP)

    def makeWidgets(self):
        set_frame = tk.Frame(self, borderwidth=10)

        self.btn_refresh = Button(set_frame, text="Update")
        self.btn_refresh.config(command=None)

        self.alarm = BooleanVar()
        self.alarm.set(True)
        cbox_alarm = tk.Checkbutton(set_frame, text="Alarm", variable=self.alarm)
        self.alarm.trace('w', self.alarm_toggle)

        self.alarm_frame = ttk.LabelFrame(set_frame, text="Alarm")

        self.notify = BooleanVar()
        self.notify.set(True)
        cbox_notify = tk.Checkbutton(self.alarm_frame, text="notify", variable=self.notify)
        self.notify.trace('w', self.notify_toggle)

        self.alert = Entry(self.alarm_frame, width=5)
        self.alert.insert(END, "5");

        self.action = StringVar()
        self.action.set("None") # default value
        opt_action = OptionMenu(self.alarm_frame, self.action, "None", "None", "Sleep", "Hibernate", "Shutdown")

        self.grp = StringVar()
        opt_grp = OptionMenu(self.alarm_frame, self.grp, "1", "1", "2", "3", "4", "5", "6", "7")

        search_frame = ttk.LabelFrame(self, text="Group no")
        combo_font = def_font[:]; combo_font[1]=11

        self.today = BooleanVar()
        cbox_today = tk.Checkbutton(search_frame, text="today")
        cbox_today.config( variable=self.today, takefocus=0)
        self.today.set(False)
        self.today.trace('w', self.sbox_enter)

        self.sbox = ttk.Combobox(search_frame, font=combo_font)
        self.sbox.insert(0, "Group no here")
        self.sbox.config(values=['1', '2', '3', '4', '5', '6', '7'])

        self.out = Text(font=def_font, height=16, width=80)

        # packing
        set_frame.pack(side=TOP, expand=YES, fill=X)
        self.alarm_frame.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10)
        self.btn_refresh.pack(side=LEFT)
        cbox_alarm.pack(side=LEFT)

        Label(self.alarm_frame, text=" Group ").pack(side=LEFT)
        opt_grp.pack(side=LEFT)

        Label(self.alarm_frame, text=" Snooze (min) ").pack(side=LEFT, pady=5)
        self.alert.pack(side=LEFT)
        Label(self.alarm_frame, text=" Action ").pack(side=LEFT)
        opt_action.pack(side=LEFT)

        Label(self.alarm_frame, text = "battery level (%) ").pack(side=LEFT)

        bat=Entry(self.alarm_frame, width=5)
        bat.insert(END, "10")
        bat.pack(side=LEFT)
        tk.Checkbutton(self.alarm_frame, text="battery level").pack(side=LEFT)
        cbox_notify.pack(side=RIGHT)

        cbox_today.pack(side=RIGHT)
        self.sbox.pack(expand=YES, side=RIGHT, fill=X)
        Label(search_frame, text="Group ").pack(side=LEFT, padx=5, pady=8)

        search_frame.pack(expand=YES, side=TOP, fill=X, padx=5, pady=5)
        self.out.pack(expand=YES, fill=BOTH, side=BOTTOM)

    def bindWidgets(self):
        self.sbox.bind("<Button-1>", lambda e: self.sbox.delete(0, END))
        self.sbox.bind("<Return>", lambda e: self.sbox_enter())
        self.sbox.bind("<Return>", lambda e: self.sbox_enter())
        root.bind('<Key>', key_press)
        root.bind('<Control-s>', self.sboxSetFocus)

    def sbox_enter(self, *arg):
        grab=self.sbox.get().lower().strip()
        arg=[ PATH_batti, "-g", grab ]

        if self.today.get():
            arg.append("-t")

        if grab == "":
            arg=[ PATH_batti ]

        print(arg)
        gui.out.config(state=NORMAL)
        try:
            output=check_output(arg, universal_newlines=True)
        except:
            pass
        vtk.parser(output)
        gui.out.config(state=DISABLED)

    def sboxSetFocus(self, event):
        self.sbox.focus()
        self.sbox.select_range(0, END)

    def alarm_toggle(self, *arg):
        if self.alarm.get():
            self.alarm_frame.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10)
            self.alarm.set(True)
        else:
            self.alarm_frame.pack_forget()
            self.alarm.set(False)

    def notify_toggle(self, *arg):
        print("hello")
        if self.notify.get():
            os.system("/usr/bin/notify-send -i /usr/share/icons/HighContrast/256x256/status/battery-caution.png 'charge khattam' 'notification will be shown here\n15 min left'")
            try:
                os.system("espeak 'baatti gaayo' -p 500 -s 200")
            except:
                pass
            self.notify.set(True)
        else:
            self.notify.set(False)


def key_press(event):
    typed = event.char
    if not typed.isalpha(): return
    gui.sbox.delete(0, END)
    gui.sbox.insert(0, typed)
    gui.sbox.focus()
    root.unbind('<Key>')

if __name__ == '__main__':
    root = Tk()
    root.title("charge खत्तम")

    try:
        logo=PhotoImage(file=fullpath+"/img/battiaayo.png")
        root.tk.call('wm', 'iconphoto', root._w, logo)
    except Exception:
        logo=None
        print("can't load image, its insane")


    gui = GUI()
    vtk = vt100.vt100tk(gui.out)
    try:
        out = check_output([PATH_batti], universal_newlines=True)
    except:
        out = open('dump').read()

    vtk.parser(out)
    gui.out.config(state=DISABLED)

    root.bind('<Key-Escape>', lambda event: quit())
    root.bind('<Control-d>', lambda e: os.system("./test.py"))

    root.mainloop()
