"""Historia clínica de un paciente (parte de la composición con Paciente)."""

from datetime import date

from .validaciones import validar_fecha, validar_texto


class HistoriaClinica:
    """Registro de todas las atenciones que ha recibido un paciente.

    No se crea desde fuera: cada Paciente construye la suya en su constructor.
    Si el paciente deja de existir, su historia clínica también (composición).
    """

    def __init__(self, codigo_paciente):
        self._codigo_paciente = validar_texto(codigo_paciente, "código del paciente")
        self._fecha_apertura = date.today().isoformat()
        self._registros = []

    @property
    def codigo_paciente(self):
        return self._codigo_paciente

    @property
    def fecha_apertura(self):
        return self._fecha_apertura

    @property
    def registros(self):
        """Copia de los registros, para que no se modifiquen desde fuera."""
        return [dict(registro) for registro in self._registros]

    @property
    def cantidad_registros(self):
        return len(self._registros)

    def agregar_registro(self, fecha, nombre_veterinario, diagnostico, tratamiento):
        """Agrega una atención a la historia."""
        self._registros.append({
            "fecha": validar_fecha(fecha),
            "veterinario": validar_texto(nombre_veterinario, "veterinario"),
            "diagnostico": validar_texto(diagnostico, "diagnóstico"),
            "tratamiento": validar_texto(tratamiento, "tratamiento"),
        })

    def ultimo_registro(self):
        """Devuelve la atención más reciente, o None si la historia está vacía."""
        if not self._registros:
            return None
        return dict(self._registros[-1])

    def mostrar(self):
        print(f"  Historia clínica de {self._codigo_paciente} (abierta el {self._fecha_apertura})")
        if not self._registros:
            print("    Sin atenciones registradas.")
            return
        for i, registro in enumerate(self._registros, start=1):
            print(f"    {i}. {registro['fecha']} - {registro['veterinario']}")
            print(f"       Diagnóstico: {registro['diagnostico']}")
            print(f"       Tratamiento: {registro['tratamiento']}")
