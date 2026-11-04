from .exceptions import ValidationError

def validar_numero(valor: str, tipo: type = float, min_val: float = 0, max_val: float = None) -> float:
    try:
        num = tipo(valor)
        if num < min_val or (max_val is not None and num > max_val):
            raise ValidationError(f"Valor fuera de rango: {min_val}-{max_val}")
        return num
    except ValueError:
        raise ValidationError(f"Formato numérico inválido: {valor}")

def validar_categoria(categoria: str) -> str:
    # TODO: Validar contra ["electronico", "libro"], normalizar, lanzar ValidationError
    pass