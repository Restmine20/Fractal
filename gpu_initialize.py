import cupy
from tkinter import messagebox
import tkinter as tk
import sys


""" В этом блоке определяется архитектура видеокарты """
try:
    device = cupy.cuda.Device(0)
    gpu_arch = str(device.compute_capability)
except Exception as e:
    error_window = tk.Tk()
    error_window.withdraw()

    messagebox.showerror(
        "Ошибка",
        f"При открытии приложения возникла следующая ошибка: {e}"
    )

    sys.exit(1)

""" Путь к скомпилированному файлу, соответствующему текущей архитектуре """
bin_path = f"fractals_bin/fractals_sm_{gpu_arch}.cubin"

""" В этом блоке создается модуль для работы с видеокартой """
try:
    module = cupy.RawModule(path=bin_path)
except Exception as e:
    error_window = tk.Tk()
    error_window.withdraw()

    messagebox.showerror(
        "Ошибка",
        f"При открытии приложения возникла следующая ошибка: {e}"
    )

    sys.exit(1)
