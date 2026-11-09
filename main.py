"""Programa principal del Sistema de Gestión de la Clínica Veterinaria "Huellitas".

Ejecuta los casos normales y los casos excepcionales del sistema.
Uso:  python main.py
"""

from clinica import (Ave, CitaYaAtendidaError, ClinicaVeterinaria, ErrorClinicaVeterinaria,
                     EspecieNoAtendidaError, Gato, HorarioNoDisponibleError, Paciente,
                     PacienteNoEncontradoError, Perro, Propietario, Veterinario,
                     VeterinarioNoEncontradoError, formato_pesos)


def seccion(numero, titulo):
    print()
    print("=" * 78)
    print(f" {numero}. {titulo}")
    print("=" * 78)


def main():
    # ------------------------------------------------------------------
    seccion(1, "Creación de la clínica, propietarios y veterinarios")
    # ------------------------------------------------------------------
    clinica = ClinicaVeterinaria("Clínica Veterinaria Huellitas", "Cra. 23 #45-10, Manizales")
    print(f"  Clínica creada: {clinica.nombre} - {clinica.direccion}")

    laura = Propietario("1053001001", "Laura Gómez", "3104567890")
    andres = Propietario("1053002002", "Andrés Ríos", "3127654321")
    marta = Propietario("1053003003", "Marta Salazar", "8861234")

    dra_valencia = Veterinario("TP-1001", "Camila Valencia", "Medicina general",
                               ["Perro", "Gato"])
    dr_ospina = Veterinario("TP-2002", "Julián Ospina", "Animales exóticos",
                            ["Ave", "Gato"])
    for veterinario in (dra_valencia, dr_ospina):
        clinica.registrar_veterinario(veterinario)
        veterinario.mostrar_informacion()

    # ------------------------------------------------------------------
    seccion(2, "Registro de pacientes (2 perros, 2 gatos y 2 aves)")
    # ------------------------------------------------------------------
    max_ = Perro("P-001", "Max", 5, 32.5, laura, "Labrador", "grande", True)
    lola = Perro("P-002", "Lola", 2, 6.0, andres, "Pinscher", "pequeño", False)
    misu = Gato("G-001", "Misu", 3, 4.2, laura, es_de_interior=True, esterilizado=True)
    tom = Gato("G-002", "Tom", 1, 3.6, marta, es_de_interior=False, esterilizado=False)
    kiwi = Ave("A-001", "Kiwi", 4, 0.4, andres, "Loro", puede_volar=True)
    piolin = Ave("A-002", "Piolín", 1, 0.03, marta, "Canario", puede_volar=False)

    for paciente in (max_, lola, misu, tom, kiwi, piolin):
        clinica.registrar_paciente(paciente)
        print(f"  Registrado: {paciente}")

    # ------------------------------------------------------------------
    seccion(3, "La clase abstracta Paciente no se puede instanciar")
    # ------------------------------------------------------------------
    try:
        Paciente("X-000", "Genérico", 1, 1.0, laura)
    except TypeError as error:
        print(f"  TypeError controlado -> {error}")
    print("  El programa continúa: solo se crean perros, gatos y aves.")

    # ------------------------------------------------------------------
    seccion(4, "Validación de datos (encapsulamiento)")
    # ------------------------------------------------------------------
    pruebas_invalidas = [
        ("Peso negativo", lambda: setattr(max_, "peso", -3)),
        ("Edad no entera", lambda: setattr(lola, "edad", "dos")),
        ("Tamaño inexistente", lambda: setattr(max_, "tamano", "gigante")),
        ("Teléfono con letras", lambda: setattr(laura, "telefono", "310ABC")),
        ("Fecha imposible", lambda: clinica.agendar_cita("P-001", "TP-1001",
                                                         "2026-02-30", "09:00", "Control")),
    ]
    for descripcion, prueba in pruebas_invalidas:
        try:
            prueba()
        except ValueError as error:
            print(f"  {descripcion}: ValueError -> {error}")
    print(f"  Los datos se conservan: {max_.nombre} sigue pesando {max_.peso} kg "
          f"y es de tamaño {max_.tamano}.")

    max_.peso = 33.1  # modificación válida
    print(f"  Modificación válida: nuevo peso de {max_.nombre} = {max_.peso} kg.")

    # ------------------------------------------------------------------
    seccion(5, "Polimorfismo: una colección heterogénea y un único ciclo")
    # ------------------------------------------------------------------
    pacientes = [max_, misu, kiwi, lola, tom, piolin]
    for paciente in pacientes:
        paciente.mostrar_informacion()
        print(f"  Costo de consulta: {formato_pesos(paciente.calcular_costo_consulta())}")
        print(f"  Cuidados: {paciente.describir_cuidados()}")
        print("  " + "-" * 60)

    # ------------------------------------------------------------------
    seccion(6, "Métodos propios de cada clase hija")
    # ------------------------------------------------------------------
    print(f"  Antes: {lola.describir_cuidados()}")
    lola.vacunar_antirrabica()
    print(f"  Después: {lola.describir_cuidados()}")

    print(f"  Costo de {tom.nombre} antes: {formato_pesos(tom.calcular_costo_consulta())}")
    tom.esterilizar()
    print(f"  Costo de {tom.nombre} después: {formato_pesos(tom.calcular_costo_consulta())}")

    kiwi.recortar_alas()
    kiwi.recortar_alas()  # segunda vez: ya estaban recortadas

    # ------------------------------------------------------------------
    seccion(7, "Agenda de citas (casos normales)")
    # ------------------------------------------------------------------
    cita_max = clinica.agendar_cita("P-001", "TP-1001", "2026-11-20", "09:00", "Control anual")
    cita_misu = clinica.agendar_cita("G-001", "TP-1001", "2026-11-20", "10:00", "Vómito")
    cita_kiwi = clinica.agendar_cita("A-001", "TP-2002", "2026-11-20", "09:00", "Revisión de plumaje")
    cita_tom = clinica.agendar_cita("G-002", "TP-2002", "2026-11-21", "15:30", "Vacunación")
    for cita in (cita_max, cita_misu, cita_kiwi, cita_tom):
        cita.mostrar_informacion()

    # ------------------------------------------------------------------
    seccion(8, "Casos excepcionales del dominio")
    # ------------------------------------------------------------------
    print("  a) Veterinario ocupado en esa fecha y hora:")
    try:
        clinica.agendar_cita("P-002", "TP-1001", "2026-11-20", "09:00", "Desparasitación")
    except HorarioNoDisponibleError as error:
        print(f"     Excepción controlada -> {error}")
    otra = clinica.agendar_cita("P-002", "TP-1001", "2026-11-20", "11:00", "Desparasitación")
    print(f"     El sistema continúa: se agendó en otro horario -> Cita N.° {otra.numero} a las {otra.hora}")

    print("  b) Veterinario que no atiende la especie del paciente:")
    try:
        clinica.agendar_cita("A-002", "TP-1001", "2026-11-22", "08:00", "Revisión de patas")
    except EspecieNoAtendidaError as error:
        print(f"     Excepción controlada -> {error}")
    otra = clinica.agendar_cita("A-002", "TP-2002", "2026-11-22", "08:00", "Revisión de patas")
    print(f"     El sistema continúa: se asignó a {otra.veterinario.nombre} -> Cita N.° {otra.numero}")

    print("  c) Búsqueda de un paciente que no existe:")
    try:
        clinica.buscar_paciente("P-999")
    except PacienteNoEncontradoError as error:
        print(f"     Excepción controlada -> {error}")
    print(f"     El sistema continúa: búsqueda de P-001 -> {clinica.buscar_paciente('P-001')}")

    print("  d) Veterinario que no existe:")
    try:
        clinica.agendar_cita("G-001", "TP-9999", "2026-11-23", "08:00", "Control")
    except VeterinarioNoEncontradoError as error:
        print(f"     Excepción controlada -> {error}")

    print("  e) Atender dos veces la misma cita:")
    valor = clinica.atender_cita(cita_max.numero, "Paciente sano", "Refuerzo de vacunas")
    print(f"     Primera atención correcta de la cita N.° {cita_max.numero}. Cobro: {formato_pesos(valor)}")
    try:
        clinica.atender_cita(cita_max.numero, "Repetido", "Repetido")
    except CitaYaAtendidaError as error:
        print(f"     Excepción controlada -> {error}")

    print("  f) Captura general con la excepción base del sistema:")
    try:
        clinica.buscar_veterinario("TP-0000")
    except ErrorClinicaVeterinaria as error:
        print(f"     {type(error).__name__} capturada como ErrorClinicaVeterinaria -> {error}")

    # ------------------------------------------------------------------
    seccion(9, "Atención de citas e historia clínica (composición)")
    # ------------------------------------------------------------------
    clinica.atender_cita(cita_misu.numero, "Gastritis leve", "Dieta blanda por 3 días")
    clinica.atender_cita(cita_kiwi.numero, "Muda normal de plumas", "Vitaminas en el agua")
    clinica.atender_cita(cita_tom.numero, "Paciente sano", "Vacuna triple felina")
    # Segunda visita de Max: su historia acumula dos registros.
    control = clinica.agendar_cita("P-001", "TP-1001", "2026-12-04", "09:00", "Revisión de oído")
    clinica.atender_cita(control.numero, "Otitis externa", "Gotas óticas por 7 días")

    for paciente in (max_, misu, piolin):
        paciente.historia.mostrar()
    print(f"  Último registro de {max_.nombre}: {max_.historia.ultimo_registro()['diagnostico']}")

    # ------------------------------------------------------------------
    seccion(10, "Resumen: propietarios con sus mascotas y agenda de la clínica")
    # ------------------------------------------------------------------
    for propietario in (laura, andres, marta):
        propietario.mostrar_informacion()
    print()
    clinica.mostrar_agenda()

    print()
    print("Fin de la ejecución: todas las excepciones fueron controladas.")


if __name__ == "__main__":
    main()
