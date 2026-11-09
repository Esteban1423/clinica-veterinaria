"""Clase que administra pacientes, veterinarios y la agenda de citas."""

from .cita import Cita
from .excepciones import (EspecieNoAtendidaError, HorarioNoDisponibleError,
                          PacienteNoEncontradoError, VeterinarioNoEncontradoError)
from .validaciones import formato_pesos, validar_fecha, validar_hora, validar_texto


class ClinicaVeterinaria:
    """Punto de entrada del sistema: registra y busca, y controla la agenda."""

    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion
        self._pacientes = {}     # código -> Paciente
        self._veterinarios = {}  # tarjeta profesional -> Veterinario
        self._citas = []

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre de la clínica")

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = validar_texto(valor, "dirección")

    @property
    def pacientes(self):
        return list(self._pacientes.values())

    @property
    def citas(self):
        return list(self._citas)

    # ----- Registro y búsqueda -----
    def registrar_paciente(self, paciente):
        if paciente.codigo in self._pacientes:
            raise ValueError(f"Ya existe un paciente con el código '{paciente.codigo}'.")
        self._pacientes[paciente.codigo] = paciente

    def registrar_veterinario(self, veterinario):
        if veterinario.tarjeta_profesional in self._veterinarios:
            raise ValueError(f"Ya existe un veterinario con la tarjeta '{veterinario.tarjeta_profesional}'.")
        self._veterinarios[veterinario.tarjeta_profesional] = veterinario

    def buscar_paciente(self, codigo):
        paciente = self._pacientes.get(codigo)
        if paciente is None:
            raise PacienteNoEncontradoError(codigo)
        return paciente

    def buscar_veterinario(self, tarjeta):
        veterinario = self._veterinarios.get(tarjeta)
        if veterinario is None:
            raise VeterinarioNoEncontradoError(tarjeta)
        return veterinario

    def buscar_cita(self, numero):
        for cita in self._citas:
            if cita.numero == numero:
                return cita
        raise ValueError(f"No existe la cita N.° {numero}.")

    # ----- Agenda -----
    def agendar_cita(self, codigo_paciente, tarjeta_veterinario, fecha, hora, motivo):
        """Crea una cita después de comprobar paciente, veterinario, especie y horario."""
        paciente = self.buscar_paciente(codigo_paciente)
        veterinario = self.buscar_veterinario(tarjeta_veterinario)

        if not veterinario.puede_atender(paciente):
            raise EspecieNoAtendidaError(veterinario.nombre, paciente.especie)

        fecha = validar_fecha(fecha)
        hora = validar_hora(hora)
        for cita in self._citas:
            if cita.ocupa(veterinario, fecha, hora):
                raise HorarioNoDisponibleError(veterinario.nombre, fecha, hora)

        nueva = Cita(paciente, veterinario, fecha, hora, motivo)
        self._citas.append(nueva)
        return nueva

    def atender_cita(self, numero, diagnostico, tratamiento):
        return self.buscar_cita(numero).atender(diagnostico, tratamiento)

    # ----- Reportes -----
    def total_facturado(self):
        return sum(cita.valor_cobrado for cita in self._citas)

    def mostrar_agenda(self):
        print(f"  Agenda de {self._nombre}:")
        if not self._citas:
            print("    No hay citas registradas.")
        for cita in self._citas:
            cita.mostrar_informacion()
        print(f"  Total facturado: {formato_pesos(self.total_facturado())}")
