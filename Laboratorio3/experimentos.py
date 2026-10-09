import math
import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from estructuras import SistemaABB, SistemaBPlus, SistemaLista
from modelo import Estudiante


def eliminar_outliers_iqr(datos: list[float]) -> list[float]:
    """Filtra valores atípicos (outliers) usando el método del Rango Intercuartílico (IQR)."""
    if len(datos) < 4:
        return datos
    q25, q75 = np.percentile(datos, [25, 75])
    iqr = q75 - q25
    limite_inferior = q25 - 1.5 * iqr
    limite_superior = q75 + 1.5 * iqr
    filtrados = [x for x in datos if limite_inferior <= x <= limite_superior]
    return filtrados if len(filtrados) > 0 else datos


def ejecutar_experimentos():
    """Ejecuta el benchmark, procesa métricas y despliega tablas e imágenes independientes."""
    tamanos_N = [100, 500, 1000, 2500, 5000, 7500, 10000]
    M = 1000  # Consultas de Búsqueda Exacta
    cant_rangos = 50  # Consultas por Rango
    repeticiones = 15  # <--- Cambiado a 15 ejecuciones por configuración
    resultados = []

    print("\n[+] Ejecutando suite de experimentos estadísticos...")

    for N in tamanos_N:
        print(f"    -> Procesando N = {N}...")

        for modo in ["aleatorio", "ordenado"]:
            for rep in range(repeticiones):
                if modo == "aleatorio":
                    ids = random.sample(range(1, N * 10 + 1), N)
                else:
                    ids = list(range(1, N + 1))

                estudiantes = [Estudiante(i, f"Est_{i}", 20, 4.0) for i in ids]
                ids_busqueda = [random.choice(ids) for _ in range(M)]

                tamano_rango = max(1, N // 10)
                rangos = [
                    (inicio, inicio + tamano_rango)
                    for inicio in [random.choice(ids) for _ in range(cant_rangos)]
                ]

                estructuras = {
                    "Lista": SistemaLista(),
                    "ABB": SistemaABB(),
                    "Arbol_BPlus": SistemaBPlus(orden=16),
                }

                for nombre_est, ds in estructuras.items():
                    # 1. Inserción
                    t0 = time.perf_counter()
                    for est in estudiantes:
                        ds.insertar(est)
                    t_insercion = time.perf_counter() - t0

                    # 2. Búsqueda Exacta
                    t0 = time.perf_counter()
                    if modo == "ordenado" and nombre_est == "ABB" and N > 2500:
                        # Muestra reducida multiplicada escalarmente para evitar cuelgues en el ABB degenerado
                        for target in ids_busqueda[:100]:
                            ds.buscar(target)
                        t_busqueda_exacta = (time.perf_counter() - t0) * (M / 100)
                    else:
                        for target in ids_busqueda:
                            ds.buscar(target)
                        t_busqueda_exacta = time.perf_counter() - t0

                    # 3. Búsqueda por Rango
                    t0 = time.perf_counter()
                    for r_ini, r_fin in rangos:
                        ds.buscar_por_rango(r_ini, r_fin)
                    t_busqueda_rango = time.perf_counter() - t0

                    # 4. Listado Ascendente
                    t0 = time.perf_counter()
                    ds.listar_ascendente()
                    t_listado = time.perf_counter() - t0

                    resultados.append(
                        {
                            "N": N,
                            "Modo": modo,
                            "Estructura": nombre_est,
                            "Repeticion": rep,
                            "Insercion_N_s": t_insercion,
                            "Busqueda_Exacta_M_s": t_busqueda_exacta,
                            "Busqueda_Rango_s": t_busqueda_rango,
                            "Listado_Ascendente_s": t_listado,
                        }
                    )

    # Procesar métricas agregadas mediante Pandas y NumPy
    df = pd.DataFrame(resultados)
    resumen_estadistico = []
    operaciones = [
        "Insercion_N_s",
        "Busqueda_Exacta_M_s",
        "Busqueda_Rango_s",
        "Listado_Ascendente_s",
    ]

    for (N, modo, est), group in df.groupby(["N", "Modo", "Estructura"]):
        registro = {
            "N": N,
            "Modo": modo,
            "Estructura": est,
            "Ejecuciones": repeticiones,
        }
        for op in operaciones:
            tiempos = group[op].tolist()
            tiempos_limpios = eliminar_outliers_iqr(tiempos)
            n_muestras_limpias = len(tiempos_limpios)

            prom = np.mean(tiempos_limpios)
            std = np.std(tiempos_limpios, ddof=1) if n_muestras_limpias > 1 else 0.0

            # Error Estándar considerando la cantidad de datos limpios
            se = std / math.sqrt(n_muestras_limpias) if n_muestras_limpias > 0 else 0.0

            registro[f"{op}_Promedio"] = prom
            registro[f"{op}_Std"] = std
            registro[f"{op}_IC95"] = 1.96 * se

        resumen_estadistico.append(registro)

    df_resumen = pd.DataFrame(resumen_estadistico)
    df_resumen.to_csv("resultados_estadisticos.csv", index=False)

    print("\n[✔] Experimentos finalizados con éxito.")

    # Imprimir en consola las 4 tablas independientes según formato de informe
    imprimir_tablas_informe(df_resumen, max(tamanos_N), M, cant_rangos)

    # Generar gráficos
    generar_graficas_comparativas(df_resumen)


def imprimir_tablas_informe(df: pd.DataFrame, max_N: int, M: int, cant_rangos: int):
    """
    Imprime 4 tablas independientes para el reporte final con métricas completas en milisegundos (ms).
    """
    op_configs = [
        (
            "Insercion_N_s",
            f"EXPERIMENTO 1: INSERCIÓN MASIVA (N = {max_N})",
            f"N={max_N}",
        ),
        (
            "Busqueda_Exacta_M_s",
            f"EXPERIMENTO 2: BÚSQUEDA EXACTA (M = {M}, N = {max_N})",
            f"M={M}",
        ),
        (
            "Busqueda_Rango_s",
            f"EXPERIMENTO 3: BÚSQUEDA POR RANGO ({cant_rangos} CONSULTAS, N = {max_N})",
            f"Rangos={cant_rangos}",
        ),
        (
            "Listado_Ascendente_s",
            f"EXPERIMENTO 4: LISTADO ASCENDENTE COMPLETO (N = {max_N})",
            f"N={max_N}",
        ),
    ]

    for op_col, titulo, parametro_extra in op_configs:
        print(f"\n\n           {titulo}")
        print("-" * 106)
        print(
            f"{'Escenario':<10} | {'Estructura':<12} | {'N':<6} | {'Parámetro':<12} | {'Ejec.':<5} | {'Promedio (ms)':<14} | {'Desv. Est. (ms)':<15} | {'IC 95% (ms)':<12}"
        )
        print("-" * 106)

        for modo in ["aleatorio", "ordenado"]:
            sub_df = df[(df["N"] == max_N) & (df["Modo"] == modo)]
            for _, row in sub_df.iterrows():
                est = row["Estructura"]
                ejec = row["Ejecuciones"]
                prom_ms = row[f"{op_col}_Promedio"] * 1000
                std_ms = row[f"{op_col}_Std"] * 1000
                ic_ms = row[f"{op_col}_IC95"] * 1000

                print(
                    f"{modo.capitalize():<10} | {est:<12} | {max_N:<6} | {parametro_extra:<12} | {ejec:<5} | {prom_ms:14.2f} | {std_ms:15.2f} | {ic_ms:12.2f}"
                )


def generar_graficas_comparativas(df: pd.DataFrame):
    """Construye y guarda los dos paneles de 2x2 en escala LOG-LOG con Desviación Estándar."""
    plt.style.use(
        "seaborn-v0_8-whitegrid"
        if "seaborn-v0_8-whitegrid" in plt.style.available
        else "default"
    )

    estructuras = ["Lista", "ABB", "Arbol_BPlus"]
    ops_titulos = [
        ("Insercion_N_s", "1. Inserción de N Estudiantes"),
        ("Busqueda_Exacta_M_s", "2. M=1000 Búsquedas Exactas"),
        ("Busqueda_Rango_s", "3. Búsquedas por Rango (50 Consultas)"),
        ("Listado_Ascendente_s", "4. Listado Ascendente Completo"),
    ]

    # PANEL 1: ALEATORIOS (Escala Log-Log)
    fig1, axes1 = plt.subplots(2, 2, figsize=(15, 10))
    fig1.suptitle(
        "Desempeño Operacional vs Tamaño N (IDs Aleatorios - Escala Log-Log)",
        fontsize=14,
        fontweight="bold",
    )
    df_rand = df[df["Modo"] == "aleatorio"]

    for idx, (op_col, titulo) in enumerate(ops_titulos):
        ax = axes1[idx // 2, idx % 2]
        for est in estructuras:
            sub = df_rand[df_rand["Estructura"] == est]
            ax.errorbar(
                sub["N"],
                sub[f"{op_col}_Promedio"],
                yerr=sub[f"{op_col}_Std"],  # Desviación Estándar
                marker="o",
                capsize=4,
                label=f"{est} ",
            )
        # CONFIGURACIÓN ESCALA LOG-LOG
        ax.set_xscale("log")  # Eje X Logarítmico (N)
        ax.set_yscale("log")  # Eje Y Logarítmico (Tiempo)

        ax.set_title(titulo)
        ax.set_xlabel("N")
        ax.set_ylabel("Tiempo Total (s)")
        ax.legend()
        ax.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("graficas_operaciones_aleatorias_loglog.png", dpi=300)

    # PANEL 2: ORDENADOS / CASO PATOLÓGICO (Escala Log-Log)
    fig2, axes2 = plt.subplots(2, 2, figsize=(15, 10))
    fig2.suptitle(
        "Desempeño Operacional vs N (IDs Ordenados - Degeneramiento ABB - Escala Log-Log)",
        fontsize=14,
        fontweight="bold",
    )
    df_ord = df[df["Modo"] == "ordenado"]

    for idx, (op_col, titulo) in enumerate(ops_titulos):
        ax = axes2[idx // 2, idx % 2]
        for est in estructuras:
            sub = df_ord[df_ord["Estructura"] == est]
            ax.errorbar(
                sub["N"],
                sub[f"{op_col}_Promedio"],
                yerr=sub[f"{op_col}_Std"],  # Desviación Estándar
                marker="s",
                capsize=4,
                label=f"{est} ",
            )
        # CONFIGURACIÓN ESCALA LOG-LOG
        ax.set_xscale("log")  # Eje X Logarítmico (N)
        ax.set_yscale("log")  # Eje Y Logarítmico (Tiempo)

        ax.set_title(titulo)
        ax.set_xlabel("N")
        ax.set_ylabel("Tiempo Total (s)")
        ax.legend()
        ax.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("graficas_operaciones_ordenadas_loglog.png", dpi=300)

    plt.show()
    plt.close("all")

    print("\n[✔] Gráficas en escala Log-Log guardadas correctamente.")
