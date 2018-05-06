import tkinter as tk
import tkinter.ttk as ttk
import subprocess

import bot1 as bot1
import bot2 as bot2

game = [[0] * 20 for _ in range(20)]
cur = 1


class GameCanvas:
    def __init__(self, master, colors):
        self.colors = ["white"] + colors
        self.root = tk.Canvas(master, width=230, height=230, background='white')
        self.grid = self.root.grid

    def draw(self, matrix):

        for y in range(20):
            for x in range(20):
                self.root.create_rectangle(11 * (x + 1), 11 * (y + 1), 11 * (x + 2), 11 * (y + 2),
                                           fill=self.colors[matrix[y][x]])

                # for i in range(21):
                #     self.root.create_line(11 * (i + 1), 0, 11 * (i + 1), 250, fill="black", width=1)
                #     self.root.create_line(0, 11 * (i + 1), 250,  11 * (i + 1), fill="black", width=1)

    def num(self, n):
        n = str(n)


class Play:
    msg = {
        "OK": "Бот %s успешно походил в [%s, %s]",
        "TL": "Бот %s слишком долго думал...",
        "RE": "Бот %s сгорел",
        "WA": "Бот %s поднял бунт и его пришлось уничтожить",
        "S": "Ходит бот %s",
        "EH": "Бот %s выиграл",
        "EA": "Боту %s пришлось выиграть",
    }

    def __init__(self, bind=""):
        global cur, game
        go["state"] = "disable"
        if cur == 1:
            cur = 0
            try:
                self.print("S", 1)
                x, y = map(int, subprocess.check_output("python bot1.py", timeout=1, universal_newlines=True,
                                                        input=self.printmatrix(game)).split())
                if game[y][x] != 0:
                    self.print("WA", 1)
                else:
                    game[y][x] = 1
                    self.print("OK", 1, x, y)
                    self.check(x, y)
                    cur = 2
            except subprocess.TimeoutExpired:
                self.print("TL", 1)
            except subprocess.CalledProcessError:
                self.print("RE", 1)
        elif cur == 2:
            cur = 0
            try:
                self.print("S", 2)
                x, y = map(int, subprocess.check_output("python bot2.py", timeout=1, universal_newlines=True,
                                                        input=self.printmatrix(game)).split())
                if game[y][x] != 0:
                    self.print("WA", 2)
                else:
                    game[y][x] = 2
                    self.print("OK", 2, x, y)
                    self.check(x, y)
                    cur = 1
            except subprocess.TimeoutExpired:
                self.print("TL", 2)
            except subprocess.CalledProcessError:
                self.print("RE", 2)
        root.draw(game)
        go["state"] = "active"
    def printmatrix(self, matrix):
        s = ""
        for i in range(len(matrix)):
            s += " ".join(map(str, matrix[i]))
            s += "\n"
        return s

    def print(self, type, bot, *args):
        global log
        log.insert(tk.END, self.msg[type] % ({1: bot1.name, 2: bot2.name}[bot], *args))

    def check(self, x, y):
        global game
        for i in range(5):
            if 0 <= x - 4 + i and x + i <= 19:
                if game[y][x - 4 + i] == game[y][x - 3 + i] == game[y][x - 2 + i] == game[y][x - 1 + i] == \
                        game[y][x + i]:
                    game[y][x - 4 + i] = game[y][x + i] + 2
                    game[y][x - 3 + i] = game[y][x + i] + 2
                    game[y][x - 2 + i] = game[y][x + i] + 2
                    game[y][x - 1 + i] = game[y][x + i] + 2
                    game[y][x + i] = game[y][x + i] + 2
        for i in range(5):
            if 0 <= y - 4 + i and y + i <= 19:
                if game[y - 4 + i][x] == game[y - 3 + i][x] == game[y - 2 + i][x] == game[y - 1 + i][x] == \
                        game[y + i][x]:
                    game[y - 4 + i][x] = game[y + i][x] + 2
                    game[y - 3 + i][x] = game[y + i][x] + 2
                    game[y - 2 + i][x] = game[y + i][x] + 2
                    game[y - 1 + i][x] = game[y + i][x] + 2
                    game[y + i][x] = game[y + i][x] + 2



win = tk.Tk()
win.resizable(True, False)
root = GameCanvas(win, ["red", "green", "orange", "lime"])

root.grid(column=0, row=0)
root.draw(game)
go = ttk.Button(win, text="Следующий ход", command=Play)
go.grid(column=0, row=1, sticky="nsew")
log = tk.Listbox(win)
log.grid(column=1, row=0, rowspan=2, sticky="nsew")
logscroll = tk.Scrollbar(win, orient="v")
logscroll.grid(column=2, row=0, rowspan=2, sticky="nsew")
logscroll['command'] = log.yview
log['yscrollcommand'] = logscroll.set
#win.bind("<KeyPress-space>", Play)
win.columnconfigure(1, weight=1)
win.mainloop()
