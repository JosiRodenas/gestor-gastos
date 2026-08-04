ahorro = 30
movimiento = 0

while movimiento != 4:
    print("***************")
    print("Bienvenido a tu Banco de confianza ")
    print("***************")


    input("Presiona enter para continuar")
    movimiento = int(input("Introduce la operacion que quiere realizar: 1.ver saldo 2.ingresar dinero 3.retirar dinero 4.salir "))


    if movimiento == 1:
        print("Su saldo es: ", ahorro)
    elif movimiento == 2:
        ingreso = int(input("Introduce la cantidad que desea ingresar: "))
        ahorro += ingreso
        print("Su nuevo saldo es: ", ahorro)
    elif movimiento == 3:
        retiro = int(input("Introduce la cantidad que desea retirar: "))
        if retiro > ahorro:
            print("No tiene suficiente saldo para realizar esta operacion ")
        else:
            ahorro -= retiro
            print("Su nuevo saldo es: ", ahorro)

    elif movimiento == 4:
        print("Gracias por usar nuestro servicio ")
        print("Hasta pronto ")
     