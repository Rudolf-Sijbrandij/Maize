from tkinter import *
from tkinter import ttk
from algoritmes import dfs, solver


class Window:
    def __init__(self, master):

        # maakt de hoofd window
        self.master = master
        self.master.title("Maize")
        self.master.geometry("620x680")
        self.master.configure(bg='#1b2838')
        self.master.iconbitmap('images/Maize.ico')

        # een aantal developer settings
        self.quick = -1  # doe als -1 om het invul proces NIET over te slaan, anders een getal tussen de max_size en
        # min_size om direct de dimensies van de maze in te vullen

        self.max_size = 99
        self.min_size = 11
        self.cell_size = 6  # pixel grootte van de maze cellen
        self.label_text = "Vul 2 oneven getallen in, minimaal " \
                          + str(self.min_size) + " en maximaal " + str(self.max_size)

        # een paar variabelen alvast aanmaken
        self.rows = -1
        self.columns = -1
        self.draw_count = 0
        self.maze = []
        self.position = [0, 0]
        self.character = Canvas(self.master)
        self.frame4 = Canvas(self.master)
        self.label1 = Label()

        # het openen van het begin window
        self.initial()

    def initial(self):
        # als de self.quick niet -1 is dan slaat hij deze window over zodat je niet constant de hoogte en breedte in
        # hoeft te vullen
        if self.quick != -1:
            self.rows = self.quick
            self.columns = self.quick
            self.initiate(0)  # 0 voor normaal, 1 voor disjointed
            return

        # maakt de frame bovenop de master window
        frame1 = Frame(self.master, width=200, height=200, bg='#1b2838')
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.label1.destroy()
        self.label1 = Label(frame1, text=self.label_text, bg='#1b2838', fg='#FFFFFF', font=("Arial", 15))
        self.label1.grid(row=0, column=0, pady=2)
        self.entry1 = Entry(frame1)
        self.entry1.insert(0, "Hoogte")
        self.entry1.grid(row=1, column=0, pady=2)
        self.entry2 = Entry(frame1)
        self.entry2.insert(0, "Breedte")
        self.entry2.grid(row=2, column=0, pady=2)
        button1 = ttk.Button(frame1, text="Normal", command=lambda: self.check(0))
        button1.grid(row=3, column=0, pady=2)
        button2 = ttk.Button(frame1, text="Disjointed", command=lambda: self.check(1))
        button2.grid(row=4, column=0, pady=2)
        return

    def check(self, maze_type):
        try:
            # probeert de waardes uit entry1 en entry2, als er niks in is gevuld gaat hij naar de except
            self.rows = int(self.entry1.get())
            self.columns = int(self.entry2.get())
        except ValueError:
            self.label_text = "Vul een geldig getal in"
            self.initial()
            return

        # checked of de ingevulde getallen te groot zijn
        if self.rows > self.max_size or self.columns > self.max_size:
            self.label_text = "Het getal mag niet groter zijn dan " + str(self.max_size)
            self.initial()
            return
        # checked of de ingevulde getallen te klein zijn
        elif self.rows < self.min_size or self.columns < self.min_size:
            self.label_text = "Het getal mag niet kleiner zijn dan " + str(self.min_size)
            self.initial()
            return

        # checked of de ingevulde getallen wel oneven zijn, als ze niet oneven zijn werkt de maze niet goed
        elif self.rows % 2 == 0 or self.columns % 2 == 0:
            self.label_text = "Vul een oneven getal in"
            self.initial()
            return
        else:
            # als alle tests doorstaan zijn gaat hij verder naar de initiate functie
            self.initiate(maze_type)
            return

    def draw(self, draw_row, draw_col, draw_color, frame):
        """
        Tekent een vierkant op de goede plaats op het opgegeven frame met de opgegeven kleur.

        Args:
            draw_row (int): De row waarop het vierkant moet komen.
            draw_col (int): De column waarop het vierkant moet komen.
            draw_color (string): De kleur van het vierkant.
            frame (frame): De tkinter frame waarop het vierkant komt

        Returns:
            None
        """
        x1 = (draw_col + 0.75) * self.cell_size
        y1 = (draw_row + 0.75) * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        frame.create_rectangle(x1, y1, x2, y2, fill=draw_color, outline=draw_color)
        return

    def draw_maze(self, maze, frame):
        # gaat elke cell af om er een vierkant te tekenen om de maze te maken
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if maze[row][col] == 1:
                    color = 'white'
                else:
                    color = 'black'
                self.draw(row, col, color, frame)
                if self.draw_count == 0:
                    frame.update()

        # houd bij hoe vaak de maze al gemaakt is om niet vaker dan 1x de animatie te spelen
        self.draw_count += 1
        return

    # een paar functies die movement opvangt

    def left(self, event):
        self.move('left')
        return

    def up(self, event):
        self.move('up')
        return

    def right(self, event):
        self.move('right')
        return

    def down(self, event):
        self.move('down')
        return

    def move(self, key):
        """
        Verplaatst de user icon op een geldig pad naarmate de gebruiker de pijltjestoetsen indrukt.

        Args:
            key (string): de naam van de ingedrukte key

        Returns:
            None
        """
        curX = self.position[0]
        curY = self.position[1]
        up = [curX - 1, curY]
        down = [curX + 1, curY]
        right = [curX, curY + 1]
        left = [curX, curY - 1]
        if key == 'left' and left[1] >= 0 and self.maze[left[0]][left[1]] == 1:
            self.position = left
        elif key == 'up' and up[0] >= 0 and self.maze[up[0]][up[1]] == 1:
            self.position = up
        elif key == 'right' and right[1] < self.columns and self.maze[right[0]][right[1]] == 1:
            self.position = right
        elif key == 'down' and down[0] < self.rows and self.maze[down[0]][down[1]] == 1:
            self.position = down
        elif key == 'right' and right == [self.rows - 1, self.columns]:
            self.frame4.destroy()
            self.frame4 = Canvas(self.master, width=25, height=10)
            self.frame4.grid(pady=2)
            label2 = Label(self.frame4, text='A-maze-ing!', bg='#1b2838', fg='#FFFFFF', font=("Arial", 10))
            label2.grid(pady=2)
        else:
            return
        self.character.destroy()
        self.character = Canvas(self.master, width=self.cell_size, height=self.cell_size, bg='red',
                                highlightthickness=0)
        self.character.place(x=16 + self.position[1] * self.cell_size, y=16 + self.position[0] * self.cell_size,
                             anchor=CENTER)
        return

    def initiate(self, maze_type):
        # verwijderd de eerdere frame met het invullen van de dimensies
        for i in self.master.winfo_children():
            i.destroy()

        # de pixel grootte van de maze berekenen
        width = (self.columns + 1) * self.cell_size
        height = (self.rows + 1) * self.cell_size

        # de maze frame maken
        frame2 = Canvas(self.master, width=width, height=height, bg='#000000')
        frame2.grid(padx=8, pady=8)

        # de maze maken door de functie uit het andere python bestand te callen
        self.maze = dfs(self.rows, self.columns, maze_type)

        # het visueel maken van de maze met nog een begin en een eind in het groen en rood
        self.draw_maze(self.maze, frame2)
        self.draw(0, -1, 'green', frame2)
        self.draw(self.rows - 1, self.columns, 'red', frame2)

        # zet het character op het eerste vakje
        self.character = Canvas(self.master, width=self.cell_size, height=self.cell_size, bg='red',
                                highlightthickness=0)
        self.character.place(x=16 + self.position[1] * self.cell_size, y=16 + self.position[0] * self.cell_size,
                             anchor=CENTER)

        # laat de user het character met de pijltjes toetsen bewegen
        self.master.bind('<Left>', self.left)
        self.master.bind('<Up>', self.up)
        self.master.bind('<Down>', self.down)
        self.master.bind('<Right>', self.right)

        # een extra frame maken voor de knop om de maze op te lossen
        frame3 = Canvas(self.master, width=25, height=10)
        frame3.grid(pady=2)
        button1 = ttk.Button(frame3, text="Solve", command=lambda: self.solve(self.maze, frame2))
        button1.grid(row=3, column=0, pady=2)
        return

    def solve(self, maze, frame):
        # het callen van de functie uit het andere python bestand om een solution te vinden voor de opgegeven maze
        solution = solver(maze)

        # het visueel maken van een pad van begin tot eind in het blauw in de eerder gemaakte maze
        self.draw_maze(maze, frame)
        self.draw(0, 0, 'blue', frame)
        for coord in solution:
            self.draw(coord[0], coord[1], 'blue', frame)
            frame.update()
        return


root = Tk()
Window(root)
root.mainloop()
