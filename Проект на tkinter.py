import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

import numpy as np

import pygame
import sys
from pygame.color import THECOLORS

from tkinter import *

global height, width, d_x, d_y, re_len, im_len, r, g, b, last_func
re_len, im_len, d_x, d_y = 4, 4, 0, 0
height, width = 600, 600
last_func = "mandelbrot"

def choose_function():
    if last_func == "mandelbrot":
        mandelbrot(
            drv.Out(surface), np.float64(d_x), np.float64(d_y), np.float64(re_len), np.float64(im_len),
            np.int32(width), np.int32(height), np.int32(r.get()), np.int32(g.get()), np.int32(b.get()),np.float64(c_re.get()), np.float64(c_im.get()),
            block=(6, 6, 1), grid=(100, 100))
        pygame.surfarray.blit_array(surf, surface)
        screen.blit(surf, (0, 0))
    elif last_func == "julia":
        julia(
            drv.Out(surface), np.float64(d_x), np.float64(d_y), np.float64(re_len), np.float64(im_len),
            np.int32(width), np.int32(height), np.int32(r.get()), np.int32(g.get()), np.int32(b.get()), np.float64(c_re.get()), np.float64(c_im.get()),
            block=(6, 6, 1), grid=(100, 100))
        pygame.surfarray.blit_array(surf, surface)
        screen.blit(surf, (0, 0))

def screen_to_complex(x, y, d_x, d_y, re_len, im_len):
    return complex(((x*(re_len/4)+d_x) - width / 2) / (width / 4), (height / 2 - (y*(im_len/4) + d_y)) / (height / 4))
class complex:
    def __init__(self, a, b):
        self.re = a
        self.im = b
    def __add__(self, z2):
        return complex(self.re + z2.re, self.im + z2.im)

    def __sub__(self, z2):
        return complex(self.re - z2.re, self.im - z2.im)

    def __mul__(self, z2):
        return complex(self.re * z2.re - self.im * z2.im, self.re * z2.im + self.im * z2.re)

    def __truediv__(self, z2):
        return complex((self.re * z2.re + self.im * z2.im) / (z2.re ** 2 + z2.im ** 2), (z2.re * self.im - self.re * z2.im) / (z2.re ** 2 + z2.im ** 2))

    def abs_in_pow_2(self):
        return self.re ** 2 + self.im ** 2


def mandelbrot_button():
    global last_func
    last_func = "mandelbrot"
    choose_function()
def julia_button():
    global last_func
    last_func = "julia"
    choose_function()
def rscale(newVal):
    choose_function()
def gscale(newVal):
    choose_function()
def bscale(newVal):
    choose_function()
def clear():
    global d_x, d_y, re_len, im_len, r, g, b, c_re, c_im
    re_len, im_len, d_x, d_y = 4, 4, 0, 0
    r.set(5)
    g.set(5)
    b.set(5)
    c_re.set(0.0)
    c_im.set(0.0)
    choose_function()

def crescale(newVal):
    choose_function()
def cimscale(newVal):
    choose_function()

pygame.init()

tk = Tk()
tk.geometry("400x600")

r, g, b = IntVar(value=5), IntVar(value=5), IntVar(value=5)
c_re, c_im = DoubleVar(value=0.0), DoubleVar(value=0.0)

btn_mandelbrot = Button(text="Множество Мандельброта", width = 50, command=mandelbrot_button)
btn_julia = Button(text="Множество Жюлиа", width = 50, command=julia_button)
btn_clean = Button(text="Сброс", bg = 'red', command=clear)


btn_mandelbrot.place(x = 100, y = 20, width = 200, height = 30)
btn_julia.place(x = 100, y = 60, width = 200, height = 30)
btn_clean.place(x = 160, y = 550, width = 80, height = 30)

scale_r = Scale(from_= 1, to=100, variable=r, orient = "horizontal", command= rscale)
scale_g = Scale(from_= 1, to=100, variable=g, orient = "horizontal", command = gscale)
scale_b = Scale(from_= 1, to=100, variable=b, orient = "horizontal", command = bscale)

scale_cre = Scale(from_= -1, to=1, variable=c_re, orient = "horizontal", resolution=0.01, command = crescale)
scale_cim = Scale(from_= -1, to=1, variable=c_im, orient = "horizontal", resolution=0.01, command = cimscale)


scale_r.place(x = 100, y = 120, width = 250)
scale_g.place(x = 100, y = 160, width = 250)
scale_b.place(x = 100, y = 200, width = 250)
scale_cre.place(x = 100, y = 340, width = 250)
scale_cim.place(x = 100, y = 380, width = 250)

label_r = Label(text = "r")
label_g = Label(text = "g")
label_b = Label(text = "b")
label_cre = Label(text = "Re(c)")
label_cim = Label(text = "Im(c)")


label_r.place(x = 80, y = 135)
label_g.place(x = 80, y = 175)
label_b.place(x = 80, y = 215)
label_cre.place(x = 70, y = 355)
label_cim.place(x = 70, y = 395)

screen = pygame.display.set_mode((width, height))
screen.fill(THECOLORS['white'])

surf = pygame.Surface((width, height))
surf.fill(THECOLORS['white'])


mod = SourceModule("""
class complex{
public:
  double re, im;
  __device__ complex(double re, double im){
    this->re = re;
    this->im = im;
  }
  
  __device__ complex operator* (complex z){
    return complex(this->re * z.re - this->im * z.im, this->re*z.im + this->im*z.re);
  }
  __device__ complex operator+ (complex z){
    return complex(this->re + z.re, this->im+ z.im);
  }
  __device__ double abs_in_pow_2(){
    return this->re * this->re + this-> im * this->im;
  }
};
__device__ complex screen_to_complex(int x, int y, double d_x, double d_y, double re_len, double im_len, int width, int height){
  return complex(((x*(re_len/4)+d_x) - width / 2) / (width / 4), (height / 2 - (y*(im_len/4) + d_y)) / (height / 4));
}
__global__ void mandelbrot(char *surface, double d_x, double d_y, double re_len, double im_len, int width, int height, int r, int g, int b, double z_re, double z_im){

  const int x = blockIdx.x * blockDim.x + threadIdx.x;
  const int y = blockIdx.y * blockDim.y + threadIdx.y;
  
  complex c = screen_to_complex(x, y, d_x, d_y, re_len, im_len, width, height);
  complex z(z_re, z_im);
    
  for (int i = 0; i < 2000; i++){
    if (z.abs_in_pow_2() > 4){
      surface[(600*x + y)*3  ] = (r*i)%255;
      surface[(600*x + y)*3+1] = (g*i)%255;
      surface[(600*x + y)*3+2] = (b*i)%255;
      return;
    }
    surface[(600*x + y)*3  ] = 0;
    surface[(600*x + y)*3+1] = 0;
    surface[(600*x + y)*3+2] = 0;
    z = z*z + c;
  }
}
__global__ void julia(char *surface, double d_x, double d_y, double re_len, double im_len, int width, int height, int r, int g, int b, double c_re, double c_im){

  const int x = blockIdx.x * blockDim.x + threadIdx.x;
  const int y = blockIdx.y * blockDim.y + threadIdx.y;
  
  complex c(c_re, c_im);
  complex z = screen_to_complex(x, y, d_x, d_y, re_len, im_len, width, height);
    
  for (int i = 0; i < 2000; i++){
    if (z.abs_in_pow_2() > 4){
      surface[(600*x + y)*3  ] = (r*i + r)%255;
      surface[(600*x + y)*3+1] = (g*i + g)%255;
      surface[(600*x + y)*3+2] = (b*i + b)%255;
      return;
    }
    surface[(600*x + y)*3  ] = 0;
    surface[(600*x + y)*3+1] = 0;
    surface[(600*x + y)*3+2] = 0;
    z = z*z + c;
  }
}


""")

mandelbrot = mod.get_function("mandelbrot")
julia = mod.get_function("julia")

surface = np.zeros([600, 600, 3], np.uint8)

choose_function()

pygame.surfarray.blit_array(surf, surface)
screen.blit(surf, (0, 0))

pygame.display.flip()

rectang_coord = [0, 0]
start_draw = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            rectang_coord[0] = event.pos
            start_draw = True


        elif event.type == pygame.MOUSEMOTION:
            if start_draw:
                rectang_coord[1] = event.pos
                rect_width = rectang_coord[1][0] - rectang_coord[0][0]
                rect_height = rectang_coord[1][1] - rectang_coord[0][1]


                rectangle = pygame.Rect(rectang_coord[0][0], rectang_coord[0][1], rect_width, rect_height)


                if rect_width < 0 and rect_height < 0:
                    rectangle = pygame.Rect(rectang_coord[0][0]-abs(rect_width), rectang_coord[0][1] - abs(rect_height), abs(rect_width), abs(rect_height))
                elif rect_height < 0:
                    rectangle = pygame.Rect(rectang_coord[0][0], rectang_coord[0][1] - abs(rect_height), rect_width, abs(rect_height))
                elif rect_width < 0:
                    rectangle = pygame.Rect(rectang_coord[0][0]-abs(rect_width), rectang_coord[0][1], abs(rect_width), rect_height)


                screen.blit(surf, (0, 0))
                pygame.draw.rect(screen, pygame.Color(THECOLORS['white']), rectangle, 1)
                pygame.display.flip()

        elif event.type == pygame.MOUSEBUTTONUP:
            start_draw = False
            if rectang_coord[1] != 0:

                re_lenf, im_lenf = re_len, im_len
                re_len = (screen_to_complex(rectangle.topright[0], rectangle.topright[1], d_x, d_y, re_lenf, im_lenf) - screen_to_complex(rectangle.topleft[0], rectangle.topleft[1], d_x, d_y, re_lenf, im_lenf)).re
                im_len = (screen_to_complex(rectangle.topright[0], rectangle.topright[1], d_x, d_y, re_lenf, im_lenf) - screen_to_complex(rectangle.bottomright[0], rectangle.bottomright[1], d_x, d_y, re_lenf, im_lenf)).im


                d_x += rectangle.topleft[0]*(re_lenf/4)
                d_y += rectangle.topleft[1]*(im_lenf/4)

                choose_function()

                pygame.surfarray.blit_array(surf, surface)
                screen.blit(surf, (0, 0))
                rectang_coord = [0, 0]


    pygame.display.update()
    tk.update()