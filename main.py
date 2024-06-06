from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Style
from PIL import Image, ImageTk


#
#   Функция, запускающая процесс решения
#   по выбранному методу.
#   Запускается при нажатии кнопки "Запустить".
#
#   Перед запуском надо проверить, что все числа
#   введены в ячейки и являются числами.
#
#   Если все проверки пройдены запускает окно с решением
#   иначе выводит ошибку
#
def btnSolveClicked():
    pass


#
#   Функция, проверяющая, является ли
#   входное значение float.
#
#   Возвращает True/False (bool)
#
def checkFloatInput(val):
    return True


#
#   Функция, проверяющая, является ли
#   входное значение int.
#
#   Возвращает True/False (bool)
#
def checkIntInput(val):
    return True


#
#   Функция, возвращающая выбранный пользователем
#   метод решения системы.
#
#   Возвращает выбранный метод решения (string)
#
def methodSelected(event):
    pass


#
#   Функция, решающая систему методом Гаусса.
#
#   Принимает массив коэффициентов А и B (float[]).
#   Возвращает массив ответов X (float[])
#
def gauss(A, B):
    pass


#
#   Функция, решающая систему методом простых итераций.
#
#   Принимает массив коэффициентов А и B (float[]),
#   минимальную точность eps (float), максимальное количество
#   итераций iter (int).
#   Возвращает массив ответов X (float[]).
#
def simpleIterations(A, B, eps, iter):
    pass


#
#   Функция, решающая систему методом Зейделя.
#
#   Принимает массив коэффициентов А и B (float[]),
#   минимальную точность eps (float), максимальное количество
#   итераций iter (int).
#   Возвращает массив ответов X (float[]).
#
def zeidel(A, B, eps, iter):
    pass


# Количество переменных системы
variables = 20

# Открытие основного окна
root = Tk()
root.title('SolveSLAU')
root.geometry('900x480')
root['bg'] = '#27292b'
root.resizable(False, False)
icon = PhotoImage(file='calc.png')
root.iconphoto(True, icon)

# Загрузка картинки символа системы
image = Image.open('symbol.png')
image = image.resize((variables*3, variables*35))
photo = ImageTk.PhotoImage(image)

# Регистрация функций проверки ввода чисел
checkFloat = (root.register(checkFloatInput), "%P")
checkInt = (root.register(checkIntInput), "%P")

root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = Frame(root, bg="#27292b")
frame_main.grid(sticky='news')

#
#   Создание полей ввода в систему
#

frame_canvas = Frame(frame_main)
frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw', rowspan=variables)
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
canvas = Canvas(frame_canvas, scrollregion=(0, 0, variables*2*91, variables*2*20), bg='#27292b', width=650, height=350,
                highlightthickness=0)
vsbX = Scrollbar(frame_canvas, orient=HORIZONTAL, command=canvas.xview)
vsbY = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview)
canvas.grid(row=0, column=0, sticky='nwes')
vsbX.grid(row=1, column=0, sticky='ew', columnspan=variables)
vsbY.grid(row=0, column=1, sticky='ns', rowspan=variables)

frame_entries = Frame(canvas, bg='#27292b')
canvas.create_window((0, 0), window=frame_entries, anchor='nw')
entries = []

# Добавление картинки символа системы
symbolPicture = Label(frame_entries, image=photo, background='#27292b')
symbolPicture.image = photo
symbolPicture.grid(column=0, rowspan=variables, row=0, sticky='nw')

for r in range(variables):
    i = 1
    for c in range(1, variables*2+2):
        if c % 2 != 0:
            entry = Entry(frame_entries, validate='focus', validatecommand=checkFloat, background='#6b6b6b',
                          foreground='#fff', font=20, width=10)
            entries.append(entry)
            entry.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, padx=5, pady=5)
        else:
            if i == variables:
                label = Label(frame_entries, text=f'x{i} = ', background='#27292b', foreground='#fff', font=20)
                label.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, ipadx=5, ipady=5)
            else:
                label = Label(frame_entries, text=f'x{i} + ', background='#27292b', foreground='#fff', font=20)
                label.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, ipadx=5, ipady=5)
                i += 1

#
#   Создание кнопок и текстовых надписей
#

frame_buttons = Frame(frame_main, bg="#27292b")
frame_buttons.grid(row=0, column=1, sticky='news')

# Надписть "Метод решения"
methodLabel = Label(frame_buttons, text='Метод решения:', background='#27292b', foreground='#fff', font=20)
methodLabel.grid(row=0, column=2, padx=55, pady=5)

# Выпадающий список для выбора методов
methods = ['Гаусс', 'Простые итерации', 'Зейдель']
comboStyle = Style()
comboStyle.theme_create('combostyle', parent='alt', settings={
    'TCombobox': {
        'configure': {
            'selectbackground': '#6b6b6b',
            'fieldbackground': '#6b6b6b',
            'background': '#6b6b6b'
        }
    }
})
comboStyle.theme_use('combostyle')
combobox = Combobox(frame_buttons, values=methods, foreground='#fff', font=20)
combobox['state'] = 'readonly'
combobox.grid(row=1, column=2, pady=(5, 5))
combobox.bind("<<ComboboxSelected>>", methodSelected)

# Надписть "Количество переменных"
varLabel = Label(frame_buttons, text='Количество переменных:', background='#27292b', foreground='#fff', font=20)
varLabel.grid(row=2, column=2, pady=(5, 5))

# Поле ввода для количества переменных
varEntry = Entry(frame_buttons, validate='focus', validatecommand=checkInt, background='#6b6b6b', foreground='#fff', font=20)
varEntry.grid(row=3, column=2, pady=(5, 5))

# Кнопка "Решить"
btnSolve = Button(frame_buttons, text='Решить', command=btnSolveClicked, bg='#6b6b6b',
                  activebackground='#27292b', fg='#fff', activeforeground='#fff', font=30)
btnSolve.grid(row=4, column=2, pady=(15, 5))

root.update_idletasks()
root.mainloop()
