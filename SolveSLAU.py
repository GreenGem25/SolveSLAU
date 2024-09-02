import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Style
from PIL import Image, ImageTk
import numpy as np

class SolveSLAU:
    def __init__(self):
        # Открытие основного окна
        self.__root = Tk()
        self.__root.title('SolveSLAU')
        self.__root.geometry('900x480')
        self.__root['bg'] = '#27292b'
        self.__root.resizable(False, False)
        icon = PhotoImage(file='calc.png')
        self.__root.iconphoto(True, icon)

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
        methodLabel = Label(self.__frame_buttons, text='Метод решения:', background='#27292b', foreground='#fff',
                            font=20)
        methodLabel.grid(row=0, column=2, padx=55, pady=5)

        # Выпадающий список для выбора методов
        methods = ['Гаусс', 'Простые итерации', 'Зейдель']
        self.__comboSelected = methods[0]
        comboStyle = Style()
        comboStyle.theme_create('combostyle', parent='alt', settings={
            'TCombobox': {
                'configure': {
                    'selectbackground': '#6b6b6b',
                    'fieldbackground': '#6b6b6b',
                    'foreground': '#fff',
                    'background': '#6b6b6b',
                }
            }
        })
        comboStyle.theme_use('combostyle')
        self.__combobox = Combobox(self.__frame_buttons, values=methods, font=20)
        self.__combobox.bind('<<ComboboxSelected>>', self.__changeMethod)
        self.__combobox['state'] = 'readonly'
        self.__combobox.set(methods[0])
        self.__combobox.grid(row=1, column=2, pady=(5, 5))

        # Надписть "Количество переменных"
        varLabel = Label(self.__frame_buttons, text='Количество переменных:', background='#27292b', foreground='#fff',
                         font=20)
        varLabel.grid(row=2, column=2, pady=(5, 5))

        # Переключатель для количества переменных
        self.__spinbox = Spinbox(self.__frame_buttons, from_=2, to=20, font=20, state="readonly",
                                 command=self.__changeVar,
                                 readonlybackground='#6b6b6b', foreground='#fff', buttonbackground='#6b6b6b')
        self.__spinbox.grid(row=3, column=2, pady=(5, 5))

        # Надпись "Точность"
        epsLabel = Label(self.__frame_buttons, text='Точность:', background='#27292b',
                         foreground='#fff', font=20)
        epsLabel.grid(row=4, column=2, pady=(5, 5))

        # Поле ввода точности, в методе Гаусса отключено
        self.__entryEps = Entry(self.__frame_buttons, validate='key',
                                vcmd=(self.__root.register(self.__checkFloatInput), '%P'),
                                background='#6b6b6b',
                                foreground='#fff', font=20, width=10)
        self.__entryEps.insert(0, '0.01')
        self.__entryEps.config(state='disabled')
        self.__entryEps.grid(row=5, column=2, pady=(5, 5))

        # Надпись "Количество итераций"
        iterLabel = Label(self.__frame_buttons, text='Количество итераций:', background='#27292b',
                          foreground='#fff', font=20)
        iterLabel.grid(row=6, column=2, pady=(5, 5))

        # Поле ввода количества итераций, в методе Гаусса отключено
        self.__entryIter = Entry(self.__frame_buttons, validate='key',
                                 vcmd=(self.__root.register(self.__checkIntInput), '%P'),
                                 background='#6b6b6b',
                                 foreground='#fff', font=20, width=10)
        self.__entryIter.insert(0, '10')
        self.__entryIter.config(state='disabled')
        self.__entryIter.grid(row=7, column=2, pady=(5, 5))

        # Кнопка "Решить"
        btnSolve = Button(self.__frame_buttons, text='Решить', command=self.__btnSolveClicked, bg='#6b6b6b',
                          activebackground='#27292b', fg='#fff', activeforeground='#fff', font=30)
        btnSolve.grid(row=8, column=2, pady=(15, 5))

    #
    #   Функция, запускающая главный цикл приложения
    #
    def start(self):
        self.__root.update_idletasks()
        self.__root.mainloop()

    #
    #   Функция, открывающая новое окно
    #
    def __openWindow(self, answer, message):
        window = tkinter.Toplevel(self.__root)
        window.geometry('400x400')
        window['bg'] = '#27292b'
        window.resizable(False, False)
        window.title('Результат работы')

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        canvas = Canvas(window, bg='#27292b', border=0, scrollregion=(0, 0, 0, self.__variables * 35), height=300, width=400,
                        borderwidth=0)
        canvas.grid(row=0, column=0, sticky='news')
        vsbY = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
        vsbY.grid(row=0, column=1, sticky='ns')
        frame_labels = Frame(canvas, bg='#27292b')
        frame_labels.grid_rowconfigure(0, weight=1)
        frame_labels.grid_columnconfigure(0, weight=1)
        canvas.create_window((0, 0), window=frame_labels, anchor='nw')

        if not answer:
            label = Label(canvas, text=message, background='#27292b', foreground='#fff', font=30)
            label.place(relx=.5, rely=.5, anchor="center")
        else:
            for i in range(0, self.__variables):
                label = Label(frame_labels, text=f'x{i+1} = {answer[i]}', background='#27292b', foreground='#fff', font=30)
                label.grid(row=i, column=0, ipadx=5, pady=5, sticky='w')

        btnExit = Button(window, text='Выход', command=window.destroy, bg='#6b6b6b',
                         activebackground='#27292b', fg='#fff', activeforeground='#fff', font=30)
        btnExit.grid(row=1, column=0, sticky='news', columnspan=2)

        window.grab_set()

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
        a, b = self.__getMatrices()
        x = []
        message = ''

        if self.__comboSelected == 'Гаусс':
            try:
                x = self.__gauss(a, b)
            except ZeroDivisionError:
                x = []
                message = 'Невозможно решить систему.'
            except Exception as e:
                x = []
                message = e
            self.__openWindow(x, message)
        elif self.__comboSelected == 'Простые итерации':
            eps, iterCount = self.__getEpsAndIter()
            try:
                x = self.__simpleIterations(a, b, eps, iterCount)
            except ZeroDivisionError:
                x = []
                message = 'Невозможно решить систему.'
            except Exception as e:
                x = []
                message = e
            self.__openWindow(x, message)
        elif self.__comboSelected == 'Зейдель':
            eps, iterCount = self.__getEpsAndIter()
            try:
                x = self.__zeidel(a, b, eps, iterCount)
            except ZeroDivisionError:
                x = []
                message = 'Невозможно решить систему.'
            except Exception as e:
                x = []
                message = e
            self.__openWindow(x, message)

    #
    #   Функция, которая получает матрицы коэффициентов
    #
    #   Возвращает: (a[][], b[])
    #
    def __getMatrices(self):
        a = []
        b = []
        a_i = []  # строка списка A
        j = 0

        # 1D entries matrix to 2D A matrix and 1D B matrix
        for i in range(len(self.__entries)):
            val = self.__entries[i].get()
            if val == '':
                val = 0
                self.__entries[i].insert(0, '0')
            if j == self.__variables:
                b.append(float(val))
                a.append(a_i)
                a_i = []
                j = 0
            else:
                a_i.append(float(val))
                j += 1

        return a, b

    #
    #   Функция, которая получает значения
    #   точности и количества итераций из полей ввода
    #   и обновляет их в случае ошибки
    #
    #   Возвращает: (точность, количество итераций)
    #
    def __getEpsAndIter(self):
        eps = self.__entryEps.get()
        if eps == '':
            eps = 0.01
            self.__entryEps.insert(0, '0.01')
        eps = float(eps)
        if eps == 0:
            eps = 0.01
            self.__entryEps.delete(0, tkinter.END)
            self.__entryEps.insert(0, '0.01')
        if eps < 0:
            eps = abs(eps)
            self.__entryEps.delete(0, tkinter.END)
            self.__entryEps.insert(0, str(eps))

        iterCount = self.__entryIter.get()
        if iterCount == '':
            iterCount = 10
            self.__entryIter.insert(0, '10')
        iterCount = int(iterCount)
        if iterCount == 0:
            iterCount = 10
            self.__entryIter.delete(0, tkinter.END)
            self.__entryIter.insert(0, '10')

        return eps, iterCount

    #
    #   Функция, проверяющая, является ли
    #   входное значение float.
    #
    #   Возвращает True/False (bool)
    #
    def __checkFloatInput(self, inp):
        if inp == '': return True
        if inp == '-': return True
        try:
            float(inp)
        except:
            return False
        return True

    #
    #   Функция, проверяющая, является ли
    #   входное значение int.
    #
    #   Возвращает True/False (bool)
    #
    def __checkIntInput(self, inp):
        if inp == '': return True
        try:
            int(inp)
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
    #   Функция, меняющая метод решения
    #
    def __changeMethod(self, event):
        self.__comboSelected = self.__combobox.get()

        if self.__comboSelected == 'Простые итерации' or self.__comboSelected == 'Зейдель':
            self.__updateFrame(True)
        else:
            self.__updateFrame(False)

    #
    #   Функция активирующая или деактивирующая
    #   поля ввода точности и количества итераций
    #
    #   turnON = True для активации
    #   turnON = False для деактивации
    #
    def __updateFrame(self, turnON):
        if turnON:
            self.__entryEps.config(state='normal')
            self.__entryIter.config(state='normal')
        else:
            self.__entryEps.config(state='disabled')
            self.__entryIter.config(state='disabled')

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
        canvas = Canvas(frame_canvas, scrollregion=(0, 0, self.__variables * 2 * 91, self.__variables * 2 * 20),
                        bg='#27292b',
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
                    entry = Entry(frame_entries, validate='key',
                                  vcmd=(self.__root.register(self.__checkFloatInput), '%P'),
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
    #   Меняет строку m[col] с одной из нижестоящих строк, с большим начальным элементом
    #
    #   Принимает матрицу m (np.matrix), номер шага прямого хода k (int)
    #   Ничего не возвращает (изменяет матрицу m)
    #
    def __bubbleMaxRow(self, m, k):
        ind = k + np.argmax(np.abs(m[k:, k]))
        if ind != k:
            m[k, :], m[ind, :] = np.copy(m[ind, :]), np.copy(m[k, :])

    #
    #   Функция, определяющая необособленную матрицу
    #
    #   Принимает квадратную матрицу m (np.matrix)
    #   Возвращает True/False
    #
    def __isSingular(self, m):
        return np.any(np.diag(m) == 0)

    #
    #   Функция, решающая систему методом Гаусса с постолбцовым выбором главного элемента.
    #
    #   Принимает массив коэффициентов А и B (float[]).
    #   Возвращает массив ответов X (float[])
    #
    def __gauss(self, a, b):
        m = []
        for i in range(self.__variables):
            a[i].append(b[i])
            m.append(a[i])
        m = np.matrix(m)
        n = m.shape[0]
        for k in range(n - 1):
            self.__bubbleMaxRow(m, k)
            for i in range(k + 1, n):
                frac = m[i, k] / m[k, k]
                m[i, :] -= m[k, :] * frac
        if self.__isSingular(m):
            raise Exception('Система имеет бесконечное число решений\nили не имеет их вовсе.')
        x = np.matrix([0.0 for i in range(n)]).T
        for k in range(n - 1, -1, -1):
            x[k, 0] = (m[k, -1] - m[k, k:n] * x[k:n, 0]) / m[k, k]

        return [ans[0] for ans in x.tolist()]


    #
    #   Функция, решающая систему методом простых итераций.
    #
    #   Принимает массив коэффициентов А и B (float[]),
    #   минимальную точность eps (float), максимальное количество
    #   итераций iter (int).
    #   Возвращает массив ответов X (float[]).
    #
    def __simpleIterations(self, a, b, eps, iterCount):
        x0 = []
        for i in range(self.__variables):
            x0.append(b[i] / a[i][i])
        x1 = [0] * self.__variables
        maxPrecision = -float('inf')
        precision = 0.0
        iter = 0
        while abs(maxPrecision) > eps:
            if iter >= iterCount: break
            iter += 1
            maxPrecision = -float('inf')
            for i in range(0, self.__variables):
                s = 0
                for j in range(0, self.__variables):
                    if i != j:
                        s += a[i][j] * x0[j]
                x1[i] = (b[i] - s) / a[i][i]
                precision = abs(x1[i] - x0[i])
                if precision > maxPrecision:
                    maxPrecision = precision
            if abs(maxPrecision) > 100000:
                raise Exception('Итерации не сходятся,\nпопробуйте использовать метод Гаусса.')
            for i in range(0, self.__variables):
                x0[i] = x1[i]
        return x1

    #
    #   Функция, решающая систему методом Зейделя.
    #
    #   Принимает массив коэффициентов А и B (float[]),
    #   минимальную точность eps (float), максимальное количество
    #   итераций iter (int).
    #   Возвращает массив ответов X (float[]).
    #
    def __zeidel(self, a, b, eps, iterCount):
        x0 = []
        for i in range(self.__variables):
            x0.append(b[i] / a[i][i])
        x1 = [0] * self.__variables
        maxPrecision = -float('inf')
        precision = 0.0
        iter = 0
        while abs(maxPrecision) > eps:
            if iter >= iterCount: break
            iter += 1
            maxPrecision = -float('inf')
            for i in range(0, self.__variables):
                s = 0
                for j in range(0, self.__variables):
                    if i != j:
                        s += a[i][j] * x0[j]
                x1[i] = (b[i] - s) / a[i][i]
                precision = abs(x1[i] - x0[i])
                if precision > maxPrecision:
                    maxPrecision = precision
                x0[i] = x1[i]
            if abs(maxPrecision) > 100000:
                raise Exception('Итерации не сходятся,\nпопробуйте использовать метод Гаусса.')
        return x1


if __name__ == "__main__":
    app = SolveSLAU()
    app.start()
