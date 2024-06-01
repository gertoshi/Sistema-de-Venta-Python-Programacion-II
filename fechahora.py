from time import strftime
from tkinter import *

import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
def actualizar_reloj():
    etiqueta_hora.config(text=strftime("%H:%M"))
    etiqueta_s.config(text=strftime("%S"))
    etiqueta_fecha.config(text=strftime("%A, %d/%m/%y"))
    etiqueta_s.after(1000,actualizar_reloj)



venta=Tk()

frame_hora=Frame()
frame_hora.pack()
etiqueta_hora= Label(frame_hora,font=("digitalk",25), text="H:M")
etiqueta_hora.grid(row=0,  column=0)

etiqueta_s= Label(frame_hora,font=("digitalk",12), text="S")
etiqueta_s.grid(row=0,  column=1, sticky="n")

etiqueta_fecha= Label(font=("digitalk",25), text="dia d/m/aaaa")
etiqueta_fecha.pack(anchor="center")

actualizar_reloj()

venta.mainloop()