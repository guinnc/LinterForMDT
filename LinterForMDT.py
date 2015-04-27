__author__ = 'guinnc'

import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
from Linter import *

class LinterForMDT(object):

    def __init__(self):
        self.win = tk.Tk()
        self.filename = ""
        self.theLinter = None

        self.win.configure(background="#808000")
        self.win.title("Lint for MDT Grammars")
        self.win.geometry("800x600")

        menu = Menu(self.win)
        self.win.config(menu=menu)
        filemenu = Menu(menu)



        frame1 = tk.Frame(self.win,width=800, height=200,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        frame1.pack(expand=True, fill="both")


        scrollbarVert = tk.Scrollbar(frame1, orient=tk.VERTICAL)
        scrollbarHori = tk.Scrollbar(frame1, orient=tk.HORIZONTAL)
        editArea = tk.Text(frame1, width=80, height=20, wrap="none",
                           yscrollcommand=scrollbarVert.set,
                           xscrollcommand=scrollbarHori.set,
                           borderwidth=0, highlightthickness=0)
        lineNumbers = tk.Text(frame1, width=5, height=20, wrap="none",
                           yscrollcommand=scrollbarVert.set,
                           xscrollcommand=scrollbarHori.set,
                           borderwidth=1, highlightthickness=0)

        def yview(*args):
                editArea.yview(*args)
                lineNumbers.yview(*args)

        scrollbarVert.config(command=yview)
        #scrollbarVert.config(command=lineNumbers.yview)
        scrollbarHori.config(command=editArea.xview)
        scrollbarVert.pack(side="right", fill="y")
        scrollbarHori.pack(side="bottom", fill="both")
        lineNumbers.pack(side="left", fill="both", expand=False)
        editArea.pack(side="right", fill="both", expand=1)

        frame2 = tk.Frame(self.win,width=800, height=200,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbarVert2 = tk.Scrollbar(frame2, orient=tk.VERTICAL)
        scrollbarHori2 = tk.Scrollbar(frame2, orient=tk.HORIZONTAL)
        editArea2 = tk.Text(frame2, width=80, height=8, wrap="none",
                           yscrollcommand=scrollbarVert2.set,
                           xscrollcommand=scrollbarHori2.set,
                           borderwidth=4, highlightthickness=4)


        scrollbarVert2.config(command=editArea2.yview)
        scrollbarHori2.config(command=editArea2.xview)
        scrollbarVert2.pack(side="right", fill="y")
        scrollbarHori2.pack(side="bottom", fill="both", expand=True)
        #editArea2.insert(tk.INSERT, "Hello")

        editArea2.config(background="#C3E4ED")
        editArea2.pack(side="bottom", fill="both", expand=1)






        frame1.place(x=10,y=30)
        frame2.place(x=10, y=380)

        self.theLinter = Linter(editArea, editArea2, lineNumbers)
        #editArea2.config(state=tk.DISABLED)

        def dummy():
            print("Test it out")

        def open_command():
                file = filedialog.askopenfile(parent=self.win,mode='rb',title='Select a file')
                if file != None:
                    self.filename = file.name
                    self.win.title(self.filename)
                    contents = file.read()
                    editArea.delete(1.0, tk.END)
                    lineNumbers.delete(1.0, tk.END)
                    editArea2.delete(1.0, tk.END)
                    editArea.insert('1.0',contents)
                    file.close()
                    self.theLinter.runLinter()


        def save_command():
            if self.filename == "":
                saveas_command()
            else:
                #lint = Linter(editArea, editArea2, lineNumbers)
                #lint.runLinter()
                self.theLinter.runLinter()
                file = open(self.filename, mode='w')
                if file != None:
                # slice off the last character from get, as an extra return is added
                    data = editArea.get('1.0', tk.END+'-1c')
                    file.write(data)
                    file.close()

        def saveas_command():
            file = filedialog.asksaveasfile(mode='w')
            if file != None:
            # slice off the last character from get, as an extra return is added
                data = editArea.get('1.0', tk.END+'-1c')
                file.write(data)
                file.close()
                self.filename = file.name
                self.win.title(self.filename)

        def exit_command():
            if messagebox.askokcancel("Quit", "Do you really want to quit?"):
                self.win.destroy()


        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=dummy)
        filemenu.add_command(label="Open...", command=open_command)
        filemenu.add_command(label="Save", command=save_command)
        filemenu.add_command(label="Save As", command=saveas_command)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=exit_command)

main = LinterForMDT()
main.win.mainloop()



