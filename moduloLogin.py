
import json
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
from moduloVentas import empleado
from main import prueba
from customtkinter import *
import customtkinter as ctk
import subprocess

def abrir_pruebas():
    subprocess.Popen(["python","pruebas.py"])

def login():
    def cargar_usuarios():
        try:
            with open('usuarios.json', "r") as archivo:
                return json.load(archivo) 
        except FileNotFoundError:
            return {}

    def verificar_datos():
        usuario = usuario_entrada.get()
        contrasena = contrasena_entry.get()
        cargo_usuario = tipo_usuario.get()
        usuarios = cargar_usuarios()
        
        if len(cargo_usuario) > 1:
            if usuario in usuarios and usuarios[usuario]["contrasena"] == contrasena:
                if usuarios[usuario]["cargo"] == cargo_usuario:
                    
                    ventana1.destroy()
                    
                    if cargo_usuario == "Administrador":
                        prueba()
                        
                    else:
                        empleado()
                        
                    
                else:
                    messagebox.showerror("Error", "Usuario incorrecto.")
            else:
                messagebox.showerror("Error", "Nombre de usuario o Contraseña incorrectos.")

        else:
            messagebox.showerror("Error", "Por favor, seleccione un cargo.")



    ventana1 = ctk.CTk()
    ventana1.title("Inicio de Sesión")
    ventana1.geometry("300x400")
    ventana1.configure(fg_color="#000000")
    ventana1.resizable(0, 0)

    marco_principal = CTkFrame(ventana1, corner_radius=10, fg_color="#000000")
    marco_principal.grid(row=0, column=0, sticky="nsew")

    ventana1.grid_rowconfigure(0, weight=1)
    ventana1.grid_columnconfigure(0, weight=1)
    style = ttk.Style()
    style.configure("Custom.TLabelframe", background="#000000")
    style.configure("Custom.TLabelframe.Label", background="#000000", foreground="#FFFFFF",font=("Bookman",14))

    tipo_usua = CTkLabel(marco_principal, text="Seleccione su cargo:", font=("Bookman", 14),text_color= ("white"))
    tipo_usua.grid(row=4, column=0, columnspan=2, pady=10, padx=10) 



    usuario_entrada = CTkEntry(marco_principal, font=("Bookman", 16),border_width= 2,border_color="blue", fg_color="grey")
    usuario_entrada.grid(row=1, column=0, pady=0, padx=80)

    contrasena_entry = CTkEntry(marco_principal, font=("Bookman", 16), show="*",border_width= 2,border_color="blue",fg_color="grey")
    contrasena_entry.grid(row=3, column=0, pady=10, padx=10)


    usuario_etiqueta = CTkLabel(marco_principal, text="Usuario:", font=("Bookman", 14),text_color= ("white"))
    usuario_etiqueta.grid(row=0, column=0,pady=10 )
    
    contrasena_etiqueta = CTkLabel(marco_principal, text="Contraseña:", font=("Bookman", 14),text_color= ("white") )
    contrasena_etiqueta.grid(row=2, column=0)
    tipo_usuario = Combobox(marco_principal, width=13, values=["Administrador", "Empleado"], state="readonly",font=("Bookman",14), foreground="grey")
    tipo_usuario.grid(row=5, column=0, pady=5, padx=10)

    iniciar_sesion_boton = CTkButton(master=marco_principal, text="Iniciar Sesión", font=("Bookman", 14), hover_color="blue", 
        fg_color="black", command= verificar_datos, height=50, width=130, border_width= 2,border_color="blue")
    iniciar_sesion_boton.grid(row=6, column=0, columnspan=2, pady=20, padx=10)  


    ventana1.mainloop()

login()