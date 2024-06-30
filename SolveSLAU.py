from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Style
from PIL import Image, ImageTk


class SolveSLAU:
    def __init__(self):
        # Открытие основного окна
        self.__root = Tk()
        self.__root.title('SolveSLAU')
        self.__root.geometry('900x480')
        self.__root['bg'] = '#27292b'
        self.__root.resizable(False, False)
        self.__icon = PhotoImage(file='calc.png')
        self.__root.iconphoto(True, self.__icon)

        # Регистрация функций проверки ввода чисел
        self.__checkFloat = (self.__root.register(self.__checkFloatInput), "%P")

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=1)

        self.__frame_main = Frame(self.__root, bg="#27292b")
        self.__frame_main.grid(sticky='news')

        # По умолчанию 2 переменные
        self.__entries = []
        self.__variables = 2
        self.__updateCanvas()

        #
        #   Создание кнопок и текстовых надписей
        #

        self.__frame_buttons = Frame(self.__frame_main, bg="#27292b")
        self.__frame_buttons.grid(row=0, column=1, sticky='news')

        # Надписть "Метод решения"
        self.__methodLabel = Label(self.__frame_buttons, text='Метод решения:', background='#27292b', foreground='#fff', font=20)
        self.__methodLabel.grid(row=0, column=2, padx=55, pady=5)

        # Выпадающий список для выбора методов
        self.__methods = ['Гаусс', 'Простые итерации', 'Зейдель']
        self.__comboSelected = StringVar()
        self.__comboStyle = Style()
        self.__comboStyle.theme_create('combostyle', parent='alt', settings={
            'TCombobox': {
                'configure': {
                    'selectbackground': '#6b6b6b',
                    'fieldbackground': '#6b6b6b',
                    'foreground': '#fff',
                    'background': '#6b6b6b',
                }
            }
        })
        self.__comboStyle.theme_use('combostyle')
        self.__combobox = Combobox(self.__frame_buttons, values=self.__methods, font=20, textvariable=self.__comboSelected)
        self.__combobox['state'] = 'readonly'
        self.__combobox.set(self.__methods[0])
        self.__combobox.grid(row=1, column=2, pady=(5, 5))

        # Надписть "Количество переменных"
        self.__varLabel = Label(self.__frame_buttons, text='Количество переменных:', background='#27292b', foreground='#fff', font=20)
        self.__varLabel.grid(row=2, column=2, pady=(5, 5))

        # Переключатель для количества переменных
        self.__spinbox = Spinbox(self.__frame_buttons, from_=2, to=20, font=20, state="readonly", command=self.__changeVar,
                                 readonlybackground='#6b6b6b', foreground='#fff', buttonbackground='#6b6b6b')
        self.__spinbox.grid(row=3, column=2, pady=(5, 5))

        # Кнопка "Решить"
        self.__btnSolve = Button(self.__frame_buttons, text='Решить', command=self.__btnSolveClicked, bg='#6b6b6b',
                                 activebackground='#27292b', fg='#fff', activeforeground='#fff', font=30)
        self.__btnSolve.grid(row=4, column=2, pady=(15, 5))

    def start(self):
        self.__root.update_idletasks()
        self.__root.mainloop()

    #
    #   Функция, запускающая процесс решения
    #   по выбранному методу.
    #   Запускается при нажатии кнопки "Решить".
    #
    #   Перед запуском надо проверить, что все числа
    #   введены в ячейки и являются числами.
    #
    #   Если все проверки пройдены запускает окно с решением
    #   иначе выводит ошибку
    #
    def __btnSolveClicked(self):
        a = []
        b = []
        a_i = []  # строка списка a
        j = 0
        for i in range(len(self.__entries)):
            val = self.__entries[i].get()
            if val == '':
                val = 0
            if j == self.__variables:
                b.append(float(val))
                a.append(a_i)
                a_i = []
                j = 0
            else:
                a_i.append(float(val))
                j += 1

        print(a)
        print(b)
        print(self.__comboSelected.get())

    #
    #   Функция, проверяющая, является ли
    #   входное значение float.
    #
    #   Возвращает True/False (bool)
    #
    def __checkFloatInput(self, inp):
        if inp == '': return True
        try:
            float(inp)
        except:
            return False
        return True

    #
    #   Функция, меняющая количество переменных
    #
    def __changeVar(self):
        self.__variables = int(self.__spinbox.get())
        self.__updateCanvas()

    #
    #   Функция, создающая таблицу с полями ввода
    #
    def __updateCanvas(self):

        # Загрузка картинки символа системы
        image = Image.open('symbol.png')
        image = image.resize((self.__variables * 3, self.__variables * 35))
        photo = ImageTk.PhotoImage(image)

        #
        #   Создание полей ввода в систему
        #

        frame_canvas = Frame(self.__frame_main)
        frame_canvas.grid(row=0, column=0, sticky='nw', rowspan=self.__variables)
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        canvas = Canvas(frame_canvas, scrollregion=(0, 0, self.__variables * 2 * 91, self.__variables * 2 * 20), bg='#27292b',
                        width=650,
                        height=463,
                        highlightthickness=0)
        vsbX = Scrollbar(frame_canvas, orient=HORIZONTAL, command=canvas.xview)
        vsbY = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview)
        canvas.grid(row=0, column=0, sticky='nwes')
        vsbX.grid(row=1, column=0, sticky='ew')
        vsbY.grid(row=0, column=1, sticky='ns')

        frame_entries = Frame(canvas, bg='#27292b')
        canvas.create_window((0, 0), window=frame_entries, anchor='nw')

        # Добавление картинки символа системы
        symbolPicture = Label(frame_entries, image=photo, background='#27292b')
        symbolPicture.image = photo
        symbolPicture.grid(column=0, rowspan=self.__variables, row=0, sticky='nw')

        self.__entries.clear()
        for r in range(self.__variables):
            i = 1
            for c in range(1, self.__variables * 2 + 2):
                if c % 2 != 0:
                    entry = Entry(frame_entries, validate='key', vcmd=(self.__root.register(self.__checkFloatInput), '%P'),
                                  background='#6b6b6b',
                                  foreground='#fff', font=20, width=10)
                    self.__entries.append(entry)
                    entry.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, padx=5, pady=5)
                else:
                    if i == self.__variables:
                        label = Label(frame_entries, text=f'x{i} = ', background='#27292b', foreground='#fff', font=20)
                        label.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, ipadx=5, ipady=5)
                    else:
                        label = Label(frame_entries, text=f'x{i} + ', background='#27292b', foreground='#fff', font=20)
                        label.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, ipadx=5, ipady=5)
                        i += 1

    #
    #   Функция, решающая систему методом Гаусса.
    #
    #   Принимает массив коэффициентов А и B (float[]).
    #   Возвращает массив ответов X (float[])
    #
    def __gauss(self, a, b):
        pass

    #
    #   Функция, решающая систему методом простых итераций.
    #
    #   Принимает массив коэффициентов А и B (float[]),
    #   минимальную точность eps (float), максимальное количество
    #   итераций iter (int).
    #   Возвращает массив ответов X (float[]).
    #
    def __simpleIterations(self, a, b, eps, iter):
        pass

    #
    #   Функция, решающая систему методом Зейделя.
    #
    #   Принимает массив коэффициентов А и B (float[]),
    #   минимальную точность eps (float), максимальное количество
    #   итераций iter (int).
    #   Возвращает массив ответов X (float[]).
    #
    def __zeidel(self, a, b, eps, iter):
        pass


if __name__ == "__main__":
    app = SolveSLAU()
    app.start()
