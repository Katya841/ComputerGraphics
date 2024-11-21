import tkinter as tk
from tkinter import messagebox
import math


def naive_line(x0, y0, x1, y1):
    steps = max(abs(x1 - x0), abs(y1 - y0))
    x_increment = (x1 - x0) / steps
    y_increment = (y1 - y0) / steps
    x, y = x0, y0
    for _ in range(steps + 1):
        yield round(x), round(y)
        x += x_increment
        y += y_increment


def dda_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0
    for _ in range(steps + 1):
        yield round(x), round(y)
        x += x_inc
        y += y_inc


def bresenham_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    if dx > dy:
        err = dx / 2.0
        while x0 != x1:
            yield x0, y0
            x0 += sx
            err -= dy
            if err < 0:
                y0 += sy
                err += dx
    else:
        err = dy / 2.0
        while y0 != y1:
            yield x0, y0
            y0 += sy
            err -= dx
            if err < 0:
                x0 += sx
                err += dy
    yield x1, y1


def bresenham_circle(xc, yc, radius):
    x, y = 0, radius
    d = 3 - 2 * radius
    while x <= y:
        yield xc + x, yc + y
        yield xc - x, yc + y
        yield xc + x, yc - y
        yield xc - x, yc - y
        yield xc + y, yc + x
        yield xc - y, yc + x
        yield xc + y, yc - x
        yield xc - y, yc - x
        if d <= 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1


class LineRasterizationApp:
    def __init__(self, root, cell_size=20, grid_width=30, grid_height=20):
        self.root = root
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.current_algorithm = "Naive"

        
        self.canvas = tk.Canvas(
            root,
            width=self.grid_width * self.cell_size,
            height=self.grid_height * self.cell_size,
            bg="white"
        )
        self.canvas.grid(row=0, column=0, columnspan=4)

        
        self.cells = {}
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    outline="gray", fill="white"
                )
                self.cells[(x, y)] = rect

        
        tk.Label(root, text="Начальная точка (x, y):").grid(row=1, column=0, sticky="e")
        self.start_x_entry = tk.Entry(root, width=5)
        self.start_x_entry.grid(row=1, column=1)
        self.start_y_entry = tk.Entry(root, width=5)
        self.start_y_entry.grid(row=1, column=2)

        tk.Label(root, text="Конечная точка (x, y):").grid(row=2, column=0, sticky="e")
        self.end_x_entry = tk.Entry(root, width=5)
        self.end_x_entry.grid(row=2, column=1)
        self.end_y_entry = tk.Entry(root, width=5)
        self.end_y_entry.grid(row=2, column=2)

        tk.Label(root, text="Радиус:").grid(row=3, column=0, sticky="e")
        self.radius_entry = tk.Entry(root, width=5, state="disabled")
        self.radius_entry.grid(row=3, column=1)

        
        self.algorithm_menu = tk.StringVar(value="Naive")
        self.algorithm_dropdown = tk.OptionMenu(
            root, self.algorithm_menu, "Naive", "DDA", "Bresenham", "Circle Bresenham", command=self.update_ui)
        self.algorithm_dropdown.grid(row=4, column=0, columnspan=2)

        self.draw_button = tk.Button(root, text="Построить", command=self.draw_line)
        self.draw_button.grid(row=4, column=2, columnspan=2)

        self.reset_button = tk.Button(root, text="Очистить", command=self.reset_grid)
        self.reset_button.grid(row=5, column=0, columnspan=4)

    def highlight_cell(self, x, y, color):
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            rect = self.cells.get((x, y))
            if rect:
                self.canvas.itemconfig(rect, fill=color)

    def update_ui(self, algorithm):
        
        if algorithm == "Circle Bresenham":
            self.radius_entry.config(state="normal")
            self.end_x_entry.config(state="disabled")
            self.end_y_entry.config(state="disabled")
        else:
            self.radius_entry.config(state="disabled")
            self.end_x_entry.config(state="normal")
            self.end_y_entry.config(state="normal")

    def draw_line(self):
        try:
            algorithm = self.algorithm_menu.get()
            start_x = int(self.start_x_entry.get())
            start_y = int(self.start_y_entry.get())

            if algorithm == "Circle Bresenham":
                radius = int(self.radius_entry.get())
                self.reset_grid()
                for x, y in bresenham_circle(start_x, start_y, radius):
                    self.highlight_cell(x, y, "blue")
            else:
                end_x = int(self.end_x_entry.get())
                end_y = int(self.end_y_entry.get())
                self.reset_grid()

                if algorithm == "Naive":
                    generator = naive_line(start_x, start_y, end_x, end_y)
                elif algorithm == "DDA":
                    generator = dda_line(start_x, start_y, end_x, end_y)
                elif algorithm == "Bresenham":
                    generator = bresenham_line(start_x, start_y, end_x, end_y)
                else:
                    raise ValueError("Неизвестный алгоритм.")

                for x, y in generator:
                    self.highlight_cell(x, y, "blue")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверные данные: {e}")

    def reset_grid(self):
        for rect in self.cells.values():
            self.canvas.itemconfig(rect, fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Растеризация линий и окружностей")
    app = LineRasterizationApp(root)
    root.mainloop()
