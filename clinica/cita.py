"""Cita médica entre un paciente y un veterinario."""

from .excepciones import CitaYaAtendidaError
from .validaciones import formato_pesos, validar_fecha, validar_hora, validar_texto


class Cita:
    """Asocia un paciente con un veterinario en una fecha y hora.

    Paciente y veterinario existen por su cuenta y se reciben ya creados
    (asociación). La cita solo los relaciona.
    """

    PROGRAMADA = "Programada"
    ATENDIDA = "Atendida"
    CANCELADA = "Cancelada"

    _contador = 0  # para numerar las citas de forma consecutiva

    def __init__(self, paciente, veterinario, fecha, hora, motivo):
        # Primero se validan los datos; el número solo se asigna si todo es correcto.
        self._fecha = validar_fecha(fecha)
        self._hora = validar_hora(hora)
        self._motivo = validar_texto(motivo, "motivo")
        self._paciente = paciente
        self._veterinario = veterinario
        Cita._contador += 1
        self._numero = Cita._contador
        self._estado = Cita.PROGRAMADA
        self._valor_cobrado = 0

    @property
    def numero(self):
        return self._numero

    @property
    def paciente(self):
        return self._paciente

    @property
    def veterinario(self):
        return self._veterinario

    @property
    def fecha(self):
        return self._fecha

    @property
    def hora(self):
        return self._hora

    @property
    def motivo(self):
        return self._motivo

    @property
    def estado(self):
        return self._estado

    @property
    def valor_cobrado(self):
        return self._valor_cobrado

    def esta_programada(self):
        return self._estado == Cita.PROGRAMADA

    def ocupa(self, veterinario, fecha, hora):
        """True si esta cita bloquea al veterinario en esa fecha y hora."""
        return (self.esta_programada() and self._veterinario is veterinario
                and self._fecha == fecha and self._hora == hora)

    def atender(self, diagnostico, tratamiento):
        """Registra la atención en la historia clínica y cobra la consulta.

        El valor se obtiene con calcular_costo_consulta(): la cita no sabe
        si el paciente es perro, gato o ave (polimorfismo).
        """
        if self._estado == Cita.ATENDIDA:
            raise CitaYaAtendidaError(self._numero)
        if self._estado == Cita.CANCELADA:
            raise ValueError(f"La cita N.° {self._numero} está cancelada y no puede atenderse.")
        self._paciente.registrar_atencion(self._fecha, self._veterinario.nombre,
                                          diagnostico, tratamiento)
        self._valor_cobrado = self._paciente.calcular_costo_consulta()
        self._estado = Cita.ATENDIDA
        return self._valor_cobrado

    def cancelar(self):
        if self._estado == Cita.ATENDIDA:
            raise CitaYaAtendidaError(self._numero)
        self._estado = Cita.CANCELADA

    def mostrar_informacion(self):
        linea = (f"  Cita N.° {self._numero} | {self._fecha} {self._hora} | {self._paciente} "
                 f"con {self._veterinario.nombre} | {self._motivo} | {self._estado}")
        if self._estado == Cita.ATENDIDA:
            linea += f" | {formato_pesos(self._valor_cobrado)}"
        print(linea)
