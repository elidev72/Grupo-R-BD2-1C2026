import json
import random
from datetime import datetime
from faker import Faker
from config import conectar_db, desconectar_db, ic
from models import *

Faker.seed(7)
fake = Faker('es_AR')

def seed_obras_sociales():
    ic("Iniciando siembra de Obras Sociales...")
    docs_creados = []

    for empresa in NombreEmpresa:
        # 1. Buscamos si ya existe
        obj = ObraSocial.objects(nombre=empresa.value).first()
        
        if not obj:
            # 2. Si no existe, lo creamos
            obj = ObraSocial(nombre=empresa.value)
            obj.save()
            ic(f"✅ Obra Social creada: {empresa.value}")
        else:
            ic(f"ℹ️ La Obra Social '{empresa.value}' ya existía.")
            
        docs_creados.append(obj)
    
    ic(f"Finalizado: {len(docs_creados)} Obras Sociales listas.")
    return docs_creados

def generar_ubicacion_faker():
    nueva_ubicacion = Ubicacion(
        calle=fake.street_name(),
        numero=fake.random_int(min=10, max=9999),
        localidad=fake.city(),
        provincia=fake.province()
    )
    return nueva_ubicacion

def seed_laboratorios(cantidad=10):
    ic(f"Siembra: Generando {cantidad} laboratorios...")
    laboratorios_creados = []

    for _ in range(cantidad):
        # Generamos un nombre de empresa realista
        nombre_lab = f"Laboratorio {fake.company()}"
        
        obj = Laboratorio(nombre=nombre_lab)
        
        try:
            obj.save()
            laboratorios_creados.append(obj)
            ic(f"✅ Laboratorio creado: {nombre_lab}")
        except Exception as e:
            ic(f"⚠️ Saltando laboratorio repetido: {nombre_lab}: {e}")

    ic(f"Finalizado: {len(laboratorios_creados)} laboratorios listos.")
    return laboratorios_creados

def seed_cadenas(cantidad=3):
    ic(f"Siembra: Generando {cantidad} cadenas comerciales...")
    cadenas_creadas = []

    for _ in range(cantidad):
        nombre_cadena = f"Farmacias {fake.unique.last_name()}"
        cuit_gen = f"30-{fake.unique.numerify('########')}-{fake.random_digit()}"

        try:
            obj = Cadena(
                nombre=nombre_cadena,
                cuit=cuit_gen
            )
            obj.save()
            
            ic(f"✅ Cadena creada: {nombre_cadena} (CUIT: {cuit_gen})")
            cadenas_creadas.append(obj)

        except Exception as e:
            ic(f"⚠️ Error al crear cadena '{nombre_cadena}': {e}")

    ic(f"Finalizado: {len(cadenas_creadas)} cadenas en la base de datos.")
    return cadenas_creadas

def generar_afiliacion_aleatoria(lista_obras_sociales):
    if not lista_obras_sociales:
        return None
    
    os_elegida = random.choice(lista_obras_sociales)
    
    fecha_alta_gen = fake.date_time_between(start_date='-10y', end_date='now')

    return Afiliacion(
        obra_social=os_elegida,
        numero_afiliado=fake.bothify(text='####-########-#'),
        fecha_alta=fecha_alta_gen
    )

def seed_sucursales(sucursales_por_cadena=3, lista_cadenas=None):
    if not lista_cadenas:
        ic("Error: Se necesita una lista de cadenas para crear sucursales.")
        return []

    ic(f"Siembra: Generando {sucursales_por_cadena} sucursales por cada una de las {len(lista_cadenas)} cadenas...")
    sucursales_creadas = []

    for cadena in lista_cadenas:
        for i in range(sucursales_por_cadena):
            nombre_suc = f"{cadena.nombre} - {fake.first_name()}"
            
            s = Sucursal(
                nombre=nombre_suc,
                cadena=cadena,
                sede= generar_ubicacion_faker()
            )
            
            s.save()
            sucursales_creadas.append(s)
            ic(f"✅ Sucursal creada: {nombre_suc}")

    ic(f"Finalizado: {len(sucursales_creadas)} sucursales listas.")
    return sucursales_creadas

def seed_personas(cantidad_clientes=80, cantidad_empleados=20, lista_sucursales=None, lista_obras=None):
    """
    Siembra Personas respetando reglas de afiliación:
    1. Empleados: SIEMPRE con afiliación.
    2. Clientes: ALGUNOS con afiliación, otros sin ella.
    """
    ic(f"Iniciando siembra de {cantidad_clientes + cantidad_empleados} personas...")
    personas_creadas = []

    roles = [('empleado', cantidad_empleados), ('cliente', cantidad_clientes)]

    for rol, total in roles:
        for _ in range(total):
            es_emp = (rol == 'empleado')
            
            # Generamos DNI único
            dni_gen = str(fake.unique.random_int(min=10000000, max=45000000))
            
            # --- Lógica de Afiliación (Las Reglas) ---
            afiliacion_data = None
            
            if es_emp:
                # Regla 1: Empleado SIEMPRE tiene afiliación
                afiliacion_data = generar_afiliacion_aleatoria(lista_obras)
            else:
                # Regla 2: Cliente tiene 50% de probabilidad de tener obra social
                if fake.boolean(chance_of_getting_true=50):
                    afiliacion_data = generar_afiliacion_aleatoria(lista_obras)

            # --- Construcción del Objeto ---
            p = Persona(
                dni=dni_gen,
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                domicilio=generar_ubicacion_faker(),
                afiliacion=afiliacion_data,
                es_empleado=es_emp
            )

            # --- Campos específicos de Empleado ---
            if es_emp:
                p.cuil = f"20-{dni_gen}-{random.randint(0, 9)}"
                p.es_encargado = fake.boolean(chance_of_getting_true=20)
                if lista_sucursales:
                    p.sucursal_donde_trabaja = random.choice(lista_sucursales)

            try:
                p.save()
                personas_creadas.append(p)
            except Exception as e:
                ic(f"Error al guardar DNI {dni_gen}: {e}")

    ic(f"✅ Siembra de personas finalizada con éxito.")
    return personas_creadas

def seed_productos(cantidad=50, lista_laboratorios=None):
    """
    Siembra N productos. 
    Distribuye los productos entre categorías de Farmacia y Perfumería.
    """
    if not lista_laboratorios:
        ic("Error: Se necesita una lista de laboratorios para asignar a los productos.")
        return []

    ic(f"Siembra: Generando {cantidad} productos...")
    productos_creados = []

    # Listas de palabras para inventar nombres de productos creíbles
    nombres_farma = ["Ibuprofeno", "Amoxicilina", "Paracetamol", "Aspirina", "Enalapril", "Dermaglós"]
    nombres_perfu = ["Shampoo", "Desodorante", "Crema Facial", "Perfume", "Jabón Líquido"]

    for _ in range(cantidad):
        # Elegimos categoría al azar
        es_farma = fake.boolean(chance_of_getting_true=60) # 60% farmacia
        cat_elegida = "farmacia" if es_farma else "perfumería"
        
        # Inventamos una descripción según la categoría
        base = random.choice(nombres_farma if es_farma else nombres_perfu)
        descripcion_gen = f"{base} {fake.word().capitalize()} {random.choice(['Plus', 'Max', 'Gold', 'Forte', '600mg', '500ml'])}"
        
        # Generamos un precio entre 500 y 15000, redondeado a 2 decimales
        precio_gen = round(random.uniform(500.0, 15000.0), 2)

        p = Producto(
            descripcion=descripcion_gen,
            precio=precio_gen,
            categoria=cat_elegida,
            laboratorio=random.choice(lista_laboratorios)
        )
        
        p.save()
        productos_creados.append(p)
        # ic(f"✅ Producto: {descripcion_gen} (${precio_gen})")

    ic(f"Finalizado: {len(productos_creados)} productos listos.")
    return productos_creados

def generar_items_venta(lista_productos, min_items=1, max_items=5):
    items = []
    # Seleccionamos N productos distintos para esta compra
    seleccion = random.sample(lista_productos, k=random.randint(min_items, max_items))
    
    for prod in seleccion:
        item = ItemVenta(
            producto_id=prod,
            cantidad=random.randint(1, 3),
            # DESNORMALIZACIÓN: Copia el precio y categoría actual del producto
            precio_unitario=prod.precio,
            categoria=prod.categoria
        )
        items.append(item)
    return items

def seed_ventas(cantidad=150, lista_personas=None, lista_sucursales=None, lista_productos=None):
    """
    Crea el historial de ventas vinculando todas las entidades y respetando
    las reglas de Forma de Pago y Tipo de Cliente.
    """
    if not all([lista_personas, lista_sucursales, lista_productos]):
        ic("Error: Faltan listas de referencias para sembrar ventas.")
        return []

    ic(f"Siembra: Generando {cantidad} documentos de Venta...")
    
    # Separamos roles
    clientes = [p for p in lista_personas if not p.es_empleado]
    empleados = [p for p in lista_personas if p.es_empleado]
    
    ventas_creadas = []

    for _ in range(cantidad):
        # 1. Elegimos Sucursal y su Cadena padre
        sucursal_actual = random.choice(lista_sucursales)
        cadena_actual = sucursal_actual.cadena # Accedemos a la referencia
        
        # 2. Elegimos un empleado que trabaje en esa sucursal
        vendedores_local = [e for e in empleados if e.sucursal_donde_trabaja == sucursal_actual]
        empleado = random.choice(vendedores_local) if vendedores_local else random.choice(empleados)
        
        # 3. Elegimos un cliente y determinamos su tipo según su afiliación
        cliente_elegido = random.choice(clientes)
        # Si tiene el objeto afiliacion, es 'obra social', sino 'privado'
        tipo_cli = 'obra social' if cliente_elegido.afiliacion else 'privado'
        
        # 4. Elegimos forma de pago al azar de las opciones del Enum
        forma_p = random.choice(['Efectivo', 'Transferencia bancaria', 'Tarjeta de débito', 'Tarjeta de crédito'])

        v = Venta(
            fecha=fake.date_time_between(start_date='-1y', end_date='now'),
            cadena=cadena_actual,
            sucursal=sucursal_actual,
            cliente=cliente_elegido,
            empleado_atiende=empleado,
            items=generar_items_venta(lista_productos), # Usamos la función del paso anterior
            forma_pago=forma_p,
            tipo_cliente=tipo_cli
        )
        
        v.save()
        ventas_creadas.append(v)

    ic(f"✅ Se han generado {len(ventas_creadas)} ventas en la colección 'ventas'.")
    return ventas_creadas

if __name__ == '__main__':
    conectar_db()

    lista_obras = seed_obras_sociales()
    lista_labs = seed_laboratorios()
    lista_cadenas = seed_cadenas()
    
    lista_sucursales = seed_sucursales(sucursales_por_cadena=3, lista_cadenas=lista_cadenas)
    lista_personas = seed_personas(lista_sucursales=lista_sucursales, lista_obras=lista_obras)
    lista_productos = seed_productos(lista_laboratorios=lista_labs)
    
    lista_ventas = seed_ventas(lista_personas=lista_personas, lista_productos= lista_productos, lista_sucursales=lista_sucursales)

    desconectar_db()