import json
import tkinter as tk
from tkinter import *
from tkinter import messagebox

contador_ventas = 1
productos_mostrados = False

def empleado():
    usuario_informacion = tk.Tk()
    usuario_informacion.title("Sistema Ventas")
    usuario_informacion.geometry("1080x800")
    moduloVenta(usuario_informacion)

    usuario_informacion.mainloop()


def moduloVenta(usuario_informacion):
    for widget in usuario_informacion.winfo_children():
            widget.destroy()
    def buscar_producto():
        entrada = entryBuscador.get().strip() 
        if entrada.isdigit(): 
            buscar_por_id(int(entrada))
        else:  
            buscar_por_nombre(entrada)

    def buscar_por_id(id_busqueda):
        listaProductos.delete(0, tk.END)
        with open("productos.json", "r") as file:
            productos = json.load(file)
            for producto in productos:
                if producto["Codigo"] == id_busqueda:
                    producto_str = f"{producto['Codigo']} - {producto['Descripcion']} stock disponible {producto['Cantidad']} --- Precio: {producto['Precio']} "
                    listaProductos.insert(tk.END, producto_str)
                    break
            else:
                listaProductos.insert(tk.END, "No se encontró ningún producto con ese ID.")

    def buscar_por_nombre(nombre_busqueda):
        listaProductos.delete(0, tk.END) 
        with open("productos.json", "r") as file:
            productos = json.load(file)
            for producto in productos:
                if nombre_busqueda.lower() in producto["Descripcion"].lower():
                    producto_str = f"{producto['Codigo']} - {producto['Descripcion']} stock disponible {producto['Cantidad']} --- Precio: {producto['Precio']} "
                    listaProductos.insert(tk.END, producto_str)
            if listaProductos.size() == 0: 
                listaProductos.insert(tk.END, "No se encontró ningún producto con ese nombre.")

    def traer_productos():
        with open("productos.json", "r") as file:
            productos = json.load(file)
        return productos
    
    def mostrar_productos():
        listaProductos.delete(0, tk.END)
        global productos_mostrados
        if listaProductos.size() == 0: 
            productos = traer_productos()
            if productos:
                for producto in productos:
                    listaProductos.insert(tk.END, f"{producto['Codigo']} - {producto['Descripcion']} stock disponible {producto['Cantidad']} --- Precio: {producto['Precio']} ")
                productos_mostrados = True

    def mover_a_carrito():
        cantidad_seleccionada = entryCantidad.get()
        if not cantidad_seleccionada:
            messagebox.showerror("Error", "Por favor, ingresa la cantidad a comprar.")
            return  
        cantidad_seleccionada = float(cantidad_seleccionada)  

        indice_seleccionado = listaProductos.curselection()
        if indice_seleccionado:
            texto_seleccionado = listaProductos.get(indice_seleccionado)
            codigo = texto_seleccionado.split(" ")[0]  
            descripcion = " ".join(texto_seleccionado.split(" ")[1:-3])  
            stock = float(texto_seleccionado.split()[-1]) 
            if cantidad_seleccionada > 0 and cantidad_seleccionada <= stock: 
                carritoProductos.insert(tk.END, f"{codigo} - {descripcion} cantidad a comprar: {cantidad_seleccionada}")
                listaProductos.delete(indice_seleccionado)
                actualizar_stock(texto_seleccionado, cantidad_seleccionada)
                actualizar_total() 
            elif cantidad_seleccionada <= 0:
                messagebox.showerror("Error","La cantidad a comprar debe ser mayor que cero.")
            else:
                messagebox.showerror("Error", "La cantidad a comprar es mayor que la cantidad disponible en stock")
            entryCantidad.delete(0, tk.END)

    def actualizar_total():
        total = 0
        for i in range(carritoProductos.size()):
            producto_texto = carritoProductos.get(i)
            codigo, descripcion_cantidad = producto_texto.split(" - ", 1)
            descripcion, cantidad_texto = descripcion_cantidad.split(" cantidad a comprar: ")
            cantidad_comprada = float(cantidad_texto)
            with open("productos.json", "r") as file:
                productos = json.load(file)
                for producto in productos:
                    if producto["Codigo"] == int(codigo):
                        precio_producto = producto["Precio"]
                        total += cantidad_comprada * precio_producto
                        break
        totalProducto.config(text=f"${total}")

    def actualizar_stock(id_producto, cantidad):
        codigo, stock_texto = id_producto.split(" - ", 2)
        stock = float(stock_texto.split()[-1])
        if cantidad <= stock:
            nuevo_stock = stock - cantidad
            with open("productos.json", "r+") as file:
                productos = json.load(file)
                for producto in productos:
                    if producto["Codigo"] == int(codigo):
                        producto["Cantidad"] = nuevo_stock
                        file.seek(0)
                        json.dump(productos, file, indent=4)
                        file.truncate()
                        break

    def eliminar_de_carrito():
        indice_seleccionado = carritoProductos.curselection()
        if indice_seleccionado:
            producto_texto = carritoProductos.get(indice_seleccionado)
            codigo, descripcion_cantidad = producto_texto.split(" - ", 1)
            descripcion, cantidad_texto = descripcion_cantidad.split(" cantidad a comprar: ")
            cantidad_comprada = int(cantidad_texto)
            with open("productos.json", "r+") as file:
                productos = json.load(file)
                for producto in productos:
                    if producto["Codigo"] == int(codigo):
                        producto["Cantidad"] += cantidad_comprada 
                        file.seek(0)
                        json.dump(productos, file, indent=4)
                        file.truncate()
                        break
            carritoProductos.delete(indice_seleccionado)
            listaProductos.insert(tk.END, f"{codigo} - {descripcion} stock disponible {producto['Cantidad']}")

    def obtener_ultimo_id_venta():
        try:
            with open("venta.json", "r") as file:
                data = json.load(file)
                ventas = data.get("ventas", [])
                if ventas:
                    ultimo_id = ventas[-1]["id_venta"]
                    return ultimo_id + 1
        except FileNotFoundError:
            pass
        return 0

    def actualizar_json(elementos_carrito):
        id_venta = obtener_ultimo_id_venta()
        nueva_venta = {
            "id_venta": id_venta,
            "elementos_carrito": [],
            "venta_total": 0  
        }
        total_venta = 0  
        for elemento in elementos_carrito:
            codigo, descripcion_cantidad = elemento.split(" - ", 1)
            descripcion, cantidad_texto = descripcion_cantidad.split(" cantidad a comprar: ")
            descripcion = descripcion.strip("- ")  
            cantidad_comprada = float(cantidad_texto)
            with open("productos.json", "r+") as file:
                productos = json.load(file)
                for producto in productos:
                    if producto["Codigo"] == int(codigo):
                        precio_unitario = producto["Precio"]
                        precio_total = precio_unitario * cantidad_comprada
                        stock_actualizado = producto["Cantidad"] - cantidad_comprada
                        venta_producto = {
                            "Codigo": int(codigo),
                            "Descripcion": descripcion,
                            "Cantidad": cantidad_comprada,
                            "Precio_Unitario": precio_unitario,
                            "Precio_Total": precio_total,
                            "Stock_Actualizado": stock_actualizado
                        }
                        nueva_venta["elementos_carrito"].append(venta_producto)
                        total_venta += precio_total 
                        break

        nueva_venta["venta_total"] = total_venta 

        try:
            with open("venta.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"ventas": []}

        data["ventas"].append(nueva_venta)

        with open("venta.json", "w") as file:
            json.dump(data, file, indent=4)

    def guardar_ventas():
        total = 0
        elementos_carrito = []
        for i in range(carritoProductos.size()):
            producto_texto = carritoProductos.get(i)
            codigo, descripcion_cantidad = producto_texto.split(" - ", 1)
            descripcion, cantidad_texto = descripcion_cantidad.split(" cantidad a comprar: ")
            cantidad_comprada = float(cantidad_texto)
            with open("productos.json", "r") as file:
                productos = json.load(file)
                for producto in productos:
                    if producto["Codigo"] == int(codigo):
                        precio_producto = producto["Precio"]
                        cantidad_disponible = producto["Cantidad"]
                        if cantidad_comprada <= cantidad_disponible:
                            subtotal = cantidad_comprada * precio_producto
                            total += subtotal
                        break
            elementos_carrito.append(producto_texto)
        totalProducto.config(text=f"${total}")
        actualizar_json(elementos_carrito)
        carritoProductos.delete(0, tk.END)
        totalProducto.config(text="$0")  
        messagebox.showinfo("Venta realizada", "La venta se ha realizado correctamente.")

    #----  ----------------------- listboxs---------------------------------------------------------------------
    listaProductos = tk.Listbox(usuario_informacion, font=("Comic Sans", 10, "bold"), width=92, height=13)
    listaProductos.place(x=400, y=10)

    barralista= Scrollbar(usuario_informacion, command=listaProductos.yview)
    barralista.place(x=1050, y=10, height=240)
    listaProductos.config(yscrollcommand=barralista)


    carritoProductos = tk.Listbox(usuario_informacion, font=("Comic Sans", 10, "bold"), width=92, height=13)
    carritoProductos.place(x=400, y=280)

    barracarrito= Scrollbar(usuario_informacion, command=carritoProductos.yview)
    barracarrito.place(x=1050, y=280, height=240)
    carritoProductos.config(yscrollcommand=barracarrito)

    #--------------------------- etiquetas   ---------------------------------------------------------------------

    etiquetaCantidad = tk.Label(usuario_informacion, text="Cantidad", font=("Comic Sans", 10, "bold"))
    etiquetaCantidad.place(x=130,y=260)

    labelBuscador = tk.Label(usuario_informacion, text="Buscar por ID o por producto:", font=("Comic Sans", 10))
    labelBuscador.place(x=108, y=120)

    totalProducto = tk.Label(usuario_informacion, text=f"$", font=("Comic Sans", 28, "bold"))
    totalProducto.place(x=650,y=545)

    etiquetaTotal = tk.Label(usuario_informacion, text="TOTAL: ", font=("Comic Sans", 24, "bold"))
    etiquetaTotal.place(x=500,y=550)
    #-------------------------------- Botones  ---------------------------------------------------------------
    botonEliminar = Button(usuario_informacion,text="ELIMINAR",height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10, "bold"),command=eliminar_de_carrito)
    botonEliminar.place(x=50, y=350)

    botonAgregar = Button(usuario_informacion,text="AGREGAR",height=2,width=10,bg="blue",fg="white",font=("Comic Sans", 10, "bold"),command=mover_a_carrito)
    botonAgregar.place(x=200, y=350)

    botonCobro = Button(usuario_informacion,text="$ COBRAR",height=3,width=10,bg="green",fg="white",font=("Comic Sans", 10, "bold"),command=guardar_ventas)
    botonCobro.place(x=130, y=450)

    botonBuscarProducto = Button(usuario_informacion, text="BUSCAR",height=2,width=10,bg="white",fg="black",font=("Comic Sans", 10, "bold"),command=buscar_producto)
    botonBuscarProducto.place(x=145, y=180)

    botonBuscar = Button(usuario_informacion,text="Traer todos los Productos",height=1,width=24,bg="grey",fg="white",font=("Comic Sans", 10, "bold"),command=mostrar_productos)
    botonBuscar.place(x=90, y=55)

    #--------------------------- Entradas   ---------------------------------------------------------------------
    entryBuscador = tk.Entry(usuario_informacion)
    entryBuscador.place(x=130, y=150)
    
    entryCantidad = tk.Entry(usuario_informacion)
    entryCantidad.place(x=130,y=290)

