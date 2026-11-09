"""Funciones de validación reutilizadas por los setters de las clases."""

from datetime import datetime


def validar_texto(valor, campo):
    """Devuelve el texto sin espacios sobrantes. Lanza ValueError si está vacío."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return valor.strip()


def validar_booleano(valor, campo):
    """Comprueba que el valor sea True o False."""
    if not isinstance(valor, bool):
        raise ValueError(f"El campo '{campo}' debe ser True o False.")
    return valor


def validar_fecha(valor):
    """Comprueba que la fecha tenga el formato AAAA-MM-DD y sea una fecha real."""
    texto = validar_texto(valor, "fecha")
    try:
        datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"La fecha '{texto}' no es válida. Use el formato AAAA-MM-DD.") from None
    return texto


def validar_hora(valor):
    """Comprueba que la hora tenga el formato HH:MM (24 horas)."""
    texto = validar_texto(valor, "hora")
    try:
        datetime.strptime(texto, "%H:%M")
    except ValueError:
        raise ValueError(f"La hora '{texto}' no es válida. Use el formato HH:MM.") from None
    return texto


def formato_pesos(valor):
    """Da formato de pesos colombianos: 65000 -> $65.000"""
    return "$" + f"{valor:,.0f}".replace(",", ".")
