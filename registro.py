import tkinter as tk
import json
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox

def cargar_usuarios():
    try:
        with open('usuarios.json', "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open('usuarios.json', "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

def modulo_usuario(usuario_informacion):
    def confirmacion():
        nombre_empleado = usuario_nombre_input.get()
        contrasena_empleado = usuario_contraseña_input.get()
        cargo = tipo_usuario.get()
        usuarios = cargar_usuarios()
        
        if len(nombre_empleado) >= 1:
            if len(contrasena_empleado) >= 6 and len(cargo) >1:

                    if nombre_empleado not in usuarios:
                        nuevo_usuario = {
                            "cargo": cargo,
                            "usuario": nombre_empleado,
                            "contrasena": contrasena_empleado,
                        }
                        # Agregar el nuevo usuario al diccionario existente
                        usuarios[nombre_empleado] = nuevo_usuario
                        # Guardar todos los usuarios (incluyendo el nuevo) en el archivo JSON
                        guardar_usuarios(usuarios)               
                        mensaje_.config(text=f"Usuario '{nombre_empleado}' agregado con éxito.", foreground="blue")
                    else:
                        mensaje_.config(text=f"El usuario '{nombre_empleado}' ya existe.", foreground="red")
                        messagebox.showerror("Error: ",f"El usuario '{nombre_empleado}' ya existe.")
            else:
                messagebox.showerror("Error: ","La contraseña debe tener al menos 6 caracteres.")
        else:
            messagebox.showerror("Error: ","Ingrese un usuario y contraseña.")


    frame = tk.Frame(usuario_informacion)
    frame.pack()  

    # Información del usuario
    usuario_informacion = ttk.LabelFrame(frame, text="Información de Usuario")
    usuario_informacion.grid(row=0, column=0, padx=20, pady=20)

    # Nombre de usuario y contraseña
    usuario_nombre = tk.Label(usuario_informacion, text="Nombre de Usuario",font=("Bookman",14))
    usuario_nombre.grid(row=0, column=0)

    usuario_contraseña = tk.Label(usuario_informacion, text="Contraseña",font=("Bookman",14))
    usuario_contraseña.grid(row=0, column=1)

    usuario_nombre_input = tk.Entry(usuario_informacion,font=("Bookman",14))
    usuario_contraseña_input = tk.Entry(usuario_informacion, show="*",font=("Bookman",14))
    usuario_nombre_input.grid(row=1, column=0)
    usuario_contraseña_input.grid(row=1, column=1)

    # Confirmación de registro
    usuario_registro = ttk.LabelFrame(frame)
    usuario_registro.grid(row=2, column=0, sticky="news", padx=20, pady=20)

    tipo_usua = ttk.LabelFrame(frame, text="Selecciones su cargo")
    tipo_usua.grid(row=1, column=0, padx=20, pady=20)

    opciones= ["Administrador", "Empleado"]
    tipo_usuario= Combobox(tipo_usua, width="13", values=opciones, state="readonly",font=("Bookman",19))
    tipo_usuario.pack()

    # espacio entre campos de entrada
    for widget in usuario_informacion.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    # Botón de confirmación
    boton = tk.Button(frame, text="Guardar Datos", command=confirmacion,font=("Bookman",14))
    boton.grid(row=3, column=0, sticky="news", padx=20, pady=20)

    mensaje_ = tk.Label(frame, text="", foreground="red")
    mensaje_.grid()

