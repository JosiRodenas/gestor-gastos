
gastos = []
CATEGORIAS = ["Alimentación", "Transporte", "Ocio", "Vivienda", "Otros"] #mayusculas para constantes, esto es una lista






while True:
    print("\n1. Añadir gasto")
    print("2. Ver gastos")
    print("3. Eliminar gasto")
    print("0. Salir")

    opcion = input("Elige: ")

    if opcion == "1": #ponemos el 1 entre comillas porque el input siempre devuelve strings

        descripcion = input("Descripcion: ")

        importe = float(input("Importe: "))#float convierte el texto en numero

        for i, cat in enumerate(CATEGORIAS, start=1): #con el enumerate recorremos la listay nos devuelve el indice y el valor, y con el start=1 hacemos que empiece en 1 en vez de 0
            print(f"{i}. {cat}") #imprime "1. Alimentación"

        while True:
            numero = int(input("Categoría: "))
            if 1 <= numero <= len(CATEGORIAS):
                break
            print("Opción no válida, elige entre 1 y", len(CATEGORIAS))

        categoria = CATEGORIAS[numero - 1]
        

        gastos.append({"descripcion": descripcion, "importe": importe, "categoria": categoria}) #el .append() es como el .push()

        
        

        
        print(f"Añadido: {descripcion} - {importe}€") #la f es para poder meter variables dentro de un string, y el {} es para meter la variable dentro del string



    elif opcion == "2":
        total = 0
        por_categoria = {}

        for g in gastos:
            print(f"{g['descripcion']} - {g['importe']:.2f}€ [{g['categoria']}]") #:.2f para que salga 9.50€ en vez de 9.5€. Detalle tonto, pero en algo que maneja dinero se nota.
            total += g['importe']
            por_categoria[g['categoria']] = por_categoria.get(g['categoria'], 0) + g['importe']

        print(f"Total: {total:.2f}€")

        print("\nPor categoría:")
        for categoria, subtotal in por_categoria.items():
            print(f"  {categoria}: {subtotal:.2f}€")

        #se podría hacer      total = sum(g["importe"] for g in gastos)


    elif opcion == "3":

    
        if not gastos:
            print("No hay gastos que eliminar.")
            continue


        for i, gasto in enumerate(gastos, start=1): #con el enumerate recorremos la listay nos devuelve el indice y el valor, y con el start=1 hacemos que empiece en 1 en vez de 0
                    print(f"{i}. {gasto['descripcion']} - {gasto['importe']:.2f}€ [{gasto['categoria']}]") #imprime "1. Alimentación"

        while True:
            try:
                numero = int(input("Elige el gasto a eliminar: "))
                if 1 <= numero <= len(gastos):
                    gasto_eliminado = gastos.pop(numero - 1)
                    print(f"Eliminado: {gasto_eliminado['descripcion']} - {gasto_eliminado['importe']:.2f}€")
                    break
                else:
                    print("Opción no válida, elige entre 1 y", len(gastos))
            except ValueError:
                print("Por favor, introduce un número válido.")

    elif opcion == "0":
        print("Adiós")
        break
    else:
        print("Opción no válida") 