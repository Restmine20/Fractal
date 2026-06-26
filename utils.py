import global_objects
import cupy
import numpy as np
from PIL import Image, ImageTk
from math import ceil
from tkinter import Event


def recalculate() -> None:
    """
    Перерисовывает фрактал на экране
    :return: None
    """
    w, h = global_objects.fractal_canvas.winfo_width(), global_objects.fractal_canvas.winfo_height()

    device_pixels = cupy.zeros(
        (h, w, 3),
        dtype=cupy.uint8)

    global_objects.fractals_functions_list[global_objects.current_fractal_idx.get()](
        (ceil(w / global_objects.block_size), ceil(h / global_objects.block_size), 1),

        (global_objects.block_size, global_objects.block_size, 1),

        (
            device_pixels,
            np.int32(global_objects.red.get()), np.int32(global_objects.green.get()), np.int32(global_objects.blue.get()),
            np.float64(global_objects.start_re.get()), np.float64(global_objects.start_im.get()),
            np.int32(global_objects.max_iters), np.float64(global_objects.stop_norm),
            np.float64(global_objects.scale_x), np.float64(global_objects.scale_y),
            np.float64(global_objects.len_shift_x), np.float64(global_objects.len_shift_y),
            np.float64(global_objects.len_width), np.float64(global_objects.len_height),
            np.int32(w), np.int32(h)
        )
    )

    fractal_pixels = cupy.asnumpy(device_pixels)

    fractal_image = Image.fromarray(fractal_pixels, "RGB")

    global_objects.fractal_canvas.image = ImageTk.PhotoImage(fractal_image)
    global_objects.fractal_canvas.create_image(0, 0, anchor="nw", image=global_objects.fractal_canvas.image)


def clear() -> None:
    """
    Очищает полотно фрактала; рисует фрактал базовой конфигурации
    :return: None
    """
    global_objects.current_fractal_idx.set(0)
    global_objects.scale_x, global_objects.scale_y = 1, 1
    global_objects.len_shift_x, global_objects.len_shift_y = 0, 0
    global_objects.len_width, global_objects.len_height = 4, 4
    global_objects.red.set(5)
    global_objects.green.set(5)
    global_objects.blue.set(5)
    global_objects.start_re.set(0.0)
    global_objects.start_im.set(0.0)

    recalculate()


def on_click(event: Event) -> None:
    """
    Фиксирует начало выбора прямоугольника для приближения
    :param event: событие нажатия ЛКМ
    :return: None
    """

    global_objects.rect_start_x, global_objects.rect_start_y = event.x, event.y

    if global_objects.selection_rect:
        global_objects.fractal_canvas.delete(global_objects.selection_rect)

    global_objects.selection_rect = global_objects.fractal_canvas.create_rectangle(
        event.x, event.y, event.x, event.y, outline="white")


def on_drag(event: Event) -> None:
    """
    Перерисовывает границу зоны приближения после движения мыши
    :param event: событие движения мыши с зажатой ЛКМ
    :return: None
    """
    if global_objects.selection_rect:
        global_objects.fractal_canvas.coords(
            global_objects.selection_rect, global_objects.rect_start_x, global_objects.rect_start_y, event.x, event.y)


def on_release(event: Event) -> None:
    """
    Начинает перерасчет факториала в выбранной зоне
    :param event: событие отпускания ЛКМ
    :return: None
    """
    if not global_objects.selection_rect:
        return

    end_x, end_y = event.x, event.y

    if global_objects.rect_start_x == end_x or global_objects.rect_start_y == end_y:
        global_objects.fractal_canvas.delete(global_objects.selection_rect)
        global_objects.selection_rect = None

        return

    x1, x2 = min(global_objects.rect_start_x, end_x), max(global_objects.rect_start_x, end_x)
    y1, y2 = min(global_objects.rect_start_y, end_y), max(global_objects.rect_start_y, end_y)

    w = global_objects.fractal_canvas.winfo_width()
    h = global_objects.fractal_canvas.winfo_height()

    global_objects.len_shift_x += x1 * global_objects.scale_x / w * global_objects.len_width
    global_objects.len_shift_y += y1 * global_objects.scale_y / h * global_objects.len_height

    global_objects.scale_x *= (x2 - x1) / w
    global_objects.scale_y *= (y2 - y1) / h

    global_objects.fractal_canvas.delete(global_objects.selection_rect)
    global_objects.selection_rect = None

    recalculate()
