while True:
    try:
        as_numero_str = input("Ingrese el número de Sistema Autónomo (AS): ")
        as_numero = int(as_numero_str)

        if 64512 <= as_numero <= 65535 or 4200000000 <= as_numero <= 4294967295:
            print(f"El AS {as_numero} es un AS Privado.")
        elif 1 <= as_numero <= 64511 or 65536 <= as_numero <= 4199999999:
            print(f"El AS {as_numero} es un AS Público.")
        else:
            print("Número de AS inválido. Debe estar entre 1 y 4294967295.")

        break # Sale del bucle si el número es válido

    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número entero.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
