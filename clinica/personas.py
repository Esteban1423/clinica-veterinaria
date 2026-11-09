"""Personas relacionadas con la clínica: propietarios y veterinarios."""

from .validaciones import validar_texto


class Propietario:
    """Dueño de una o varias mascotas (asociación con Paciente)."""

    def __init__(self, documento, nombre, telefono):
        self._documento = validar_texto(documento, "documento")
        self.nombre = nombre
        self.telefono = telefono
        self._mascotas = []

    @property
    def documento(self):
        return self._documento

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        texto = validar_texto(valor, "teléfono")
        if not texto.isdigit() or not 7 <= len(texto) <= 10:
            raise ValueError("El teléfono debe tener entre 7 y 10 dígitos, sin espacios ni letras.")
        self._telefono = texto

    @property
    def mascotas(self):
        return list(self._mascotas)

    def agregar_mascota(self, paciente):
        """La llama el constructor de Paciente. Evita registrar dos veces la misma mascota."""
        if paciente not in self._mascotas:
            self._mascotas.append(paciente)

    def mostrar_informacion(self):
        print(f"  {self._nombre} (doc. {self._documento}, tel. {self._telefono})")
        if not self._mascotas:
            print("    Sin mascotas registradas.")
        for mascota in self._mascotas:
            print(f"    - {mascota}")


class Veterinario:
    """Profesional que atiende las citas. Solo atiende las especies para las que está habilitado."""

    def __init__(self, tarjeta_profesional, nombre, especialidad, especies_atendidas):
        self._tarjeta_profesional = validar_texto(tarjeta_profesional, "tarjeta profesional")
        self.nombre = nombre
        self.especialidad = especialidad
        self.especies_atendidas = especies_atendidas

    @property
    def tarjeta_profesional(self):
        return self._tarjeta_profesional

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor):
        self._especialidad = validar_texto(valor, "especialidad")

    @property
    def especies_atendidas(self):
        return tuple(self._especies_atendidas)

    @especies_atendidas.setter
    def especies_atendidas(self, valor):
        if not isinstance(valor, (list, tuple)) or not valor:
            raise ValueError("El veterinario debe atender al menos una especie.")
        self._especies_atendidas = [validar_texto(e, "especie").capitalize() for e in valor]

    def puede_atender(self, paciente):
        """Compara con la propiedad especie del paciente; no necesita saber su clase."""
        return paciente.especie in self._especies_atendidas

    def mostrar_informacion(self):
        especies = ", ".join(self._especies_atendidas)
        print(f"  Dr(a). {self._nombre} - {self._especialidad} (TP {self._tarjeta_profesional})")
        print(f"    Atiende: {especies}")
