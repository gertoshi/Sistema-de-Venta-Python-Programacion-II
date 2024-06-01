import customtkinter as ctk
from time import strftime
import locale
from moduloVentas import moduloVenta
from gestion_cortaa import gestion_corta
from registro import modulo_usuario
import subprocess



def prueba():
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    def actualizar_reloj():
        etiqueta_hora.configure(text=strftime("%H:%M"))
        etiqueta_s.configure(text=strftime("%S"))
        etiqueta_fecha.configure(text=strftime("%A, %d/%m/%y"))
        etiqueta_s.after(1000, actualizar_reloj)

    def usuario():
        for widget in usuario_informacion.winfo_children():
            widget.destroy()
        modulo_usuario(usuario_informacion)

    def productos():
        for widget in usuario_informacion.winfo_children():
            widget.destroy()
        # Mostrar la información de gestión corta
        gestion_corta(usuario_informacion)

    def salir():

        ventana.destroy()

    def ventas():
        for widget in usuario_informacion.winfo_children():
            widget.grid_configure(padx=10, pady=5)
        moduloVenta(usuario_informacion)

    # Inicializar la ventana principal
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Sistema Ventas")
    ventana.geometry("1080x800")

    def volver_login ():
        subprocess.Popen(["python","login1.py"])
        ventana.destroy()

    usuario_informacion = ctk.CTkFrame(ventana, width=1700, height=1400)
    usuario_informacion.grid(row=0, column=0, padx=20, pady=100)

    for widget in usuario_informacion.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    boton_productos = ctk.CTkButton(master=ventana, text="Productos", border_width= 3,border_color="blue",font=("Bookman", 14), hover_color="blue", fg_color="black", command=productos, height=60, width=190)
    boton_productos.place(x=30, y=30)

    boton_cerrar = ctk.CTkButton(master=ventana, text="cerrar sesion", border_width= 3,border_color="blue",font=("Bookman", 14), hover_color="blue", fg_color="black", height=60, width=190,command=volver_login)
    boton_cerrar.place(x=1000, y=30)

    boton_ventas = ctk.CTkButton(master=ventana, text="Ventas", border_width= 3,border_color="blue",font=("Bookman", 14), hover_color="blue", fg_color="black", command=ventas, height=60, width=190)
    boton_ventas.place(x=250, y=30)

    boton_usuarios = ctk.CTkButton(master=ventana, text="Usuarios",border_width= 3,border_color="blue", font=("Bookman", 14), hover_color="blue", fg_color="black", command=usuario, height=60, width=190)
    boton_usuarios.place(x=500, y=30)

    boton_salir = ctk.CTkButton(master=ventana, text="Salir", border_width= 3,border_color="blue",font=("Bookman", 14), hover_color="blue", fg_color="black", command=salir, height=60, width=190)
    boton_salir.place(x=750, y=30)

    frame_hora = ctk.CTkFrame(ventana)
    frame_hora.place(x=1300, y=30)

    etiqueta_hora = ctk.CTkLabel(frame_hora, font=("digitalk", 25), text="H:M")
    etiqueta_hora.grid(row=0, column=0)

    etiqueta_s = ctk.CTkLabel(frame_hora, font=("digitalk", 12), text="S")
    etiqueta_s.grid(row=0, column=0,columnspan=3, sticky="n",padx=100, pady=0)

    etiqueta_fecha = ctk.CTkLabel(frame_hora, font=("digitalk", 25), text="dia d/m/aaaa")
    etiqueta_fecha.grid(row=1, column=0, columnspan=2)

    actualizar_reloj()

    ventana.mainloop()
