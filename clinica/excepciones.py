"""Excepciones personalizadas de la Clínica Veterinaria.

Todas heredan de ErrorClinicaVeterinaria. Así, el programa principal puede
capturar un error concreto o todos los errores del sistema con un solo except.

Los errores de datos (peso negativo, teléfono vacío, etc.) siguen usando
ValueError. Estas excepciones se reservan para situaciones anormales de la
operación de la clínica.
"""


class ErrorClinicaVeterinaria(Exception):
    """Clase base de todos los errores propios del sistema."""


class HorarioNoDisponibleError(ErrorClinicaVeterinaria):
    """El veterinario ya tiene una cita programada en esa fecha y hora."""

    def __init__(self, nombre_veterinario, fecha, hora):
        self.nombre_veterinario = nombre_veterinario
        self.fecha = fecha
        self.hora = hora
        super().__init__(
            f"{nombre_veterinario} ya tiene una cita programada el {fecha} a las {hora}."
        )


class EspecieNoAtendidaError(ErrorClinicaVeterinaria):
    """El veterinario no está habilitado para atender la especie del paciente."""

    def __init__(self, nombre_veterinario, especie):
        self.nombre_veterinario = nombre_veterinario
        self.especie = especie
        super().__init__(
            f"{nombre_veterinario} no atiende pacientes de la especie '{especie}'."
        )


class PacienteNoEncontradoError(ErrorClinicaVeterinaria):
    """El código de paciente buscado no está registrado en la clínica."""

    def __init__(self, codigo):
        self.codigo = codigo
        super().__init__(f"No existe ningún paciente registrado con el código '{codigo}'.")


class VeterinarioNoEncontradoError(ErrorClinicaVeterinaria):
    """La tarjeta profesional buscada no pertenece a ningún veterinario de la clínica."""

    def __init__(self, tarjeta):
        self.tarjeta = tarjeta
        super().__init__(f"No existe ningún veterinario con la tarjeta profesional '{tarjeta}'.")


class CitaYaAtendidaError(ErrorClinicaVeterinaria):
    """Se intenta atender (o cancelar) una cita que ya fue atendida."""

    def __init__(self, numero_cita):
        self.numero_cita = numero_cita
        super().__init__(f"La cita N.° {numero_cita} ya fue atendida y no puede modificarse.")
