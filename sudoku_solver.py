import tkinter as tk
from tkinter import messagebox

# ---------------- Sudoku Solver Logic ----------------
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, num, pos):
    row, col = pos

    # Check row
    for j in range(9):
        if board[row][j] == num and col != j:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num and row != i:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

# ---------------- GUI Section ----------------
class SudokuGUI:
    def __init__(self, root, initial_board=None):
        self.root = root
        self.root.title("Sudoku Solver - Backtracking")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.fixed_cells = set()

        # Create 9x9 grid of entry boxes
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(root, width=3, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=3, pady=3)

                # Add thicker borders to separate 3x3 boxes
                if i % 3 == 0 and i != 0:
                    entry.grid(pady=(10, 3))
                if j % 3 == 0 and j != 0:
                    entry.grid(padx=(10, 3))

                self.entries[i][j] = entry

        # Single Solve Button
        solve_btn = tk.Button(root, text="Solve Sudoku", command=self.solve_gui,
                              bg="lightgreen", font=("Arial", 12, "bold"))
        solve_btn.grid(row=9, column=0, columnspan=9, sticky="we", pady=10)

        # Load initial board if given
        if initial_board:
            self.set_board(initial_board)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            row.append(0)
                    except:
                        row.append(0)
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                if board[i][j] != 0:
                    entry.insert(0, str(board[i][j]))
                    entry.config(fg="blue", state="disabled")  # fixed cells
                    self.fixed_cells.add((i, j))
                else:
                    entry.config(state="normal", fg="black")

    def solve_gui(self):
        board = self.get_board()
        if solve(board):
            self.set_board(board)
            messagebox.showinfo("Sudoku Solver", "Sudoku Solved Successfully!")
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists!")

# ---------------- Main Program ----------------
if __name__ == "__main__":
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9] ]

    root = tk.Tk()
    gui = SudokuGUI(root, puzzle)
    root.mainloop()

