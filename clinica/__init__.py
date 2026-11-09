"""Paquete del Sistema de Gestión de una Clínica Veterinaria."""

from .cita import Cita
from .clinica import ClinicaVeterinaria
from .excepciones import (CitaYaAtendidaError, ErrorClinicaVeterinaria,
                          EspecieNoAtendidaError, HorarioNoDisponibleError,
                          PacienteNoEncontradoError, VeterinarioNoEncontradoError)
from .historia_clinica import HistoriaClinica
from .pacientes import Ave, Gato, Paciente, Perro
from .personas import Propietario, Veterinario
from .validaciones import formato_pesos
