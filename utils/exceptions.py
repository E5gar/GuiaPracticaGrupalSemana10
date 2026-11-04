class MarketplaceError(Exception):
    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERAL"):
        super().__init__(mensaje)
        self.codigo_error = codigo_error
        self.mensaje = mensaje

    def __str__(self) -> str:
        return f"[{self.codigo_error}] {self.mensaje}"


class ValidationError(MarketplaceError):
    def __init__(self, mensaje: str, campo: str = "desconocido"):
        super().__init__(mensaje, codigo_error="ERR_VALIDACION")
        self.campo = campo

    def __str__(self) -> str:
        return f"[{self.codigo_error}] Campo '{self.campo}': {self.mensaje}"


class NotFoundError(MarketplaceError):
    def __init__(self, entidad: str, identificador: str | int):
        mensaje = f"No se encontró {entidad} con identificador '{identificador}'"
        super().__init__(mensaje, codigo_error="ERR_NO_ENCONTRADO")
        self.entidad = entidad
        self.identificador = identificador