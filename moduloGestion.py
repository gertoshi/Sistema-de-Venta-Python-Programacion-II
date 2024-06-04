import tkinter as tk
import json
from tkinter import messagebox
from tkinter import ttk

productos = []

def cargar_datos():
    try:
        with open("productos.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(data):
    with open("productos.json", "w") as file:
        json.dump(data, file, indent=4)

def gestion_corta(usuario_informacion):
    def cargar_datos_treeview(treeview):
        for item in treeview.get_children():
            treeview.delete(item)
        for producto in productos:
            treeview.insert("", tk.END, values=(producto["Codigo"], producto["Descripcion"], producto["Precio"], producto["Cantidad"]))

    def dar_alta_producto():
        ventana_alta_producto = tk.Toplevel()
        ventana_alta_producto.title("Alta Producto")
        ventana_alta_producto.geometry("800x600")
        ventana_alta_producto.resizable(0, 0)

        etiquetas = ["Descripcion", "Precio", "Cantidad"]
        entries = []

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(ventana_alta_producto, text=f"{etiqueta}: ", font="Arial 12").grid(row=i, column=0)
            entry = tk.Entry(ventana_alta_producto, width=70) if etiqueta == "Descripcion" else tk.Entry(ventana_alta_producto, width=30)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def guardar_producto():
            datos = [entry.get().strip() for entry in entries]
            if "" in datos[1:]:
                messagebox.showerror("Advertencia", "Por favor, ingrese valores válidos.")
                return

            try:
                precio = float(datos[1])
                cantidad = int(datos[2])
            except ValueError:
                messagebox.showerror("Advertencia", "El precio y la cantidad deben ser valores numéricos.")
                return

            ultimo_codigo = productos[-1]["Codigo"] if productos else 0
            nuevo_producto = {
                "Descripcion": datos[0].upper(),
                "Codigo": ultimo_codigo + 1,
                "Precio": precio,
                "Cantidad": cantidad
            }
            productos.append(nuevo_producto)
            guardar_datos(productos)
            cargar_datos_treeview(treeview)
            ventana_alta_producto.destroy()

        tk.Button(ventana_alta_producto, text="CONFIRMAR", font="Arial 12", bg="light green", command=guardar_producto).grid(row=3, column=1)
        tk.Button(ventana_alta_producto, text="CANCELAR", font="Arial 12", bg="dark red", command=ventana_alta_producto.destroy).grid(row=4, column=1)

    def modificar_producto():
        seleccion = treeview.selection()
        if seleccion:
            item_id = seleccion[0]
            indice = treeview.index(item_id)
            producto_seleccionado = productos[indice]

            def guardar_cambios():
                producto_seleccionado["Descripcion"] = entry_descripcion.get().upper()
                producto_seleccionado["Precio"] = float(entry_precio.get())
                producto_seleccionado["Cantidad"] = int(entry_cantidad.get())
                guardar_datos(productos)
                cargar_datos_treeview(treeview)
                ventana_modificar_producto.destroy()

            ventana_modificar_producto = tk.Toplevel()
            ventana_modificar_producto.title("Modificar Producto")
            ventana_modificar_producto.geometry("600x300")
            ventana_modificar_producto.resizable(False, False)

            tk.Label(ventana_modificar_producto, text="Descripcion: ", font="Arial 12").grid(row=0, column=0)
            tk.Label(ventana_modificar_producto, text="Precio: ", font="Arial 12").grid(row=1, column=0)
            tk.Label(ventana_modificar_producto, text="Cantidad: ", font="Arial 12").grid(row=2, column=0)

            entry_descripcion = tk.Entry(ventana_modificar_producto, width=70)
            entry_descripcion.grid(row=0, column=1)
            entry_descripcion.insert(0, producto_seleccionado["Descripcion"])

            entry_precio = tk.Entry(ventana_modificar_producto, width=30)
            entry_precio.grid(row=1, column=1)
            entry_precio.insert(0, producto_seleccionado["Precio"])

            entry_cantidad = tk.Entry(ventana_modificar_producto, width=30)
            entry_cantidad.grid(row=2, column=1)
            entry_cantidad.insert(0, producto_seleccionado["Cantidad"])

            tk.Button(ventana_modificar_producto, text="Guardar Cambios", command=guardar_cambios).grid(row=3, column=1)
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto primero.")

    def eliminar_producto():
        seleccion = treeview.selection()
        if seleccion:
            item_id = seleccion[0]
            indice = treeview.index(item_id)
            producto_eliminado = productos.pop(indice)
            guardar_datos(productos)
            cargar_datos_treeview(treeview)
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto primero.")

    def salir_gestion_producto():
        usuario_informacion.destroy()
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14))  # Cambiar el tamaño de la fuente
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  
    # Crear y configurar el Treeview
    columnas = ("Codigo", "Descripcion", "Precio", "Cantidad")
    treeview = ttk.Treeview(usuario_informacion, columns=columnas, show="headings")
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, anchor=tk.CENTER,width=300)
    treeview.grid(row=1, column=0, columnspan=4, sticky="nsew")
    
    # Cargar datos al iniciar la aplicación
    productos = cargar_datos()
    cargar_datos_treeview(treeview)

    # Crear y configurar los botones
    tk.Button(usuario_informacion, text="Ingresar Producto", command=dar_alta_producto).grid(row=3, column=0, padx=5, pady=55)
    tk.Button(usuario_informacion, text="Modificar Producto", command=modificar_producto).grid(row=3, column=1, padx=5, pady=55)
    tk.Button(usuario_informacion, text="Eliminar Producto", command=eliminar_producto).grid(row=3, column=2, padx=5, pady=55)
    tk.Button(usuario_informacion, text="Salir", command=salir_gestion_producto).grid(row=3, column=3, padx=5, pady=55)

