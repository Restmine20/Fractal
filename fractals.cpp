// Подключаем CUDA-совместимый класс комплексных чисел
#include <cuda/std/complex>

// Используем псевдоним для удобства
using GPUComplex = cuda::std::complex<double>;

/// <summary>
/// Принимает координаты точки (в пикселях) на отрисовываемом экране,
/// возвращает комплексное число на плоскости, связанной с начальным экраном (без приближения)
/// </summary>
/// 
/// <param name="pixel_x"> Координата точки на экране по оси X (в пикселях) </param>
/// <param name="pixel_y"> Координата точки на экране по оси Y (в пикселях) </param>
/// 
/// <param name="scale_x"> Коэффициент приближения по оси X </param>
/// <param name="scale_y"> Коэффициент приближения по оси Y </param>
/// 
/// <param name="len_shift_x"> Сдвиг окна (относительно начального) по оси X </param>
/// <param name="len_shift_y"> Сдвиг окна (относительно начального) по оси Y </param>
/// 
/// <param name="len_width"> Длина окна по оси X </param>
/// <param name="len_height"> Длина окна по оси Y </param>
/// 
/// <param name="pixel_width"> Длина окна по оси X (в пикселях) </param>
/// <param name="pixel_height"> Длина окна по оси Y (в пикселях) </param>
/// 
/// <returns> Комплексное число, соответствующее переданной точке </returns>
__device__ GPUComplex screen_to_complex(
	int pixel_x, int pixel_y,

	double scale_x, double scale_y,
	double len_shift_x, double len_shift_y,
	double len_width, double len_height,
	int pixel_width, int pixel_height)
{
	return {
		-len_width / 2 + pixel_x * scale_x / pixel_width * len_width + len_shift_x,
		len_height / 2 - pixel_y * scale_y / pixel_height * len_height + len_shift_y
	};
}


/// <summary>
/// Рисует множество Мандельброта на переданной поверхности с указанными параметрами
/// </summary>
/// <param name="surface"> Указатель на поверхность для отрисовки точек множества </param>
/// 
/// <param name="red"> Параметр, отвечающий за КРАСНУЮ составляющую цвета </param>
/// <param name="green"> Параметр, отвечающий за ЗЕЛЕНУЮ составляющую цвета </param>
/// <param name="blue"> Параметр, отвечающий за СИНЮЮ составляющую цвета </param>
/// 
/// <param name="start_re"> Вещественная часть стартовой точки последовательности </param>
/// <param name="start_im"> Мнимая часть стартовой точки последовательности </param>
/// 
/// <param name="max_iters"> Ограничение числа проверяемых точек последовательности </param>
/// <param name="stop_norm"> Минимальное значение квадрата модуля числа, при котором оно считается не принадлежащим множеству </param>
/// 
/// <param name="scale_x"> Коэффициент приближения по оси X </param>
/// <param name="scale_y"> Коэффициент приближения по оси Y </param>
/// 
/// <param name="len_shift_x"> Сдвиг окна (относительно начального) по оси X </param>
/// <param name="len_shift_y"> Сдвиг окна (относительно начального) по оси Y </param>
/// 
/// <param name="len_width"> Длина окна по оси X </param>
/// <param name="len_height"> Длина окна по оси Y </param>
/// 
/// <param name="pixel_width"> Длина окна по оси X (в пикселях) </param>
/// <param name="pixel_height"> Длина окна по оси Y (в пикселях) </param>
/// 
/// <returns></returns>
__global__ void mandelbrot(
	char* surface,
	int red, int green, int blue,
	double start_re, double start_im,
	int max_iters, double stop_norm,

	double scale_x, double scale_y,
	double len_shift_x, double len_shift_y,
	double len_width, double len_height,
	int pixel_width, int pixel_height
)
{

	const int pixel_x = blockIdx.x * blockDim.x + threadIdx.x;
	const int pixel_y = blockIdx.y * blockDim.y + threadIdx.y;

	if (pixel_x >= pixel_width || pixel_y >= pixel_height) return;

	GPUComplex base = screen_to_complex(
		pixel_x, pixel_y,
		scale_x, scale_y,
		len_shift_x, len_shift_y,
		len_width, len_height,
		pixel_width, pixel_height
	);

	GPUComplex cur(start_re, start_im);

	int index = 3 * (pixel_width * pixel_y + pixel_x);

	for (int i = 0; i < max_iters; i++) {
		if (cuda::std::norm(cur) > stop_norm) {
			surface[index] = (red * i) % 255;
			surface[index + 1] = (green * i) % 255;
			surface[index + 2] = (blue * i) % 255;
			return;
		}
		cur = cur * cur + base;
	}
	surface[index] = 0;
	surface[index + 1] = 0;
	surface[index + 2] = 0;
}


/// <summary>
/// Рисует множество Жюлиа на переданной поверхности с указанными параметрами
/// </summary>
/// <param name="surface"> Указатель на поверхность для отрисовки точек множества </param>
/// 
/// <param name="red"> Параметр, отвечающий за КРАСНУЮ составляющую цвета </param>
/// <param name="green"> Параметр, отвечающий за ЗЕЛЕНУЮ составляющую цвета </param>
/// <param name="blue"> Параметр, отвечающий за СИНЮЮ составляющую цвета </param>
/// 
/// <param name="start_re"> Вещественная часть стартовой точки последовательности </param>
/// <param name="start_im"> Мнимая часть стартовой точки последовательности </param>
/// 
/// <param name="max_iters"> Ограничение числа проверяемых точек последовательности </param>
/// <param name="stop_norm"> Минимальное значение квадрата модуля числа, при котором оно считается не принадлежащим множеству </param>
/// 
/// <param name="scale_x"> Коэффициент приближения по оси X </param>
/// <param name="scale_y"> Коэффициент приближения по оси Y </param>
/// 
/// <param name="len_shift_x"> Сдвиг окна (относительно начального) по оси X </param>
/// <param name="len_shift_y"> Сдвиг окна (относительно начального) по оси Y </param>
/// 
/// <param name="len_width"> Длина окна по оси X </param>
/// <param name="len_height"> Длина окна по оси Y </param>
/// 
/// <param name="pixel_width"> Длина окна по оси X (в пикселях) </param>
/// <param name="pixel_height"> Длина окна по оси Y (в пикселях) </param>
/// 
/// <returns></returns>
__global__ void julia(
	char* surface,
	int red, int green, int blue,
	double start_re, double start_im,
	int max_iters, double stop_norm,

	double scale_x, double scale_y,
	double len_shift_x, double len_shift_y,
	double len_width, double len_height,
	int pixel_width, int pixel_height
)
{
	const int pixel_x = blockIdx.x * blockDim.x + threadIdx.x;
	const int pixel_y = blockIdx.y * blockDim.y + threadIdx.y;

	if (pixel_x >= pixel_width || pixel_y >= pixel_height) return;

	GPUComplex cur = screen_to_complex(
		pixel_x, pixel_y,
		scale_x, scale_y,
		len_shift_x, len_shift_y,
		len_width, len_height,
		pixel_width, pixel_height
	);

	GPUComplex base(start_re, start_im);

	int index = 3 * (pixel_width * pixel_y + pixel_x);

	for (int i = 0; i < max_iters; i++) {
		if (cuda::std::norm(cur) > stop_norm) {
			surface[index] = (red * i) % 255;
			surface[index + 1] = (green * i) % 255;
			surface[index + 2] = (blue * i) % 255;
			return;
		}
		cur = cur * cur + base;
	}
	surface[index] = 0;
	surface[index + 1] = 0;
	surface[index + 2] = 0;
}