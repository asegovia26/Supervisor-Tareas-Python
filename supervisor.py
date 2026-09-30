import subprocess
import sys
import os

# ── Configuración ─────────────────────────────────────────────────
TIMEOUT_SEGUNDOS = 5                # segundos máximos de espera
RUTA_TRABAJADOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "trabajador.py")
PYTHON = sys.executable             # mismo intérprete que ejecuta el supervisor


def ejecutar_trabajador(valor: str, timeout: int = TIMEOUT_SEGUNDOS) -> None:
    """Lanza trabajador.py con *valor* como stdin y muestra el informe."""

    print("=" * 60)
    print(f"  Entrada enviada al trabajador: {valor!r}")
    print("=" * 60)

    try:
        resultado = subprocess.run(
            [PYTHON, RUTA_TRABAJADOR],
            input=valor + "\n",       # enviar el valor por stdin
            capture_output=True,      # capturar stdout y stderr
            text=True,                # modo texto (str en vez de bytes)
            timeout=timeout,          # límite de tiempo
            check=True,              # lanza CalledProcessError si código ≠ 0
        )

        # ── 1. Éxito ─────────────────────────────────────────────
        print(f"  ✅ ÉXITO  (código de retorno: {resultado.returncode})")
        print(f"  stdout → {resultado.stdout.strip()}")
        if resultado.stderr.strip():
            print(f"  stderr → {resultado.stderr.strip()}")

    except subprocess.CalledProcessError as e:
        # ── 2. Error de ejecución (código ≠ 0) ───────────────────
        print(f"  ❌ ERROR DE EJECUCIÓN  (código de retorno: {e.returncode})")
        if e.stdout.strip():
            print(f"  stdout → {e.stdout.strip()}")
        if e.stderr.strip():
            print(f"  stderr → {e.stderr.strip()}")

    except FileNotFoundError:
        # ── 3. Ejecutable inexistente ─────────────────────────────
        print("  ⚠️  EJECUTABLE NO ENCONTRADO")
        print(f"  No se pudo encontrar: {PYTHON} o {RUTA_TRABAJADOR}")

    except subprocess.TimeoutExpired as e:
        # ── 4. Timeout ────────────────────────────────────────────
        print(f"  ⏰ TIMEOUT  (superados {timeout} segundos)")
        if e.stdout:
            salida = e.stdout if isinstance(e.stdout, str) else e.stdout.decode()
            print(f"  stdout parcial → {salida.strip()}")
        if e.stderr:
            error = e.stderr if isinstance(e.stderr, str) else e.stderr.decode()
            print(f"  stderr parcial → {error.strip()}")

    print("-" * 60)
    print()


def parsear_timeout() -> int:
    """Lee --timeout SEG de los argumentos de línea de comandos."""
    timeout = TIMEOUT_SEGUNDOS
    if "--timeout" in sys.argv:
        idx = sys.argv.index("--timeout")
        if idx + 1 < len(sys.argv):
            try:
                timeout = int(sys.argv[idx + 1])
            except ValueError:
                print(f"Valor de timeout no válido: {sys.argv[idx + 1]}. "
                      f"Se usará {TIMEOUT_SEGUNDOS} s.")
    return timeout


def main():
    timeout = parsear_timeout()

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        SUPERVISOR DE TAREAS – Factorial Worker          ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  Timeout configurado: {timeout} segundo(s)")
    print("║  Escribe 'salir' para terminar.                         ║")
    print("║  Escribe 'sleep' para provocar un timeout.              ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    while True:
        try:
            entrada = input("Introduce un valor (o 'salir'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSesión finalizada por el usuario.")
            break

        if entrada.lower() == "salir":
            print("\n¡Hasta luego!")
            break

        ejecutar_trabajador(entrada, timeout=timeout)


if __name__ == "__main__":
    main()
