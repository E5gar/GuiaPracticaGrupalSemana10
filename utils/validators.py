import re
from .exceptions import ValidationError


def validar_numero(valor: str | float | int, tipo: type = float, min_val: float = 0, max_val: float | None = None, campo: str = "número") -> float | int:
    try:
        num = tipo(valor)
    except (ValueError, TypeError):
        raise ValidationError(f"El valor '{valor}' debe ser de tipo numérico ({tipo.__name__})", campo=campo)

    if num < min_val:
        raise ValidationError(f"El valor {num} no puede ser menor a {min_val}", campo=campo)
    if max_val is not None and num > max_val:
        raise ValidationError(f"El valor {num} no puede superar el límite de {max_val}", campo=campo)
    return num


def validar_texto(valor: str, campo: str, min_len: int = 2, max_len: int = 120) -> str:
    if not isinstance(valor, str):
        raise ValidationError("El valor proporcionado debe ser una cadena de texto", campo=campo)
    texto = valor.strip()
    if len(texto) < min_len:
        raise ValidationError(f"Debe contener al menos {min_len} caracteres", campo=campo)
    if len(texto) > max_len:
        raise ValidationError(f"No puede exceder los {max_len} caracteres", campo=campo)
    return texto


def validar_sku(sku: str) -> str:
    sku_limpio = validar_texto(sku, campo="SKU", min_len=4, max_len=15).upper()
    patron = r"^[A-Z]{2,4}-\d{3,6}$"
    if not re.match(patron, sku_limpio):
        raise ValidationError(f"Formato inválido. Debe seguir el patrón 'PRE-1234' (Ej: ELEC-101, LIB-204)", campo="SKU")
    return sku_limpio


def validar_categoria(categoria: str) -> str:
    cat_normalizada = validar_texto(categoria, campo="categoría").lower()
    categorias_validas = {"electronico", "libro"}
    if cat_normalizada not in categorias_validas:
        raise ValidationError(f"Categoría '{cat_normalizada}' no admitida. Opciones: {list(categorias_validas)}", campo="categoría")
    return cat_normalizada


def validar_tipo_libro(tipo: str) -> str:
    tipo_normalizado = validar_texto(tipo, campo="tipo_libro").lower()
    tipos_validos = {"universitario", "literatura"}
    if tipo_normalizado not in tipos_validos:
        raise ValidationError(f"Tipo de libro inválido. Debe ser 'universitario' o 'literatura'", campo="tipo_libro")
    return tipo_normalizado