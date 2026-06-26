import tkinter as tk
from gpu_initialize import module


root = tk.Tk()


""" Зона технических параметров """
scale_x, scale_y = 1, 1
len_shift_x, len_shift_y = 0, 0
len_width, len_height = 4, 4
max_iters, stop_norm = 500, 4
current_fractal_idx = tk.IntVar(value=0)
block_size = 16
rect_start_x, rect_start_y = None, None
selection_rect = None


""" Зона объектов окна Tkinter """
ui_frame = tk.Frame(root, bg="#323232")
ui_frame.pack(side="left", fill="y")

fractal_canvas = tk.Canvas(root, bg="#000000", highlightthickness=0)
fractal_canvas.pack(side="right", expand=True, fill="both")


""" Зона пользовательских параметров """
red, green, blue = tk.IntVar(value=5), tk.IntVar(value=5), tk.IntVar(value=5)
start_re, start_im = tk.DoubleVar(value=0.0), tk.DoubleVar(value=0.0)


""" Зона регистрации фракталов """
fractals_names_list = ["Множество Мандельброта", "Множество Жюлиа"]
fractals_functions_list = [module.get_function("mandelbrot"), module.get_function("julia")]