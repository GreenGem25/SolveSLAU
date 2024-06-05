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
variables = 5

# Открытие основного окна
root = Tk()
root.title('SolveSLAU')
root.geometry('900x480')
root['bg'] = '#27292b'
root.minsize(900, 480)
icon = PhotoImage(file='calc.png')
root.iconphoto(True, icon)

# Загрузка картиныки символа системы
image = Image.open('symbol.png')
image = image.resize((variables*10, round(variables*10*3.6537)))
photo = ImageTk.PhotoImage(image)

# Регистрация функций проверки ввода чисел
checkFloat = (root.register(checkFloatInput), "%P")
checkInt = (root.register(checkIntInput), "%P")

#
#   Создание полей ввода в систему
#

# Инициализация таблицы с полями ввода
for c in range(variables*2+2): root.columnconfigure(index=c)
for r in range(variables): root.rowconfigure(index=r)

# Создание таблицы с полями ввода
for r in range(variables):
    i = 1
    for c in range(1, variables*2+2):
        if c % 2 != 0:
            entry = Entry(validate='focus', validatecommand=checkFloat, background='#6b6b6b', foreground='#fff', font=20, width=10)
            entry.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, padx=5, pady=5)
        else:
            if i == variables:
                label = Label(text=f'x{i} = ', background='#27292b', foreground='#fff', font=20)
                label.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, ipadx=5, ipady=5)
            else:
                label = Label(text=f'x{i} + ', background='#27292b', foreground='#fff', font=20)
                label.grid(row=r, column=c, sticky=NW, columnspan=1, rowspan=1, ipadx=5, ipady=5)
                i += 1
# Добавление картинки символа системы
symbolPicture = Label(root, image=photo, background='#27292b')
symbolPicture.image = photo
symbolPicture.grid(column=0, rowspan=variables, row=0)

#
#   Создание кнопок и текстовых надписей
#

# Надписть "Метод решения"
methodLabel = Label(text='Метод решения:', background='#27292b', foreground='#fff', font=20)
methodLabel.place(height=50, width=200, relx=0.73, rely=0.01)

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
combobox = Combobox(values=methods, foreground='#fff', font=20)
combobox['state'] = 'readonly'
combobox.place(relx=0.73, rely=0.1)
combobox.bind("<<ComboboxSelected>>", methodSelected)

# Надписть "Количество переменных"
varLabel = Label(text='Количество переменных:', background='#27292b', foreground='#fff', font=20)
varLabel.place(height=50, width=200, relx=0.73, rely=0.15)

# Поле ввода для количества переменных
varEntry = Entry(validate='focus', validatecommand=checkInt, background='#6b6b6b', foreground='#fff', font=20)
varEntry.place(relx=0.739, rely=0.248)

# Кнопка "Решить"
btnSolve = Button(text='Решить', command=btnSolveClicked, bg='#6b6b6b',
                  activebackground='#27292b', fg='#fff', activeforeground='#fff', font=30)
btnSolve.place(height=50, width=200, relx=0.73, rely=0.35)

root.mainloop()
