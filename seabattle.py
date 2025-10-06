import tkinter as tk
from tkinter import messagebox
import random

root, player_board, enemy_board, player_display, bot_display = None, None, None, None, None
player_buttons, enemy_buttons, bot_hits, bot_targets = [], [], [], []
bot_mode, game_over, placing_ships, ships = "search", False, True, [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
size_var, dir_var, ships_label = None, None, None

def create_board(): return [["~" for _ in range(10)] for _ in range(10)]

def can_place_ship(b, x, y, s, d):
    if d == "h" and y + s <= 10:
        for i in range(max(0, x - 1), min(10, x + 2)):
            for j in range(max(0, y - 1), min(10, y + s + 1)):
                if b[i][j] != "~": return False
    elif d == "v" and x + s <= 10:
        for i in range(max(0, x - 1), min(10, x + s + 1)):
            for j in range(max(0, y - 1), min(10, y + 2)):
                if b[i][j] != "~": return False
    else:
        return False
    return True

def place_ship(b, x, y, s, d):
    if can_place_ship(b, x, y, s, d):
        for i in range(s):
            if d == "h":
                b[x][y + i] = "S"
            else:
                b[x + i][y] = "S"
        return True
    return False

def setup_bot_ships():
    for s in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
        while not place_ship(enemy_board, random.randint(0, 9), random.randint(0, 9), s,
                             random.choice(["h", "v"])): pass

def update_ships_label():
    c = {4: 0, 3: 0, 2: 0, 1: 0}
    for s in ships: c[s] += 1
    ships_label.config(
        text=f"Осталось: {', '.join(f'{v}×{k}' for k, v in sorted(c.items(), reverse=True) if v) or 'нет кораблей'}")

def update_ui():
    for i in range(10):
        for j in range(10):
            c = player_board[i][j]
            player_buttons[i][j].config(
                bg="blue" if c == "S" else "white" if c == "~" else "red" if c == "X" else "gray",
                state="disabled" if not placing_ships else "normal")
            c = player_display[i][j]
            enemy_buttons[i][j].config(bg="white" if c == "~" else "red" if c == "X" else "gray",
                                       state="disabled" if c in ["X", "O"] or placing_ships else "normal"); update_ships_label()

def place_ship_click(x, y):
    global placing_ships, ships
    if not placing_ships or not ships: return
    try:
        s = int(size_var.get())
        if s not in ships: raise ValueError
        if place_ship(player_board, x, y, s, "h" if dir_var.get() == "Горизонтально" else "v"):
            ships.remove(s)
            if not ships:
                placing_ships = False
                for i in range(10):
                    for j in range(10): player_buttons[i][j].config(command=lambda: None, state="disabled");
                    enemy_buttons[i][j].config(state="normal")
            update_ui()
    except:
        pass

def is_hit(b, x, y): return b[x][y] == "S"

def is_ship_sunk(b, x, y, d):
    if b[x][y] != "X": return False
    v, s = set(), [(x, y)]
    while s:
        cx, cy = s.pop()
        if (cx, cy) in v or not (0 <= cx < 10 and 0 <= cy < 10): continue
        if b[cx][cy] == "X": v.add((cx, cy)); s.extend(
            [(cx + dx, cy + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)] if
             0 <= cx + dx < 10 and 0 <= cy + dy < 10])
    for cx, cy in v:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and b[nx][ny] == "S": return False
    for cx, cy in v:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and b[nx][ny] == "~": b[nx][ny] = d[nx][ny] = "O"
    return True

def all_ships_sunk(b): return not any("S" in row for row in b)

def player_turn(x, y):
    global game_over, player_display, enemy_board
    if game_over or placing_ships or player_display[x][y] in ["X", "O"]: return
    hit = is_hit(enemy_board, x, y)
    player_display[x][y] = enemy_board[x][y] = "X" if hit else "O"
    is_ship_sunk(enemy_board, x, y, player_display)
    if all_ships_sunk(enemy_board):
        messagebox.showinfo("Победа", "Вы потопили все корабли противника!")
        game_over = True
        for i in range(10):
            for j in range(10): enemy_buttons[i][j].config(state="disabled")
    elif not hit:
        for i in range(10):
            for j in range(10): enemy_buttons[i][j].config(state="disabled")
        root.after(500, bot_turn)
    update_ui()

def bot_turn():
    global player_board, bot_display, bot_hits, bot_targets, bot_mode, game_over
    if game_over: return
    if bot_mode == "hunt" and bot_hits:
        x, y = bot_hits[-1]
        for dx, dy in random.sample([(0, 1), (1, 0), (0, -1), (-1, 0)], 4):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and bot_display[nx][ny] == "~": bot_targets = [(nx, ny)]; break
        else:
            bot_mode = "search"; bot_hits.pop()
    if bot_mode == "search":
        bot_targets = [(i, j) for i in range(10) for j in range(10) if
                       bot_display[i][j] == "~" and (i + j) % 2 == 0] or [(i, j) for i in range(10) for j in range(10)
                                                                          if bot_display[i][j] == "~"]
    if not bot_targets: return
    x, y = random.choice(bot_targets); bot_targets.remove((x, y)); hit = is_hit(player_board, x, y)
    bot_display[x][y] = player_board[x][y] = "X" if hit else "O"; is_ship_sunk(player_board, x, y, bot_display)
    if hit: bot_hits.append((x, y)); bot_mode = "hunt"
    if all_ships_sunk(player_board):
        messagebox.showinfo("Поражение", "Бот потопил все ваши корабли!")
        game_over = True
    elif not hit:
        for i in range(10):
            for j in range(10): enemy_buttons[i][j].config(state="normal")
    else:
        root.after(500, bot_turn)
    update_ui()

def create_ui():
    global root, player_buttons, enemy_buttons, size_var, dir_var, ships_label
    pf = tk.Frame(root); pf.grid(row=0, column=0, padx=10); ef = tk.Frame(root); ef.grid(row=0, column=1, padx=10); tk.Label(pf, text="Ваше поле").grid(row=0, column=0, columnspan=11); tk.Label(ef, text="Поле бота").grid(row=0, column=0, columnspan=11)
    for i in range(10):
        tk.Label(pf, text=str(i)).grid(row=i + 2, column=0); tk.Label(pf, text=str(i)).grid(row=1, column=i + 1); tk.Label(ef, text=str(i)).grid(row=i + 2, column=0); tk.Label(ef, text=str(i)).grid(row=1, column=i + 1); pr, er = [], []
        for j in range(10):
            btn = tk.Button(pf, width=2, height=1, command=lambda x=i, y=j: place_ship_click(x, y)); btn.grid(row=i + 2, column=j + 1); pr.append(btn); btn = tk.Button(ef, width=2, height=1, command=lambda x=i, y=j: player_turn(x, y), state="disabled"); btn.grid(row=i + 2, column=j + 1); er.append(btn)
        player_buttons.append(pr); enemy_buttons.append(er)
    cf = tk.Frame(root); cf.grid(row=1, column=0, columnspan=2, pady=5); ships_label = tk.Label(cf, text=""); ships_label.grid(row=0, column=0, columnspan=2)
    tk.Label(cf, text="Размер:").grid(row=1, column=0); size_var = tk.StringVar(value=str(ships[0])); tk.OptionMenu(cf, size_var, *sorted(set(ships), reverse=True)).grid(row=1, column=1)
    tk.Label(cf, text="Направление:").grid(row=1, column=2); dir_var = tk.StringVar(value="Горизонтально"); tk.OptionMenu(cf, dir_var, "Горизонтально", "Вертикально").grid(row=1, column=3); update_ui()

def main():
    global root, player_board, enemy_board, player_display, bot_display; root = tk.Tk(); root.title("Морской бой")
    player_board, enemy_board, player_display, bot_display = create_board(), create_board(), create_board(), create_board(); setup_bot_ships(); create_ui(); root.mainloop()

if __name__ == "__main__":
    main()
