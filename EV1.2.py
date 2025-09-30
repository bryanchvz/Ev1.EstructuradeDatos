from datetime import datetime

salas = {}
reservaciones = {}
clientes = {}
contador_clientes = 0

def preguntar_continuar(accion):
    while True:
        continuar = input(f"\n¿Desea {accion} otro/a? (s/n): ").strip().lower()
        if continuar in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif continuar in ['n', 'no']:
            return False
        else:
            print("Por favor ingrese 's' para sí o 'n' para no.")

def registrar_cliente():
    global contador_clientes
    
    while True:
        while True:
            nombre = input("Ingrese su nombre: ").strip()
            if nombre and nombre.replace(" ", "").isalpha():
                break
            print("Error: El nombre solo puede contener letras y no puede estar vacío.")

        while True:
            apellidos = input("Ingrese sus apellidos: ").strip()
            if apellidos and apellidos.replace(" ", "").isalpha():
                break
            print("Error: Los apellidos solo pueden contener letras y no pueden estar vacíos.")

        contador_clientes += 1
        clave = f"C{contador_clientes:03d}"
        clientes[clave] = {"nombre": nombre, "apellidos": apellidos}

        print(f"Cliente registrado exitosamente con la clave {clave}")
        
        if not preguntar_continuar("registrar cliente"):
            break

def listar_clientes():
    if not clientes:
        print("No hay clientes registrados.")
        return
    
    print("\n" + "="*60)
    print("LISTA DE CLIENTES REGISTRADOS")
    print("="*60)
    
    clientes_ordenados = sorted(clientes.items(), 
                               key=lambda x: (x[1]["apellidos"].lower(), x[1]["nombre"].lower()))
    
    for clave, datos in clientes_ordenados:
        print(f"{clave}: {datos['apellidos']}, {datos['nombre']}")
    print("="*60)

def registrar_sala():
    while True:
        clave = f"S{len(salas)+1:03d}"
        
        while True:
            nombre = input("Ingrese el nombre de la sala: ").strip()
            if nombre:
                break
            print("Error: El nombre de la sala no puede estar vacío.")
        
        while True:
            try:
                cupo = int(input("Ingrese el cupo máximo de la sala: "))
                if cupo > 0:
                    break
                print("Error: El cupo debe ser mayor a 0.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")
        
        salas[clave] = {"nombre": nombre, "cupo": cupo}
        print(f"Sala registrada exitosamente con clave {clave}: {nombre} (cupo: {cupo})")
        
        if not preguntar_continuar("registrar sala"):
            break

def mostrar_salas_disponibles(fecha_str):
    if not salas:
        return {}
    
    salas_disponibles = {}
    print(f"\nSalas disponibles para {fecha_str}:")
    print("-" * 80)
    
    for clave_sala, info_sala in salas.items():
        turnos_disponibles = ["MATUTINO", "VESPERTINO", "NOCTURNO"]
        
        for reserva in reservaciones.values():
            if reserva["sala"] == clave_sala and reserva["fecha"] == fecha_str:
                if reserva["turno"] in turnos_disponibles:
                    turnos_disponibles.remove(reserva["turno"])
        
        if turnos_disponibles:
            salas_disponibles[clave_sala] = turnos_disponibles
            print(f"{clave_sala}: {info_sala['nombre']} (cupo {info_sala['cupo']}) - Turnos: {', '.join(turnos_disponibles)}")
    
    if not salas_disponibles:
        print("No hay salas disponibles para esta fecha.")
    
    print("-" * 80)
    return salas_disponibles

def registrar_reservacion():
    if not clientes:
        print("Error: Primero debe registrar clientes.")
        return
    if not salas:
        print("Error: Primero debe registrar salas.")
        return

    while True:
        listar_clientes()
        while True:
            cliente = input("\nIngrese la clave del cliente: ").strip().upper()
            if cliente in clientes:
                break
            print("Error: Clave de cliente inválida.")

        while True:
            fecha_str = input("Ingrese la fecha de reserva (YYYY-MM-DD): ").strip()
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                hoy = datetime.now()
                diferencia_dias = (fecha - hoy).days
                if diferencia_dias >= 2:
                    break
                print("Error: La fecha debe ser al menos dos días después de hoy.")
            except ValueError:
                print("Error: Formato de fecha inválido. Use YYYY-MM-DD")

        salas_disponibles = mostrar_salas_disponibles(fecha_str)
        if not salas_disponibles:
            if not preguntar_continuar("intentar reservación"):
                break
            continue

        while True:
            sala = input("Ingrese la clave de la sala: ").strip().upper()
            if sala in salas_disponibles:
                break
            print("Error: Clave de sala inválida o no disponible.")

        turnos_validos = salas_disponibles[sala]
        print(f"Turnos disponibles: {', '.join(turnos_validos)}")
        while True:
            turno = input("Ingrese el turno (MATUTINO/VESPERTINO/NOCTURNO): ").strip().upper()
            if turno in turnos_validos:
                break
            print("Error: Turno no válido o no disponible.")

        while True:
            evento = input("Ingrese el nombre del evento: ").strip()
            if evento:
                break
            print("Error: El nombre del evento no puede estar vacío.")

        folio = f"R{len(reservaciones)+1:03d}"
        reservaciones[folio] = {
            "cliente": cliente,
            "sala": sala,
            "fecha": fecha_str,
            "turno": turno,
            "evento": evento
        }
        
        cliente_info = clientes[cliente]
        sala_info = salas[sala]
        print(f"\n¡Reservación registrada exitosamente!")
        print(f"Folio: {folio}")
        print(f"Cliente: {cliente_info['nombre']} {cliente_info['apellidos']}")
        print(f"Sala: {sala_info['nombre']}")
        print(f"Fecha: {fecha_str}")
        print(f"Turno: {turno}")
        print(f"Evento: {evento}")
        
        if not preguntar_continuar("hacer reservación"):
            break

def editar_evento():
    if not reservaciones:
        print("No hay reservaciones registradas.")
        return
    
    while True:
        print("\n" + "="*60)
        print("RESERVACIONES EXISTENTES")
        print("="*60)
        
        for folio, reserva in reservaciones.items():
            cliente_info = clientes[reserva["cliente"]]
            sala_info = salas[reserva["sala"]]
            print(f"{folio}: {reserva['evento']} - {cliente_info['nombre']} {cliente_info['apellidos']} - "
                  f"Sala {sala_info['nombre']} - {reserva['fecha']} ({reserva['turno']})")
        
        while True:
            folio = input("\nIngrese el folio de la reservación a editar: ").strip().upper()
            if folio in reservaciones:
                break
            print("Error: Folio de reservación inválido.")
        
        print(f"Evento actual: {reservaciones[folio]['evento']}")
        while True:
            nuevo_evento = input("Ingrese el nuevo nombre del evento: ").strip()
            if nuevo_evento:
                reservaciones[folio]['evento'] = nuevo_evento
                print("¡Evento actualizado exitosamente!")
                break
            print("Error: El nombre del evento no puede estar vacío.")
        
        if not preguntar_continuar("editar evento"):
            break

def consultar_reservaciones():
    if not reservaciones:
        print("No hay reservaciones registradas.")
        return
    
    while True:
        while True:
            fecha_consulta = input("Ingrese la fecha a consultar (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(fecha_consulta, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Formato de fecha inválido. Use YYYY-MM-DD")
        
        reservas_fecha = []
        for folio, reserva in reservaciones.items():
            if reserva["fecha"] == fecha_consulta:
                reservas_fecha.append((folio, reserva))
        
        if not reservas_fecha:
            print(f"No hay reservaciones para la fecha {fecha_consulta}")
        else:
            print(f"\n" + "="*80)
            print(f"RESERVACIONES PARA EL DÍA {fecha_consulta}")
            print("="*80)
            print(f"{'FOLIO':<8} {'SALA':<15} {'CLIENTE':<25} {'EVENTO':<20} {'TURNO'}")
            print("-"*80)
            
            for folio, reserva in sorted(reservas_fecha, key=lambda x: x[1]["turno"]):
                cliente_info = clientes[reserva["cliente"]]
                sala_info = salas[reserva["sala"]]
                cliente_nombre = f"{cliente_info['nombre']} {cliente_info['apellidos']}"
                
                print(f"{folio:<8} {sala_info['nombre']:<15} {cliente_nombre:<25} "
                      f"{reserva['evento']:<20} {reserva['turno']}")
            print("="*80)
        
        if not preguntar_continuar("consultar fecha"):
            break

def generar_reporte():
    if not reservaciones:
        print("No hay reservaciones registradas.")
        return
    
    while True:
        while True:
            fecha_reporte = input("Ingrese la fecha para el reporte (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(fecha_reporte, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Formato de fecha inválido. Use YYYY-MM-DD")
        
        reservas_reporte = []
        for reserva in reservaciones.values():
            if reserva["fecha"] == fecha_reporte:
                reservas_reporte.append(reserva)
        
        if not reservas_reporte:
            print(f"No hay reservaciones para generar reporte del día {fecha_reporte}")
        else:
            print("\n" + "*" * 80)
            print("**" + " " * 76 + "**")
            print(f"**{f'REPORTE DE RESERVACIONES PARA EL DÍA {fecha_reporte}':^76}**")
            print("**" + " " * 76 + "**")
            print("*" * 80)
            print(f"{'SALA':<6} {'CLIENTE':<20} {'EVENTO':<30} {'TURNO'}")
            print("*" * 80)
            
            reservas_ordenadas = sorted(reservas_reporte, 
                                       key=lambda x: int(x["sala"][1:]))
            
            for reserva in reservas_ordenadas:
                sala_num = reserva["sala"][1:]
                cliente_info = clientes[reserva["cliente"]]
                cliente_nombre = f"{cliente_info['apellidos']} {cliente_info['nombre']}"
                
                print(f"{sala_num:<6} {cliente_nombre:<20} {reserva['evento']:<30} {reserva['turno']}")
            
            print("*" * 27 + " FIN DEL REPORTE " + "*" * 27)
            print()
        
        if not preguntar_continuar("generar reporte"):
            break

def mostrar_menu():
    print("\n" + "="*60)
    print("--- Menú de Opciones ---")
    print("="*60)
    print("1. Registrar reservación de una sala")
    print("2. Editar el nombre del evento de una reservación ya hecha")
    print("3. Consultar las reservaciones existentes para una fecha específica")
    print("4. Registrar un nuevo cliente")
    print("5. Registrar una sala")
    print("6. Generar reporte de reservaciones")
    print("7. Salir")
    print("="*60)

def main():
    
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Seleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                registrar_reservacion()
            elif opcion == "2":
                editar_evento()
            elif opcion == "3":
                consultar_reservaciones()
            elif opcion == "4":
                registrar_cliente()
            elif opcion == "5":
                registrar_sala()
            elif opcion == "6":
                generar_reporte()
            elif opcion == "7":
                print("Saliendo del programa...")
                break
            else:
                print("Error: Opción inválida. Por favor seleccione una opción del 1 al 7.")
                
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            print("¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            print("Por favor intente nuevamente.")

if __name__ == "__main__":
    main()