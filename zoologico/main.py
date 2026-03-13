import funciones
import os
import sys

def main():
    """Función principal del programa"""
    
    print("="*50)
    print("BIENVENIDO AL SISTEMA DE GESTIÓN DEL ZOOLÓGICO")
    print("="*50)
    
    # Verificar que los archivos existen
    archivos_necesarios = ['clases.csv', 'zoo.csv']
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            print(f"Error: No se encuentra el archivo {archivo}")
            print("Asegúrese de que los archivos están en la misma carpeta que el programa")
            input("Presione Enter para salir...")
            sys.exit(1)
    
    # Cargar datos
    print("\nCargando datos del zoológico...")
    clases = funciones.cargar_archivo('clases.csv')
    animales = funciones.cargar_archivo('zoo.csv')
    
    if not clases:
        print("Error: No se pudieron cargar las clases.")
        input("Presione Enter para salir...")
        sys.exit(1)
    
    if not animales:
        print("Advertencia: No se pudieron cargar los animales o el archivo está vacío.")
        animales = {}  # Inicializar como diccionario vacío
    
    print(f"✓ Se cargaron {len(clases)} clases")
    print(f"✓ Se cargaron {len(animales)} animales")
    
    # Variable para controlar si hubo cambios
    cambios_realizados = False
    
    # Bucle principal del menú
    while True:
        opcion = funciones.mostrar_menu()
        
        if opcion == 1:
            funciones.listar_por_clase(animales, clases)
            
        elif opcion == 2:
            funciones.listar_por_caracteristica(animales)
            
        elif opcion == 3:
            animales_actualizados, cambio = funciones.agregar_animal(animales, clases)
            if cambio:
                animales = animales_actualizados
                cambios_realizados = True
                print("\n⚠️  Animal agregado. No olvide salir para guardar los cambios.")
            
        elif opcion == 4:
            print("\n" + "-"*30)
            print("GUARDANDO CAMBIOS...")
            print("-"*30)
            
            if cambios_realizados:
                print(f"Se guardarán {len(animales)} animales en zoo.csv")
                exito = funciones.guardar_archivo('zoo.csv', animales)
                if exito:
                    print("✓ Datos guardados exitosamente.")
                else:
                    print("✗ Error al guardar los datos.")
            else:
                print("No hay cambios para guardar.")
            
            print("\n¡Gracias por usar el sistema!")
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida. Por favor, seleccione 1-4")
        
        # Pausa para que el usuario vea los resultados
        if opcion in [1, 2, 3]:
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
        print("Los cambios no guardados se perderán")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        input("Presione Enter para salir...")
        sys.exit(1)