numero = float(input("Ingrese un numero: "))
porcentaje = float(input("Ingrese el porcentaje: "))
porcentaje = porcentaje / 100
resultado1 = (numero * porcentaje)
resultado = (numero + resultado1)
print(f"El ", porcentaje, "% de ", numero, "es: ", resultado)