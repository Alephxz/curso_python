import csv

class Animal:
    """Clase que representa un animal del zoológico"""
    
    def __init__(self, nombre, pelo, plumas, huevos, leche, vuela, acuatico, 
                 depredador, dientes, espinazo, respira, venenoso, aletas, 
                 patas, cola, domestico, tamanio_gato, clase):
        self.nombre = nombre
        self.pelo = int(pelo)
        self.plumas = int(plumas)
        self.huevos = int(huevos)
        self.leche = int(leche)
        self.vuela = int(vuela)
        self.acuatico = int(acuatico)
        self.depredador = int(depredador)
        self.dientes = int(dientes)
        self.espinazo = int(espinazo)
        self.respira = int(respira)
        self.venenoso = int(venenoso)
        self.aletas = int(aletas)
        self.patas = int(patas)
        self.cola = int(cola)
        self.domestico = int(domestico)
        self.tamanio_gato = int(tamanio_gato)
        self.clase = int(clase)
    
    def __str__(self):
        caracteristicas = []
        if self.pelo: caracteristicas.append("tiene pelo")
        if self.plumas: caracteristicas.append("tiene plumas")
        if self.huevos: caracteristicas.append("pone huevos")
        if self.leche: caracteristicas.append("produce leche")
        if self.vuela: caracteristicas.append("vuela")
        if self.acuatico: caracteristicas.append("es acuático")
        if self.depredador: caracteristicas.append("es depredador")
        if self.venenoso: caracteristicas.append("es venenoso")
        
        return f"{self.nombre} - Características: {', '.join(caracteristicas)}"
    
    def __repr__(self):
        """Representación para depuración"""
        return f"Animal('{self.nombre}', clase={self.clase})"
    
    def to_csv_row(self):
        """Convierte el objeto a una fila para CSV"""
        return [
            f'"{self.nombre}"', self.pelo, self.plumas, self.huevos, self.leche,
            self.vuela, self.acuatico, self.depredador, self.dientes, self.espinazo,
            self.respira, self.venenoso, self.aletas, self.patas, self.cola,
            self.domestico, self.tamanio_gato, self.clase
        ]


def cargar_archivo(nombre_archivo):
    """
    Carga un archivo CSV y lo convierte en un diccionario.
    Para clases.csv: {id: nombre_clase}
    Para zoo.csv: {nombre_animal: Animal}
    """
    datos = {}
    
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector)  # Saltar la primera fila (encabezados)
            
            if nombre_archivo == 'clases.csv':
                for fila in lector:
                    if fila and len(fila) >= 2:  # Verificar que la fila no esté vacía
                        id_clase = int(fila[0])
                        nombre_clase = fila[1]
                        datos[id_clase] = nombre_clase
            else:  # zoo.csv
                for fila in lector:
                    if fila and len(fila) >= 18:  # Verificar que tenga todos los campos
                        # Limpiar el nombre de posibles comillas adicionales
                        nombre = fila[0].strip('"')
                        animal = Animal(
                            nombre,  # nombre
                            fila[1], fila[2], fila[3], fila[4], fila[5], fila[6],
                            fila[7], fila[8], fila[9], fila[10], fila[11], fila[12],
                            fila[13], fila[14], fila[15], fila[16], fila[17]
                        )
                        datos[nombre] = animal
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {nombre_archivo}")
    except Exception as e:
        print(f"Error al cargar {nombre_archivo}: {e}")
    
    return datos


def guardar_archivo(nombre_archivo, datos, clases=None):
    """
    Guarda los datos en un archivo CSV.
    Para zoo.csv: guarda los objetos Animal
    Para clases.csv: guarda el diccionario de clases
    """
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
            if nombre_archivo == 'clases.csv':
                writer = csv.writer(archivo)
                writer.writerow(['Clase_id', 'Clase_tipo'])
                for id_clase, nombre_clase in datos.items():
                    writer.writerow([id_clase, nombre_clase])
            else:  # zoo.csv
                writer = csv.writer(archivo)
                writer.writerow([
                    'nombre_animal', 'pelo', 'plumas', 'huevos', 'leche', 'vuela',
                    'acuatico', 'depredador', 'dientes', 'espinazo', 'respira',
                    'venenoso', 'aletas', 'patas', 'cola', 'domestico',
                    'tamanio_gato', 'clase'
                ])
                # Ordenar los animales por nombre para mejor organización
                animales_ordenados = sorted(datos.values(), key=lambda x: x.nombre)
                for animal in animales_ordenados:
                    writer.writerow(animal.to_csv_row())
        
        print(f"Archivo {nombre_archivo} guardado exitosamente con {len(datos)} registros")
        return True
    except Exception as e:
        print(f"Error al guardar {nombre_archivo}: {e}")
        return False


def listar_por_clase(animales, clases):
    """Lista todos los animales de una clase seleccionada por el usuario"""
    print("\n--- Clases disponibles ---")
    for id_clase, nombre_clase in clases.items():
        print(f"{id_clase}. {nombre_clase}")
    
    try:
        opcion = int(input("\nSeleccione el número de la clase: "))
        if opcion not in clases:
            print("Opción no válida")
            return
        
        clase_seleccionada = clases[opcion]
        animales_clase = []
        
        for animal in animales.values():
            if animal.clase == opcion:
                animales_clase.append(animal)
        
        if animales_clase:
            print(f"\n--- Animales de la clase {clase_seleccionada} ({len(animales_clase)} encontrados) ---")
            # Ordenar alfabéticamente
            animales_clase.sort(key=lambda x: x.nombre)
            for i, animal in enumerate(animales_clase, 1):
                print(f"  {i}. {animal}")
        else:
            print(f"\nNo hay animales de la clase {clase_seleccionada}")
            
    except ValueError:
        print("Por favor, ingrese un número válido")


def listar_por_caracteristica(animales):
    """Lista todos los animales que tienen una característica seleccionada"""
    caracteristicas = {
        '1': ('pelo', 'tienen pelo'),
        '2': ('plumas', 'tienen plumas'),
        '3': ('huevos', 'ponen huevos'),
        '4': ('leche', 'producen leche'),
        '5': ('vuela', 'vuelan'),
        '6': ('acuatico', 'son acuáticos'),
        '7': ('depredador', 'son depredadores'),
        '8': ('venenoso', 'son venenosos'),
        '9': ('domestico', 'son domésticos'),
        '10': ('aletas', 'tienen aletas'),
        '11': ('cola', 'tienen cola'),
        '12': ('dientes', 'tienen dientes'),
        '13': ('espinazo', 'tienen espinazo'),
        '14': ('respira', 'respiran')
    }
    
    print("\n--- Características disponibles ---")
    for key, (_, desc) in caracteristicas.items():
        print(f"{key}. Animales que {desc}")
    
    opcion = input("\nSeleccione el número de la característica: ")
    
    if opcion not in caracteristicas:
        print("Opción no válida")
        return
    
    atributo, descripcion = caracteristicas[opcion]
    animales_caract = []
    
    for animal in animales.values():
        if getattr(animal, atributo) == 1:
            animales_caract.append(animal)
    
    if animales_caract:
        print(f"\n--- Animales que {descripcion} ({len(animales_caract)} encontrados) ---")
        # Ordenar alfabéticamente
        animales_caract.sort(key=lambda x: x.nombre)
        for i, animal in enumerate(animales_caract, 1):
            print(f"  {i}. {animal}")
    else:
        print(f"\nNo hay animales que {descripcion}")


def agregar_animal(animales, clases):
    """Permite agregar un nuevo animal con todas sus características"""
    print("\n--- Agregar nuevo animal ---")
    
    # Mostrar clases disponibles
    print("\nClases disponibles:")
    for id_clase, nombre_clase in clases.items():
        print(f"{id_clase}. {nombre_clase}")
    
    try:
        # Datos básicos
        nombre = input("Nombre del animal: ").strip().lower()
        
        if nombre in animales:
            print(f"El animal '{nombre}' ya existe en la base de datos")
            return animales, False
        
        clase = int(input("Número de la clase: "))
        if clase not in clases:
            print("Clase no válida")
            return animales, False
        
        # Recolectar características (1 = Sí, 0 = No)
        print("\nCaracterísticas (1 = Sí, 0 = No):")
        
        def pedir_caracteristica(mensaje):
            while True:
                try:
                    valor = int(input(mensaje))
                    if valor in [0, 1]:
                        return valor
                    else:
                        print("Por favor, ingrese 0 o 1")
                except ValueError:
                    print("Por favor, ingrese un número válido")
        
        pelo = pedir_caracteristica("¿Tiene pelo? (0/1): ")
        plumas = pedir_caracteristica("¿Tiene plumas? (0/1): ")
        huevos = pedir_caracteristica("¿Pone huevos? (0/1): ")
        leche = pedir_caracteristica("¿Produce leche? (0/1): ")
        vuela = pedir_caracteristica("¿Vuela? (0/1): ")
        acuatico = pedir_caracteristica("¿Es acuático? (0/1): ")
        depredador = pedir_caracteristica("¿Es depredador? (0/1): ")
        dientes = pedir_caracteristica("¿Tiene dientes? (0/1): ")
        espinazo = pedir_caracteristica("¿Tiene espinazo? (0/1): ")
        respira = pedir_caracteristica("¿Respira? (0/1): ")
        venenoso = pedir_caracteristica("¿Es venenoso? (0/1): ")
        aletas = pedir_caracteristica("¿Tiene aletas? (0/1): ")
        
        # Para patas, puede ser más de 1
        while True:
            try:
                patas = int(input("Número de patas: "))
                if patas >= 0:
                    break
                else:
                    print("Por favor, ingrese un número positivo")
            except ValueError:
                print("Por favor, ingrese un número válido")
        
        cola = pedir_caracteristica("¿Tiene cola? (0/1): ")
        domestico = pedir_caracteristica("¿Es doméstico? (0/1): ")
        tamanio_gato = pedir_caracteristica("¿Es más grande que un gato? (0/1): ")
        
        # Crear el nuevo animal
        nuevo_animal = Animal(
            nombre, pelo, plumas, huevos, leche, vuela, acuatico,
            depredador, dientes, espinazo, respira, venenoso, aletas,
            patas, cola, domestico, tamanio_gato, clase
        )
        
        # Preguntar si desea guardar
        print(f"\n--- Resumen del animal ---")
        print(nuevo_animal)
        confirmar = input("\n¿Guardar este animal? (s/n): ").lower()
        
        if confirmar == 's':
            animales[nombre] = nuevo_animal
            print(f"\n¡Animal '{nombre}' agregado exitosamente!")
            return animales, True
        else:
            print("Operación cancelada")
            return animales, False
        
    except Exception as e:
        print(f"Error al agregar el animal: {e}")
        return animales, False


def mostrar_menu():
    """Muestra el menú principal y retorna la opción seleccionada"""
    print("\n" + "="*50)
    print("          SISTEMA DE GESTIÓN DEL ZOOLÓGICO")
    print("="*50)
    print("1. Listar animales por clase")
    print("2. Listar animales por característica")
    print("3. Agregar nuevo animal")
    print("4. Salir")
    print("="*50)
    
    try:
        opcion = int(input("Seleccione una opción: "))
        return opcion
    except ValueError:
        return -1