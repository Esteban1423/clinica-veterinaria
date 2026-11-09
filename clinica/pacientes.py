"""Pacientes de la clínica: clase abstracta Paciente y sus tres especializaciones."""

from abc import ABC, abstractmethod

from .historia_clinica import HistoriaClinica
from .validaciones import validar_booleano, validar_texto


class Paciente(ABC):
    """Concepto general de animal atendido en la clínica.

    Es abstracta porque la clínica nunca atiende a "un paciente" sin especie:
    el costo de la consulta y los cuidados dependen de qué animal es.
    """

    COSTO_BASE_CONSULTA = 60000

    def __init__(self, codigo, nombre, edad, peso, propietario):
        self._codigo = validar_texto(codigo, "código")
        self.nombre = nombre
        self.edad = edad
        self.peso = peso
        self._propietario = propietario
        # Composición: el paciente crea su propia historia clínica.
        self._historia = HistoriaClinica(self._codigo)
        # Asociación bidireccional: el propietario conoce a sus mascotas.
        propietario.agregar_mascota(self)

    # ----- Propiedades comunes -----
    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0 or valor > 40:
            raise ValueError("La edad debe ser un número entero entre 0 y 40 años.")
        self._edad = valor

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El peso debe ser un número mayor que 0 kg.")
        self._peso = float(valor)

    @property
    def propietario(self):
        return self._propietario

    @property
    def historia(self):
        """Solo lectura: la historia clínica no se reemplaza desde fuera."""
        return self._historia

    # ----- Métodos abstractos (cada especie los implementa) -----
    @property
    @abstractmethod
    def especie(self):
        """Nombre de la especie del paciente (Perro, Gato, Ave)."""

    @abstractmethod
    def calcular_costo_consulta(self):
        """Valor de una consulta general para este paciente."""

    @abstractmethod
    def describir_cuidados(self):
        """Recomendaciones de cuidado según la especie y los datos del paciente."""

    # ----- Métodos comunes -----
    def mostrar_informacion(self):
        print(f"  Código: {self._codigo} | Nombre: {self._nombre} | Especie: {self.especie}")
        anios = "año" if self._edad == 1 else "años"
        print(f"  Edad: {self._edad} {anios} | Peso: {self._peso:g} kg")
        print(f"  Propietario: {self._propietario.nombre} ({self._propietario.telefono})")

    def registrar_atencion(self, fecha, nombre_veterinario, diagnostico, tratamiento):
        """Delega en la historia clínica, que es parte del paciente."""
        self._historia.agregar_registro(fecha, nombre_veterinario, diagnostico, tratamiento)

    def __str__(self):
        return f"{self._nombre} ({self.especie}, {self._codigo})"


class Perro(Paciente):
    """Un perro ES UN paciente. Agrega raza, tamaño y vacuna antirrábica."""

    TAMANOS = ("pequeño", "mediano", "grande")
    RECARGO_POR_TAMANO = {"pequeño": 0, "mediano": 10000, "grande": 20000}
    MINUTOS_PASEO = {"pequeño": 30, "mediano": 60, "grande": 90}

    def __init__(self, codigo, nombre, edad, peso, propietario, raza, tamano, vacuna_antirrabica):
        super().__init__(codigo, nombre, edad, peso, propietario)
        self.raza = raza
        self.tamano = tamano
        self._vacuna_antirrabica = validar_booleano(vacuna_antirrabica, "vacuna antirrábica")

    @property
    def especie(self):
        return "Perro"

    @property
    def raza(self):
        return self._raza

    @raza.setter
    def raza(self, valor):
        self._raza = validar_texto(valor, "raza")

    @property
    def tamano(self):
        return self._tamano

    @tamano.setter
    def tamano(self, valor):
        texto = validar_texto(valor, "tamaño").lower()
        if texto not in self.TAMANOS:
            raise ValueError(f"Tamaño '{valor}' no válido. Opciones: {', '.join(self.TAMANOS)}.")
        self._tamano = texto

    @property
    def vacuna_antirrabica(self):
        return self._vacuna_antirrabica

    # ----- Métodos propios -----
    def minutos_paseo_recomendados(self):
        return self.MINUTOS_PASEO[self._tamano]

    def vacunar_antirrabica(self):
        """Aplica la vacuna antirrábica (si ya la tenía, solo lo informa)."""
        if self._vacuna_antirrabica:
            print(f"  {self._nombre} ya tenía la vacuna antirrábica al día.")
        else:
            self._vacuna_antirrabica = True
            print(f"  Vacuna antirrábica aplicada a {self._nombre}.")

    # ----- Métodos sobrescritos -----
    def calcular_costo_consulta(self):
        # Los perros grandes requieren más manejo y más dosis de medicamento.
        return self.COSTO_BASE_CONSULTA + self.RECARGO_POR_TAMANO[self._tamano]

    def describir_cuidados(self):
        texto = (f"Paseos de {self.minutos_paseo_recomendados()} min diarios "
                 f"(tamaño {self._tamano}) y cepillado semanal")
        if not self._vacuna_antirrabica:
            texto += ". PENDIENTE: vacuna antirrábica"
        return texto + "."

    def mostrar_informacion(self):
        print("[PERRO]")
        super().mostrar_informacion()
        vacuna = "al día" if self._vacuna_antirrabica else "pendiente"
        print(f"  Raza: {self._raza} | Tamaño: {self._tamano} | Antirrábica: {vacuna}")


class Gato(Paciente):
    """Un gato ES UN paciente. Agrega si vive en interior y si está esterilizado."""

    RECARGO_NO_ESTERILIZADO = 15000

    def __init__(self, codigo, nombre, edad, peso, propietario, es_de_interior, esterilizado):
        super().__init__(codigo, nombre, edad, peso, propietario)
        self._es_de_interior = validar_booleano(es_de_interior, "es de interior")
        self._esterilizado = validar_booleano(esterilizado, "esterilizado")

    @property
    def especie(self):
        return "Gato"

    @property
    def es_de_interior(self):
        return self._es_de_interior

    @property
    def esterilizado(self):
        return self._esterilizado

    # ----- Métodos propios -----
    def esterilizar(self):
        if self._esterilizado:
            print(f"  {self._nombre} ya estaba esterilizado(a).")
        else:
            self._esterilizado = True
            print(f"  {self._nombre} fue esterilizado(a).")

    def gramos_alimento_diario(self):
        """Ración aproximada de concentrado: 15 g por kg de peso."""
        return round(self._peso * 15)

    # ----- Métodos sobrescritos -----
    def calcular_costo_consulta(self):
        # Un gato no esterilizado incluye valoración reproductiva.
        costo = self.COSTO_BASE_CONSULTA
        if not self._esterilizado:
            costo += self.RECARGO_NO_ESTERILIZADO
        return costo

    def describir_cuidados(self):
        texto = f"{self.gramos_alimento_diario()} g de concentrado al día y arenero limpio a diario"
        if not self._es_de_interior:
            texto += "; sale al exterior: desparasitación mensual"
        return texto + "."

    def mostrar_informacion(self):
        print("[GATO]")
        super().mostrar_informacion()
        habitat = "interior" if self._es_de_interior else "exterior"
        esterilizado = "sí" if self._esterilizado else "no"
        print(f"  Hábitat: {habitat} | Esterilizado: {esterilizado}")


class Ave(Paciente):
    """Un ave ES UN paciente. Agrega la especie de ave y si puede volar."""

    FACTOR_EXOTICOS = 1.35

    def __init__(self, codigo, nombre, edad, peso, propietario, tipo_ave, puede_volar):
        super().__init__(codigo, nombre, edad, peso, propietario)
        self.tipo_ave = tipo_ave
        self._puede_volar = validar_booleano(puede_volar, "puede volar")

    @property
    def especie(self):
        return "Ave"

    @property
    def tipo_ave(self):
        return self._tipo_ave

    @tipo_ave.setter
    def tipo_ave(self, valor):
        self._tipo_ave = validar_texto(valor, "tipo de ave")

    @property
    def puede_volar(self):
        return self._puede_volar

    # ----- Método propio -----
    def recortar_alas(self):
        """Recorte de plumas de vuelo para evitar escapes o accidentes en casa."""
        if not self._puede_volar:
            print(f"  {self._nombre} ya tiene las alas recortadas.")
        else:
            self._puede_volar = False
            print(f"  Se recortaron las plumas de vuelo de {self._nombre}.")

    # ----- Métodos sobrescritos -----
    def calcular_costo_consulta(self):
        # Las aves son pacientes exóticos: requieren equipo y manejo especial.
        return round(self.COSTO_BASE_CONSULTA * self.FACTOR_EXOTICOS)

    def describir_cuidados(self):
        texto = f"Jaula amplia para {self._tipo_ave.lower()}, 1 h de sol indirecto y frutas frescas"
        if self._puede_volar:
            texto += "; vuela libremente: cerrar ventanas al sacarla de la jaula"
        return texto + "."

    def mostrar_informacion(self):
        print("[AVE]")
        super().mostrar_informacion()
        vuelo = "sí" if self._puede_volar else "no (alas recortadas)"
        print(f"  Tipo de ave: {self._tipo_ave} | Puede volar: {vuelo}")
