from tkinter import *
from tkinter import ttk
from algoritmes import *


class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Maize")
        self.master.geometry("620x680")
        self.master.configure(bg='#1b2838')
        self.master.iconbitmap('images/Maize.ico')
        self.quick = 99  # doe als -1 om het invul proces NIET over te slaan
        self.max_size = 99
        self.min_size = 21
        self.label_text = "Vul 2 oneven getallen in, minimaal "\
                          + str(self.min_size) + " en maximaal " + str(self.max_size)
        self.rows = -1
        self.columns = -1
        self.cell_size = 6  # pixels
        self.draw_count = 0
        self.initial()

    def initial(self):
        if self.quick != -1:
            self.rows = self.quick
            self.columns = self.quick
            self.initiate()
            return
        frame1 = Frame(self.master, width=200, height=200, bg='#1b2838')
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER)
        label = Label(frame1, text=self.label_text, bg='#1b2838', fg='#FFFFFF', font=("Arial", 15))
        label.grid(row=0, column=0, pady=2)
        self.entry1 = Entry(frame1)
        self.entry1.insert(0, "Hoogte")
        self.entry1.grid(row=1, column=0, pady=2)
        self.entry2 = Entry(frame1)
        self.entry2.insert(0, "Breedte")
        self.entry2.grid(row=2, column=0, pady=2)
        button1 = ttk.Button(frame1, text="Confirm", command=self.check)
        button1.grid(row=3, column=0, pady=2)
        return

    def check(self):
        try:
            self.rows = int(self.entry1.get())
            self.columns = int(self.entry2.get())
        except ValueError:
            self.label_text = "Vul een geldig getal in"
            self.initial()
            return
        if self.rows > self.max_size or self.columns > self.max_size:
            self.label_text = "Het getal mag niet groter zijn dan" + str(self.max_size)
            self.initial()
            return
        elif self.rows < self.min_size or self.columns < self.min_size:
            self.label_text = "Het getal mag niet kleiner zijn dan" + str(self.min_size)
            self.initial()
            return
        elif self.rows % 2 == 0 or self.columns % 2 == 0:
            self.label_text = "Vul een oneven getal in"
            self.initial()
            return
        else:
            self.initiate()
            return

    def draw(self, draw_row, draw_col, draw_color, frame):
        x1 = (draw_col + 0.75) * self.cell_size
        y1 = (draw_row + 0.75) * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        frame.create_rectangle(x1, y1, x2, y2, fill=draw_color, outline=draw_color)
        return

    def draw_maze(self, maze, frame):
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if maze[row][col] == 1:
                    color = 'white'
                else:
                    color = 'black'
                self.draw(row, col, color, frame)
                if self.draw_count == 0:
                    frame.update()
        self.draw_count += 1
        return

    def initiate(self):
        for i in self.master.winfo_children():
            i.destroy()
        width = (self.columns + 1)*self.cell_size
        height = (self.rows + 1)*self.cell_size
        frame2 = Canvas(self.master, width=width, height=height, bg='#000000')
        frame2.place(relx=0.5, rely=0.5, anchor=CENTER)
        maze = dfs(self.rows, self.columns)
        self.draw_maze(maze, frame2)
        self.draw(0, -1, 'green', frame2)
        self.draw(self.rows - 1, self.columns, 'red', frame2)
        frame3 = Canvas(self.master, width=25, height=10)
        frame3.pack(side=TOP)
        button1 = ttk.Button(frame3, text="Solve", command=lambda: self.solve(maze, frame2))
        button1.grid(row=3, column=0, pady=2)
        return

    def solve(self, maze, frame):
        solution = tremaux(maze)
        self.draw_maze(maze, frame)
        self.draw(0, 0, 'blue', frame)
        for coord in solution:
            print(coord)
            self.draw(coord[0], coord[1], 'blue', frame)
            frame.update()
        return


root = Tk()
Window(root)
root.mainloop()
