# Diagrama UML de clases

GitHub muestra este diagrama como imagen. También está exportado en [`diagrama_uml.png`](diagrama_uml.png).

```mermaid
classDiagram
    direction TB

    class Paciente {
        <<abstract>>
        -_codigo : str
        -_nombre : str
        -_edad : int
        -_peso : float
        -_propietario : Propietario
        -_historia : HistoriaClinica
        +COSTO_BASE_CONSULTA : int
        +especie()* str
        +calcular_costo_consulta()* int
        +describir_cuidados()* str
        +mostrar_informacion()
        +registrar_atencion(fecha, veterinario, diagnostico, tratamiento)
    }

    class Perro {
        -_raza : str
        -_tamano : str
        -_vacuna_antirrabica : bool
        +especie() str
        +calcular_costo_consulta() int
        +describir_cuidados() str
        +mostrar_informacion()
        +minutos_paseo_recomendados() int
        +vacunar_antirrabica()
    }

    class Gato {
        -_es_de_interior : bool
        -_esterilizado : bool
        +especie() str
        +calcular_costo_consulta() int
        +describir_cuidados() str
        +mostrar_informacion()
        +esterilizar()
        +gramos_alimento_diario() int
    }

    class Ave {
        -_tipo_ave : str
        -_puede_volar : bool
        +especie() str
        +calcular_costo_consulta() int
        +describir_cuidados() str
        +mostrar_informacion()
        +recortar_alas()
    }

    class HistoriaClinica {
        -_codigo_paciente : str
        -_fecha_apertura : str
        -_registros : list
        +agregar_registro(fecha, veterinario, diagnostico, tratamiento)
        +ultimo_registro() dict
        +mostrar()
    }

    class Propietario {
        -_documento : str
        -_nombre : str
        -_telefono : str
        -_mascotas : list~Paciente~
        +agregar_mascota(paciente)
        +mostrar_informacion()
    }

    class Veterinario {
        -_tarjeta_profesional : str
        -_nombre : str
        -_especialidad : str
        -_especies_atendidas : list~str~
        +puede_atender(paciente) bool
        +mostrar_informacion()
    }

    class Cita {
        -_numero : int
        -_paciente : Paciente
        -_veterinario : Veterinario
        -_fecha : str
        -_hora : str
        -_motivo : str
        -_estado : str
        -_valor_cobrado : int
        +ocupa(veterinario, fecha, hora) bool
        +atender(diagnostico, tratamiento) int
        +cancelar()
        +mostrar_informacion()
    }

    class ClinicaVeterinaria {
        -_nombre : str
        -_direccion : str
        -_pacientes : dict
        -_veterinarios : dict
        -_citas : list~Cita~
        +registrar_paciente(paciente)
        +registrar_veterinario(veterinario)
        +buscar_paciente(codigo) Paciente
        +buscar_veterinario(tarjeta) Veterinario
        +agendar_cita(codigo, tarjeta, fecha, hora, motivo) Cita
        +atender_cita(numero, diagnostico, tratamiento) int
        +total_facturado() int
        +mostrar_agenda()
    }

    Paciente <|-- Perro
    Paciente <|-- Gato
    Paciente <|-- Ave
    Paciente *-- "1" HistoriaClinica : composición
    Propietario "1" -- "1..*" Paciente : es dueño de
    Cita "*" --> "1" Paciente
    Cita "*" --> "1" Veterinario
    ClinicaVeterinaria o-- "*" Paciente
    ClinicaVeterinaria o-- "*" Veterinario
    ClinicaVeterinaria "1" --> "*" Cita : agenda
```

## Jerarquía de excepciones

```mermaid
classDiagram
    Exception <|-- ErrorClinicaVeterinaria
    ErrorClinicaVeterinaria <|-- HorarioNoDisponibleError
    ErrorClinicaVeterinaria <|-- EspecieNoAtendidaError
    ErrorClinicaVeterinaria <|-- PacienteNoEncontradoError
    ErrorClinicaVeterinaria <|-- VeterinarioNoEncontradoError
    ErrorClinicaVeterinaria <|-- CitaYaAtendidaError
```

Notación: `*` después de un método indica método abstracto; `◆` (`*--`) es composición, `◇` (`o--`) agregación y `-->` asociación.
