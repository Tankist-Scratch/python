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
        self.root = tk.Canvas(master, width=436, height=431)
        self.grid = self.root.grid

    def draw(self, matrix):
        self.root.delete("all")
        for y in range(20):
            for x in range(20):
                self.root.create_rectangle(21 * x + 17, 21 * y + 12, 21 * (x + 1) + 17, 21 * (y + 1) + 12,
                                           fill=self.colors[matrix[y][x]])
        self.text(1, 24, 0)
        self.text(2, 45, 0)
        self.text(3, 66, 0)
        self.text(4, 87, 0)
        self.text(5, 108, 0)
        self.text(6, 129, 0)
        self.text(7, 150, 0)
        self.text(8, 171, 0)
        self.text(9, 192, 0)
        self.text(10, 210, 0)
        self.text(11, 231, 0)
        self.text(12, 252, 0)
        self.text(13, 273, 0)
        self.text(14, 294, 0)
        self.text(15, 315, 0)
        self.text(16, 336, 0)
        self.text(17, 357, 0)
        self.text(18, 378, 0)
        self.text(19, 399, 0)
        self.text(20, 420, 0)
        self.text(1, 9, 15)
        self.text(2, 9, 36)
        self.text(3, 9, 57)
        self.text(4, 9, 78)
        self.text(5, 9, 99)
        self.text(6, 9, 120)
        self.text(7, 9, 141)
        self.text(8, 9, 162)
        self.text(9, 9, 183)
        self.text(10, 2, 204)
        self.text(11, 2, 225)
        self.text(12, 2, 246)
        self.text(13, 2, 267)
        self.text(14, 2, 288)
        self.text(15, 2, 309)
        self.text(16, 2, 330)
        self.text(17, 2, 351)
        self.text(18, 2, 372)
        self.text(19, 2, 393)
        self.text(20, 2, 414)

        # for i in range(21):
        #     self.root.create_line(11 * (i + 1), 0, 11 * (i + 1), 250, fill="black", width=1)
        #     self.root.create_line(0, 11 * (i + 1), 250,  11 * (i + 1), fill="black", width=1)

    def text(self, n, x, y):
        self.root.create_text(x, y, text=n, fill="black", font="Courier 8", anchor="nw")


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
            self.print("S", 1)
            try:
                x, y = map(int, subprocess.check_output("python bot1.py", timeout=1, universal_newlines=True,
                                                        input=self.printmatrix(game)).split())
                if game[y][x] != 0:
                    self.print("WA", 1)
                    self.print("EA", 2)
                else:
                    game[y][x] = 1
                    self.print("OK", 1, x + 1, y + 1)
                    if self.check(x, y):
                        self.print("EH", 1)
                    else:
                        cur = 2
            except subprocess.TimeoutExpired:
                self.print("TL", 1)
                self.print("EA", 2)
            except subprocess.CalledProcessError:
                self.print("RE", 1)
                self.print("EA", 2)
        elif cur == 2:
            cur = 0
            self.print("S", 2)
            try:
                x, y = map(int, subprocess.check_output("python bot2.py", timeout=1, universal_newlines=True,
                                                        input=self.printmatrix(game)).split())
                if game[y][x] != 0:
                    self.print("WA", 2)
                    self.print("EA", 1)
                else:
                    game[y][x] = 2
                    self.print("OK", 2, x + 1, y + 1)
                    if self.check(x, y):
                        self.print("EH", 2)
                    else:
                        cur = 1
            except subprocess.TimeoutExpired:
                self.print("TL", 2)
                self.print("EA", 1)
            except subprocess.CalledProcessError:
                self.print("RE", 2)
                self.print("EA", 1)

        root.draw(game)
        if cur != 0:
            go["state"] = "active"

    @staticmethod
    def printmatrix(matrix):
        s = ""
        for i in range(len(matrix)):
            s += " ".join(map(str, matrix[i]))
            s += "\n"
        return s

    def print(self, res, bot, *args):
        global log, rs
        log.insert(tk.END, self.msg[res] % ({1: bot1.name, 2: bot2.name}[bot], *args))
        log.yview(tk.END)
        rs["text"] = self.msg[res] % ({1: bot1.name, 2: bot2.name}[bot], *args) + "     "

    @staticmethod
    def check(x, y):
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
                    return True
        for i in range(5):
            if 0 <= y - 4 + i and y + i <= 19:
                if game[y - 4 + i][x] == game[y - 3 + i][x] == game[y - 2 + i][x] == game[y - 1 + i][x] == \
                        game[y + i][x]:
                    game[y - 4 + i][x] = game[y + i][x] + 2
                    game[y - 3 + i][x] = game[y + i][x] + 2
                    game[y - 2 + i][x] = game[y + i][x] + 2
                    game[y - 1 + i][x] = game[y + i][x] + 2
                    game[y + i][x] = game[y + i][x] + 2
                    return True
        for i in range(5):
            if x - 4 + i >= 0 <= y - 4 + i and y + i <= 19 >= x + i:
                if game[y - 4 + i][x - 4 + i] == game[y - 3 + i][x - 3 + i] == game[y - 2 + i][x - 2 + i] == \
                        game[y - 1 + i][x - 1 + i] == game[y + i][x + i]:
                    game[y - 4 + i][x - 4 + i] = game[y + i][x + i] + 2
                    game[y - 3 + i][x - 3 + i] = game[y + i][x + i] + 2
                    game[y - 2 + i][x - 2 + i] = game[y + i][x + i] + 2
                    game[y - 1 + i][x - 1 + i] = game[y + i][x + i] + 2
                    game[y + i][x + i] = game[y + i][x + i] + 2
                    return True
        for i in range(5):
            if 0 <= y - 4 + i and y + i <= 19 and x - i >= 0 and x + 4 - i <= 19:
                if game[y - 4 + i][x + 4 - i] == game[y - 3 + i][x + 3 - i] == game[y - 2 + i][x + 2 - i] == \
                        game[y - 1 + i][x + 1 - i] == game[y + i][x + i]:
                    game[y - 4 + i][x + 4 - i] = game[y + i][x - i] + 2
                    game[y - 3 + i][x + 3 - i] = game[y + i][x - i] + 2
                    game[y - 2 + i][x + 2 - i] = game[y + i][x - i] + 2
                    game[y - 1 + i][x + 1 - i] = game[y + i][x - i] + 2
                    print(game)
                    game[y + i][x - i] = game[y + i][x - i] + 2
                    print(game)
                    return True
        return False


win = tk.Tk()
win.resizable(True, False)
win.title("Крестики нолики")
root = GameCanvas(win, ["darkred", "green", "red", "lime"])

root.grid(column=0, row=0)
root.draw(game)
go = ttk.Button(win, text="Следующий ход", command=Play)
go.grid(column=0, row=1, sticky="nsew")
log = tk.Listbox(win, font="Courier")
log.grid(column=1, row=0, rowspan=2, sticky="nsew")
logscroll = tk.Scrollbar(win, orient="v")
logscroll.grid(column=2, row=0, rowspan=2, sticky="nsew")
logscroll['command'] = log.yview
log['yscrollcommand'] = logscroll.set
rs = tk.Label(win, font="Courier")
rs.grid(row=2, column=0, columnspan=3, sticky="w")
# win.bind("<KeyPress-space>", Play)
win.columnconfigure(1, weight=1)
win.mainloop()


