import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk
from PIL import Image, ImageDraw

"""
Программа для создания изображений и сохранения их в формате *.png.
Графический интерфейс программы разработан на основе TKinter.Пользователь может рисовать на холсте, выбирать цвет
и размер кисти, очищать холст и сохранять в формате PNG.
"""


class DrawingApp:
    """Параметр:- root: Это корневой виджет Tkinter, который служит контейнером для всего интерфейса приложения.
    """

    def __init__(self, root):
        self.root = root  # корень
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        # холст
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()
        # установка
        self.setup_ui()
        # последний
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.text = None

        self.canvas.bind('<B1-Motion>', self.paint)  # холст связать с методом красить
        self.canvas.bind('<ButtonRelease-1>', self.reset)  # холст связать  со сбросом кнопки

        """Привязываем обработчик события <Button-3> к холсту, чтобы выбрать цвет"""
        self.canvas.bind('<Button-3>', self.pick_color)

        """Добавляем гарячую клавишу для сохранения изображения."""
        self.root.bind('<Control-s>', self.save_image)

        """Гарячая клавиша для выбора цвета."""
        self.root.bind('<Control-c>', self.choose_color)

        """Маленький холст-окно для предварительного просмотра текущего цвета"""
        self.preview_color = tk.Canvas(root, width=30, height=30, background=self.pen_color)
        self.preview_color.pack(side=tk.LEFT)

        """ Привязываем обработчик события <Button-1> к холсту, чтобы вставлять текст."""
        self.canvas.bind('<Button-1>', self.paste_text)

    def setup_ui(self):  # настройка
        """Этот метод отвечает за создание и расположение виджетов управления"""
        control_frame = tk.Frame(self.root)  # рамка
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)  # размер масштаб кисти

        """Добавлена кнопка для изменения размера холста"""
        change_canvas_button = tk.Button(control_frame, text="Изменить размер холста", command=self.change_size_canvas)
        change_canvas_button.pack(side=tk.LEFT)

        """Добавлена метка для размера кисти."""
        label = ttk.Label(control_frame, text='Размер кисти:')
        label.pack(side=tk.LEFT)


        """Выпадающее меню для выбора размера кисти"""
        sizes = ['1', '2', '5', '10']
        combo = ttk.OptionMenu(control_frame, self.brush_size_scale, sizes[0], *sizes)
        combo.pack(side=tk.LEFT)

        """Добавился ластик"""
        self.eraser_get_button = tk.Button(control_frame, text="Ластик", command=self.eraser_get)
        self.eraser_get_button.pack(side=tk.LEFT)

        """Вернуться к рисованию"""
        self.brush_button = tk.Button(control_frame, text="Кисть", command=self.brush)
        self.brush_button.pack(side=tk.LEFT)

        """Кнопка 'Добавить текст'."""
        self.text_button = tk.Button(control_frame, text="Ввести текст", command=self.add_text)
        self.text_button.pack(side=tk.LEFT)

        """Кнопка для изменения цвета холста."""
        self.change_color_button = tk.Button(control_frame, text="Цвет холста", command=self.change_canvas_color)
        self.change_color_button.pack(side=tk.LEFT)
    def brushs_size(self):
        """
        Метод, отвечающий за выбор размера кисти из списка, а так же за список этих размеров
        :return: None
        """
        self.brush_size_scale.pack(side=tk.LEFT)

    def brush(self):
        """
        Метод выбора инструмента - "Кисть" возвращает к рисованию и выбору цвета.
        """
        self.pen_color = 'black'
        # self.choose_color()
        self.canvas.bind('<B1-Motion>', self.paint)

    def eraser_get(self):
        """Метод для работы ластика"""
        self.pen_color = 'white'
        self.canvas.bind('<ButtonRelease-1>', self.reset)


    def paint(self, event):
        """Функция вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует линии на холсте Tkinter
        и параллельно на объекте Image из Pillow:
        - event: Событие содержит координаты мыши, которые используются для рисования.
        - Линии рисуются между текущей и последней зафиксированной позициями курсора, что создает непрерывное изображение.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                            width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def pick_color(self, event):
        """ Функция "Пипетка", которая обновляет цвет пера на основе цвета пикселя изображения в координатах события.
        Args:
            self: Экземпляр класса DrawingApp.
            event: Событие, содержащее координаты пикселя в холсте."""
        self.pen_color = '#%02x%02x%02x' % self.image.getpixel((event.x, event.y))
        return self.pen_color

    def reset(self, event):
        """Сбрасывает последние координаты кисти. Это необходимо для корректного начала новой линии после того,
         как пользователь отпустил кнопку мыши и снова начал рисовать.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw для нового изображения.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.preview_color.configure(bg=self.pen_color)

    def save_image(self, event=None):
        """Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
         Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def change_size_canvas(self):
        """Функция для изменения размера холста."""
        width = tk.simpledialog.askinteger(title="Изменить размер холста", prompt="Ширина холста:")
        height = tk.simpledialog.askinteger(title="Изменить размер холста", prompt="Высота холста:")
        self.canvas.config(width=width, height=height)
        self.image = self.image.resize((width, height))
        self.draw = ImageDraw.Draw(self.image)


    def add_text(self):
        """Функция выводит диалоговое окно для ввода текста."""
        text = tk.simpledialog.askstring(title='Ввести текст', prompt="Текст:")
        self.text = text

    def paste_text(self, event):
        """ Функция вставляет текст на холст в координатах щелчка левой кнопки мыши."""
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.create_text(self.last_x, self.last_y, text=self.text, fill=self.pen_color)
        self.text = None
    def change_canvas_color(self):
        """Функция для изменения цвета холста."""
        color = tk.colorchooser.askcolor()
        new_color = color[1]
        self.canvas.config(bg=new_color)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
