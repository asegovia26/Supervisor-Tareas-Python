import sys
import math
import time


def main():
    # Leer una línea de stdin
    linea = sys.stdin.readline().strip()

    # ── Modo de prueba: provocar timeout ──────────────────────────
    if linea.lower() == "sleep":
        time.sleep(30)          # duerme lo suficiente para que el supervisor corte
        print("Desperté tras el sleep")
        sys.exit(0)

    # ── Validación ────────────────────────────────────────────────
    if linea == "":
        print("Error: no se recibió ninguna entrada.", file=sys.stderr)
        sys.exit(1)

    try:
        numero = int(linea)
    except ValueError:
        print(f"Error: '{linea}' no es un número entero válido.", file=sys.stderr)
        sys.exit(1)

    if numero < 0:
        print(f"Error: el número {numero} es negativo. Se requiere un entero >= 0.",
              file=sys.stderr)
        sys.exit(1)

    # ── Cálculo del factorial ─────────────────────────────────────
    resultado = math.factorial(numero)
    print(f"El factorial de {numero} es: {resultado}")


if __name__ == "__main__":
    main()
