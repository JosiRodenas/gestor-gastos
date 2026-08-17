#IMPORTAMOS LIBRERIAS
import csv
import os
import sqlite3



# DECLARACION DE VARIABLES Y CONSTANTES
ARCHIVO = "gastos.csv"
CATEGORIAS = ["Alimentación", "Transporte", "Ocio", "Vivienda", "Otros"] #mayusculas para constantes, esto es una lista
BASE_DATOS = "gastos.db"

gastos = []


#FUNCIONES

def crear_tabla():
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            importe REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def cargar():
    #Lee el CSV al arrancar. Si no existe, la lista se queda sin nada
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, newline="", encoding="utf-8") as f: #con el with nos aseguramos de que no ocurren errores y todo se cierra bien al terminar
            for fila in csv.DictReader(f):
                gastos.append({ #append es para añadir
                    "descripcion": fila["descripcion"],
                    "importe": float(fila["importe"]),   # del CSV todo sale en formato texto
                    "categoria": fila["categoria"],
                })
        print(f"Cargados {len(gastos)} gastos")  #len(gastos) es para saber la lnguitud


def guardar():
    #Vuelca la lista completa al CSV. El modo 'w' vacía el fichero y lo pone a 0
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["descripcion", "importe", "categoria"])   # cabecera
        for g in gastos:
            escritor.writerow([g["descripcion"], g["importe"], g["categoria"]])
    print(f"Guardados {len(gastos)} gastos")


def anadir_gasto():
    descripcion = input("Descripcion: ")
    importe = float(input("Importe: "))

    for i, cat in enumerate(CATEGORIAS, start=1):
        print(f"{i}. {cat}")

    while True:
        numero = int(input("Categoría: "))
        if 1 <= numero <= len(CATEGORIAS):
            break
        print("Opción no válida, elige entre 1 y", len(CATEGORIAS))

    categoria = CATEGORIAS[numero - 1]

    conexion = sqlite3.connect(BASE_DATOS)
    conexion.execute(
        "INSERT INTO gastos (descripcion, importe, categoria) VALUES (?, ?, ?)",
        (descripcion, importe, categoria)
    )
    conexion.commit()
    conexion.close()

    print(f"Añadido: {descripcion} - {importe:.2f}€ ({categoria})")


def listar_gastos():
    conexion = sqlite3.connect(BASE_DATOS)
    filas = conexion.execute(
        "SELECT id, descripcion, importe, categoria FROM gastos"
    ).fetchall()
    conexion.close()

    if not filas:
        print("No hay gastos registrados.")
        return

    total = 0
    por_categoria = {}

    for id_gasto, descripcion, importe, categoria in filas:
        print(f"{id_gasto}. {descripcion} - {importe:.2f}€ [{categoria}]")
        total += importe
        por_categoria[categoria] = por_categoria.get(categoria, 0) + importe

    print(f"Total: {total:.2f}€")

    print("\nPor categoría:")
    for categoria, subtotal in por_categoria.items():
        print(f"  {categoria}: {subtotal:.2f}€")

def eliminar_gasto():
    conexion = sqlite3.connect(BASE_DATOS)
    filas = conexion.execute(
        "SELECT id, descripcion, importe, categoria FROM gastos"
    ).fetchall()

    if not filas:
        print("No hay gastos que eliminar.")
        conexion.close()
        return

    for id_gasto, descripcion, importe, categoria in filas:
        print(f"{id_gasto}. {descripcion} - {importe:.2f}€ [{categoria}]")

    ids_validos = [f[0] for f in filas]

    while True:
        try:
            numero = int(input("Elige el id del gasto a eliminar: "))
            if numero in ids_validos:
                break
            print("Ese id no existe.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    conexion.execute("DELETE FROM gastos WHERE id = ?", (numero,))
    conexion.commit()
    conexion.close()
    print(f"Eliminado el gasto {numero}")


def migrar_csv():
    if not os.path.exists(ARCHIVO):
        print("No hay CSV que migrar.")
        return

    conexion = sqlite3.connect(BASE_DATOS)

    ya_hay = conexion.execute("SELECT COUNT(*) FROM gastos").fetchone()[0]
    if ya_hay > 0:
        print(f"La base de datos ya tiene {ya_hay} gastos. Migración cancelada.")
        conexion.close()
        return

    migrados = 0
    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            conexion.execute(
                "INSERT INTO gastos (descripcion, importe, categoria) VALUES (?, ?, ?)",
                (fila["descripcion"], float(fila["importe"]), fila["categoria"])
            )
            migrados += 1

    conexion.commit()
    conexion.close()
    print(f"Migrados {migrados} gastos del CSV a la base de datos")


def mostrar_menu():
    print("\n1. Añadir gasto")
    print("2. Ver gastos")
    print("3. Eliminar gasto")
    print("0. Salir")           
    




# MAIN

crear_tabla()
migrar_csv()

while True:
    mostrar_menu()
    opcion = input("Elija una opción: ")

    if opcion == "1":
        anadir_gasto()
    elif opcion == "2":
        listar_gastos()
    elif opcion == "3":
        eliminar_gasto()
    elif opcion == "0":
        
        print("Adiós")
        break
    else:
        print("Opción no válida")
