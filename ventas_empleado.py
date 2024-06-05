import tkinter as tk
from tkinter import *
from tkinter import ttk
from modulo_ventas import moduloVenta
def empleado():
    usuario_informacion = tk.Tk()
    usuario_informacion.title("Sistema Ventas")
    usuario_informacion.geometry("1080x800")
    
    
    moduloVenta(usuario_informacion)

    usuario_informacion.mainloop()
