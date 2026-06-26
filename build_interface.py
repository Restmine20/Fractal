import global_objects
import utils
import tkinter as tk

""" Зона переключения фракталов """
nav_frame = tk.Frame(global_objects.ui_frame, bg="#323232")
nav_frame.pack(padx=10, pady=20, fill="x")

btn_prev = tk.Button(nav_frame, text="<",
                     command=lambda: global_objects.current_fractal_idx.set(
                         (global_objects.current_fractal_idx.get() - 1) % len(global_objects.fractals_names_list)),
                     bg="#4a4a4a", fg="white", bd=0, width=3)
btn_prev.pack(side="left")

fractal_label = tk.Label(nav_frame, text=global_objects.fractals_names_list[global_objects.current_fractal_idx.get()],
                         bg="#222222", fg="white", height=2)
fractal_label.pack(side="left", fill="x", expand=True, padx=5)

btn_next = tk.Button(nav_frame, text=">",
                     command=lambda: global_objects.current_fractal_idx.set(
                         (global_objects.current_fractal_idx.get() + 1) % len(global_objects.fractals_names_list)),
                     bg="#4a4a4a", fg="white", bd=0, width=3)
btn_next.pack(side="right")

""" Зона ползунков """
scale_red = tk.Scale(global_objects.ui_frame, from_=1, to=100, variable=global_objects.red,
                     orient="horizontal", showvalue=True, label="Красный")
scale_red.pack(padx=10, pady=(0, 10), fill="x")

scale_green = tk.Scale(global_objects.ui_frame, from_=1, to=100, variable=global_objects.green,
                       orient="horizontal", showvalue=True, label="Зеленый")
scale_green.pack(padx=10, pady=(0, 10), fill="x")

scale_blue = tk.Scale(global_objects.ui_frame, from_=1, to=100, variable=global_objects.blue,
                      orient="horizontal", showvalue=True, label="Синий")
scale_blue.pack(padx=10, pady=(0, 10), fill="x")

scale_start_re = tk.Scale(global_objects.ui_frame, from_=-1, to=1, variable=global_objects.start_re,
                          orient="horizontal", resolution=0.01, showvalue=True, label="Re(start)")
scale_start_re.pack(padx=10, pady=(0, 10), fill="x")

scale_start_im = tk.Scale(global_objects.ui_frame, from_=-1, to=1, variable=global_objects.start_im,
                          orient="horizontal", resolution=0.01, showvalue=True, label="Im(start)")
scale_start_im.pack(padx=10, pady=(0, 10), fill="x")

""" Зона кнопок перерисовки и очистки экрана """
btn_clean = tk.Button(global_objects.ui_frame, text="Сброс", bg="red", fg="white", command=utils.clear)
btn_clean.pack(side="bottom", padx=10, pady=20, fill="x")

btn_recalc = tk.Button(global_objects.ui_frame, text="Рисовать", bg="green", fg="white", command=utils.recalculate)
btn_recalc.pack(side="bottom", padx=10, pady=20, fill="x")

""" Зона регистрации команд и отслеживания переменных """
global_objects.red.trace_add("write", lambda *args: utils.recalculate())
global_objects.green.trace_add("write", lambda *args: utils.recalculate())
global_objects.blue.trace_add("write", lambda *args: utils.recalculate())
global_objects.start_re.trace_add("write", lambda *args: utils.recalculate())
global_objects.start_im.trace_add("write", lambda *args: utils.recalculate())
global_objects.current_fractal_idx.trace_add(
    "write",
    lambda *args: (
        fractal_label.config(text=global_objects.fractals_names_list[global_objects.current_fractal_idx.get()]),
        utils.recalculate())
)

global_objects.fractal_canvas.bind("<Button-1>", utils.on_click)
global_objects.fractal_canvas.bind("<B1-Motion>", utils.on_drag)
global_objects.fractal_canvas.bind("<ButtonRelease-1>", utils.on_release)
