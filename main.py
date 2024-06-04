from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Style
from PIL import Image, ImageTk


def btnSolveClicked():
    pass


def checkFloatInput(val):
    return True


def checkIntInput(val):
    return True


def methodSelected(event):
    pass


def gauss():
    pass


def simpleIterations():
    pass


def zeidel():
    pass


variables = 3

root = Tk()
root.title('SolveSLAU')
root.geometry('900x480')
root['bg'] = '#27292b'
root.minsize(900, 480)
icon = PhotoImage(file='calc.png')
root.iconphoto(True, icon)

image = Image.open('symbol.png')
image = image.resize((variables*10, round(variables*10*3.6537)))
photo = ImageTk.PhotoImage(image)

checkFloat = (root.register(checkFloatInput), "%P")
checkInt = (root.register(checkIntInput), "%P")

for c in range(variables*2+2): root.columnconfigure(index=c)
for r in range(variables): root.rowconfigure(index=r)

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
symbolPicture = Label(root, image=photo, background='#27292b')
symbolPicture.image = photo
symbolPicture.grid(column=0, rowspan=variables, row=0)
methodLabel = Label(text='Метод решения:', background='#27292b', foreground='#fff', font=20)
methodLabel.place(height=50, width=200, relx=0.73, rely=0.01)
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
btnSolve = Button(text='Решить', command=btnSolveClicked, bg='#6b6b6b',
                  activebackground='#27292b', fg='#fff', activeforeground='#fff', font=30)
btnSolve.place(height=50, width=200, relx=0.73, rely=0.35)
comboStyle.theme_use('combostyle')
combobox = Combobox(values=methods, foreground='#fff', font=20)
combobox['state'] = 'readonly'
combobox.place(relx=0.73, rely=0.1)
combobox.bind("<<ComboboxSelected>>", methodSelected)
varLabel = Label(text='Количество переменных:', background='#27292b', foreground='#fff', font=20)
varLabel.place(height=50, width=200, relx=0.73, rely=0.15)
varEntry = Entry(validate='focus', validatecommand=checkInt, background='#6b6b6b', foreground='#fff', font=20)
varEntry.place(relx=0.739, rely=0.248)

root.mainloop()
