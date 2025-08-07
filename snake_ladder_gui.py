import tkinter as tk
import random
from tkinter import messagebox

CELL_SIZE = 60
ROWS = 10
COLS = 10
BOARD_SIZE = CELL_SIZE * ROWS

snakes = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78
}

ladders = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100
}

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍🪜 Snake and Ladder Game")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg="lightyellow")
        self.canvas.pack()


        self.draw_board()
        self.create_players()

        self.turn = 0
        self.positions = [1, 1]

        self.dice_label = tk.Label(root, text="🎲 Dice: ", font=("Arial", 20), bg="lightgray")
        self.dice_label.pack(pady=10)

        self.roll_button = tk.Button(root, text="Roll Dice", font=("Arial", 16), command=self.roll_dice, bg="lightblue")
        self.roll_button.pack(pady=5)

        self.info_label = tk.Label(root, text="Player 1's turn (🔵)", font=("Arial", 14), bg="white")
        self.info_label.pack()

    def draw_board(self):
        colors = ["#DDEEFF", "#FFFFFF"]
        for i in range(ROWS):
            for j in range(COLS):
                x1 = j * CELL_SIZE
                y1 = (9 - i) * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = colors[(i + j) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                number = i * 10 + (j + 1) if i % 2 == 0 else i * 10 + (10 - j)
                self.canvas.create_text(x1 + 30, y1 + 30, text=str(number), font=("Arial", 10, "bold"))

        # Draw ladders – bold green lines
        for start, end in ladders.items():
            x1, y1 = self.get_cell_center(start)
            x2, y2 = self.get_cell_center(end)
            self.canvas.create_line(x1, y1, x2, y2, fill="darkgreen", width=6)

        # Draw snakes – bold red lines
        for start, end in snakes.items():
            x1, y1 = self.get_cell_center(start)
            x2, y2 = self.get_cell_center(end)
            self.canvas.create_line(x1, y1, x2, y2, fill="darkred", width=5, dash=(4, 2))

    def create_players(self):
        self.player1 = self.canvas.create_oval(10, BOARD_SIZE - 50, 30, BOARD_SIZE - 30, fill="blue")
        self.player2 = self.canvas.create_oval(35, BOARD_SIZE - 50, 55, BOARD_SIZE - 30, fill="red")

    def get_coords(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        x = col * CELL_SIZE + 10 + self.turn * 25
        y = (9 - row) * CELL_SIZE + 10
        return x, y

    def get_cell_center(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = (9 - row) * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def move_player(self, player, pos):
        x, y = self.get_coords(pos)
        self.canvas.coords(player, x, y, x + 20, y + 20)

    def roll_dice(self):
        dice = random.randint(1, 6)
        self.dice_label.config(text=f"🎲 Dice: {dice}")

        player = self.turn
        pos = self.positions[player]

        pos += dice

        if pos > 100:
            pos = self.positions[player]
        else:
            if pos in snakes:
                messagebox.showinfo("🐍 Snake!", f"Oops! Player {player + 1} got bitten by a snake!")
                pos = snakes[pos]
            elif pos in ladders:
                messagebox.showinfo("🪜 Ladder!", f"Yay! Player {player + 1} climbed a ladder!")
                pos = ladders[pos]

        self.positions[player] = pos
        self.move_player(self.player1 if player == 0 else self.player2, pos)

        if pos == 100:
            messagebox.showinfo("🎉 Winner", f"Player {player + 1} wins the game!")
            self.root.quit()

        self.turn = 1 - self.turn
        next_player = f"Player {self.turn + 1} {'(🔵)' if self.turn == 0 else '(🔴)'}"
        self.info_label.config(text=f"{next_player}'s turn")

# Run game
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="lightgray")
    game = SnakeLadderGame(root)
    root.mainloop()
