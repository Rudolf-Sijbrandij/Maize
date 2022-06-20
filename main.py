from tkinter import *
from tkinter import ttk
from random import randint


class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Maize")
        self.master.geometry("620x620")
        self.master.configure(bg='#1b2838')
        self.master.iconbitmap('images/Maize.ico')
        self.max_size = 70
        self.min_size = 10
        self.label_text = "Vul 2 getallen in, minimaal " + str(self.min_size) + " en maximaal " + str(self.max_size)
        self.rows = -1
        self.columns = -1
        self.cell_size = 8  # pixels
        self.initial()

    def initial(self):
        for i in self.master.winfo_children():
            i.destroy()
        frame1 = Frame(self.master, width=200, height=200, bg='#1b2838')
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER)
        label = Label(frame1, text=self.label_text, bg='#1b2838', fg='#FFFFFF', font=("Arial", 15))
        label.grid(row=0, column=0, pady=2)
        self.entry1 = Entry(frame1)
        self.entry1.grid(row=1, column=0, pady=2)
        self.entry2 = Entry(frame1)
        self.entry2.grid(row=2, column=0, pady=2)
        button1 = ttk.Button(frame1, text="Confirm", command=self.check)
        button1.grid(row=3, column=0, pady=2)

    def check(self):
        try:
            self.rows = int(self.entry1.get())
            self.columns = int(self.entry2.get())
        except ValueError:
            self.label_text = "Vul een geldig getal in"
            self.initial()
            return
        if self.rows > self.max_size or self.columns > self.max_size:
            self.label_text = "Het getal mag niet groter zijn dan " + str(self.max_size)
            self.initial()
            return
        elif self.rows < self.min_size or self.columns < self.min_size:
            self.label_text = " Het getal mag niet kleiner zijn dan " + str(self.min_size)
            self.initial()
            return
        else:
            self.register()
            return

    def register(self):
        def draw(draw_row, draw_col, draw_color):
            x1 = (draw_col + 0.75) * self.cell_size
            y1 = (draw_row + 0.75) * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            frame2.create_rectangle(x1, y1, x2, y2, fill=draw_color)
            return

        for i in self.master.winfo_children():
            i.destroy()
        width = (self.columns + 2)*self.cell_size
        height = (self.rows + 2)*self.cell_size
        frame2 = Canvas(self.master, width=width, height=height, bg='#000000')
        frame2.place(relx=0.5, rely=0.5, anchor=CENTER)
        for row in range(self.rows + 1):
            for col in range(self.columns + 1):
                if randint(0, 1) == 0:
                    color = 'white'
                else:
                    color = 'black'
                draw(row, col, color)


root = Tk()
Window(root)
root.mainloop()
