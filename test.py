#!/usr/bin/python

import tkinter as tk

def_font=[ "DejaVuSansMono",100, "normal" ]
def_font2=[ "DejaVuSansMono", 50, "normal" ]

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10, font=def_font)
        tk.Label(self, text="Hit ESC to stop", font=def_font2).pack()

        self.label.pack()
        self.remaining = 0
        self.countdown(10)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

if __name__ == "__main__":
    app = ExampleApp()
    app.bind('<Key-Escape>', lambda event: quit())
    app.mainloop()
