"""
Punto de entrada principal del proyecto de Benchmark de Estructuras de Datos.
Este script ejecuta la suite de experimentos, genera los reportes tabulares
en consola, exporta los resultados a CSV y construye las gráficas en escala Log-Log.
"""

from experimentos import ejecutar_experimentos


def main():
    print("-" * 70)
    print(" COMPARATIVO DE ESTRUCTURAS DE DATOS (Lista vs ABB vs B+ Tree)")
    print("-" * 70)

    try:
        # Ejecución única del pipeline de pruebas estadístico
        ejecutar_experimentos()

        print("\n" + "-" * 80)
        print(" PROCESO FINALIZADO CON ÉXITO")
        print(" -> Archivo de datos exportado: 'resultados_estadisticos.csv'")
        print(" -> Gráficas generadas (Log-Log):")
        print("    - 'graficas_operaciones_aleatorias.png'")
        print("    - 'graficas_operaciones_ordenadas.png'")
        print("-" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n\n[!] Ejecución cancelada por el usuario.")
    except Exception as e:
        print(f"\n\n[X] Ocurrió un error inesperado durante la ejecución: {e}")


if __name__ == "__main__":
    main()
