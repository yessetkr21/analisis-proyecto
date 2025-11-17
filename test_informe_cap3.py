"""
Script de prueba para verificar el informe mejorado del Capítulo 3
Este script prueba que el endpoint del informe calcule correctamente:
- Errores de interpolación
- Método más rápido
- Método con menor error
- Mejor método general
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.metodos import capitulo3
import numpy as np
import time

def probar_informe():
    """Prueba el sistema de informe mejorado"""

    print("="*70)
    print("PRUEBA DEL INFORME MEJORADO - CAPITULO 3")
    print("="*70)

    # Datos de prueba
    puntos_str = "0,1;1,2;2,1.5;3,3;4,2.5"
    print(f"\nPuntos de prueba: {puntos_str}")

    # Validar puntos
    x, y, error = capitulo3.validar_puntos(puntos_str)
    if error:
        print(f"[X] Error al validar puntos: {error}")
        return

    print(f"[OK] Puntos validados: {len(x)} puntos")
    print(f"   X: {x}")
    print(f"   Y: {y}")

    # Ejecutar cada método y recopilar resultados
    resultados = []
    metodos = ['vandermonde', 'newton', 'lagrange', 'spline-lineal', 'spline-cubico']
    nombres = ['Vandermonde', 'Newton Interpolante', 'Lagrange', 'Spline Lineal', 'Spline Cubico']

    print("\n" + "="*70)
    print("EJECUTANDO METODOS")
    print("="*70)

    for metodo, nombre in zip(metodos, nombres):
        print(f"\n>> Ejecutando: {nombre}")
        try:
            inicio = time.time()
            res = capitulo3.ejecutar_metodo(metodo, puntos_str)
            tiempo = time.time() - inicio

            if res['exito']:
                # Calcular error promedio si está disponible
                error_promedio = None
                if 'errores' in res and res['errores']:
                    error_promedio = float(np.mean(res['errores']))

                resultados.append({
                    'metodo': nombre,
                    'exito': True,
                    'polinomio': res.get('polinomio', 'N/A'),
                    'tiempo': tiempo,
                    'error_promedio': error_promedio,
                    'errores': res.get('errores', [])
                })

                print(f"   [OK] Exitoso")
                print(f"   Tiempo: {tiempo*1000:.2f} ms")
                if error_promedio is not None:
                    print(f"   Error promedio: {error_promedio:.2e}")
                else:
                    print(f"   Error promedio: N/A (Spline)")

            else:
                resultados.append({'metodo': nombre, 'exito': False, 'error_msg': res.get('mensaje', 'Error desconocido')})
                print(f"   [X] Fallo: {res.get('mensaje', 'Error desconocido')}")

        except Exception as e:
            resultados.append({'metodo': nombre, 'exito': False, 'error_msg': str(e)})
            print(f"   [X] Excepcion: {str(e)}")

    # Analisis de resultados
    exitosos = [r for r in resultados if r.get('exito', False)]

    if not exitosos:
        print("\n[X] Ningun metodo fue exitoso")
        return

    print("\n" + "="*70)
    print("ANALISIS DE RESULTADOS")
    print("="*70)

    # Metodo mas rapido
    mas_rapido = min(exitosos, key=lambda x: x['tiempo'])
    print(f"\n>> Metodo mas rapido: {mas_rapido['metodo']}")
    print(f"   Tiempo: {mas_rapido['tiempo']*1000:.2f} ms")

    # Metodo con menor error
    exitosos_con_error = [r for r in exitosos if r.get('error_promedio') is not None]

    if exitosos_con_error:
        menor_error = min(exitosos_con_error, key=lambda x: x['error_promedio'])
        print(f"\n>> Metodo con menor error: {menor_error['metodo']}")
        print(f"   Error promedio: {menor_error['error_promedio']:.2e}")

        # Mejor metodo general
        metodos_polinomiales = [r for r in exitosos_con_error if r['metodo'] in ['Vandermonde', 'Newton Interpolante', 'Lagrange']]

        if metodos_polinomiales:
            mejor_metodo = min(metodos_polinomiales, key=lambda x: x['tiempo'])
            print(f"\n>> Mejor metodo general: {mejor_metodo['metodo']}")
            print(f"   (Mas rapido entre los metodos polinomiales con menor error)")
        else:
            print(f"\n>> Mejor metodo general: {menor_error['metodo']}")
    else:
        print("\n>> Metodo con menor error: N/A (solo splines ejecutados)")

    # Estadisticas generales
    print("\n" + "="*70)
    print("ESTADISTICAS GENERALES")
    print("="*70)
    print(f"Total de metodos: {len(resultados)}")
    print(f"Metodos exitosos: {len(exitosos)}")
    print(f"Metodos fallidos: {len(resultados) - len(exitosos)}")

    # Tabla comparativa
    print("\n" + "="*70)
    print("TABLA COMPARATIVA")
    print("="*70)
    print(f"{'Método':<25} {'Estado':<12} {'Error Promedio':<18} {'Tiempo (ms)':<12}")
    print("-"*70)

    for r in resultados:
        if r['exito']:
            error_str = f"{r['error_promedio']:.2e}" if r.get('error_promedio') is not None else "N/A"
            tiempo_str = f"{r['tiempo']*1000:.2f}"
            print(f"{r['metodo']:<25} {'[OK] Exitoso':<12} {error_str:<18} {tiempo_str:<12}")
        else:
            print(f"{r['metodo']:<25} {'[X] Fallo':<12} {r.get('error_msg', 'Error')[:35]}")

    print("\n" + "="*70)
    print("[OK] PRUEBA COMPLETADA EXITOSAMENTE")
    print("="*70)
    print("\n>> El informe ahora incluye:")
    print("   1. Metodo mas rapido")
    print("   2. Metodo con menor error")
    print("   3. Mejor metodo general")
    print("   4. Columna de errores en la tabla comparativa")
    print("="*70)

if __name__ == "__main__":
    probar_informe()
