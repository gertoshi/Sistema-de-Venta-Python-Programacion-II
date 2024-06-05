import tkinter as tk
from gestion_cortaa import *
from modulo_ventas import moduloVenta
import sys
from registro import modulo_usuario


def main(cargo_usuario):
    def botonSalirPrograma():
        sys.exit()

    ventana = tk.Tk()
    ventana.title("Sistema Ventas")
    ventana.geometry("300x200")
    ventana.resizable(0, 0)

    frame_botones_programas = tk.Frame(ventana)
    frame_botones_programas.grid(row=0, column=4)
    
    if cargo_usuario == "Administrador":
        boton_productos = tk.Button(frame_botones_programas,text="USUARIOS", command=modulo_usuario)  
        boton_productos.grid(row=0, column=1, pady=5, padx=5)

        boton_ventas = tk.Button(frame_botones_programas,text="PRODUCTOS", command=gestion_corta)
        boton_ventas.grid(row=0, column=2, pady=5, padx=5)

        boton_usuarios = tk.Button(frame_botones_programas, text="VENTAS", command=moduloVenta)
        boton_usuarios.grid(row=0, column=3, pady=5, padx=5)

        boton_salir = tk.Button(frame_botones_programas,text="SALIR", command=botonSalirPrograma)
        boton_salir.grid(row=0, column=4, pady=5, padx=5)
    else:
        boton_ventas = tk.Button(frame_botones_programas,text="VENTAS", command=moduloVenta)
        boton_ventas.grid(row=0, column=2, pady=5, padx=5)
        
        boton_salir = tk.Button(frame_botones_programas,text="SALIR", command=botonSalirPrograma)
        boton_salir.grid(row=0, column=4, pady=5, padx=5)

    ventana.mainloop()
