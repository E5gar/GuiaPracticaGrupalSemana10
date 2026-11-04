class DescuentoMixin:
    def aplicar_descuento_semestre(self, precio: float, porcentaje: float = 15.0) -> float:
        if porcentaje < 0 or porcentaje > 100:
            return precio
        monto_descuento = precio * (porcentaje / 100.0)
        return max(0.0, precio - monto_descuento)

    def obtener_beneficio_estudiantil(self) -> str:
        return "Bono de Ciclo Académico: Envío de instrumental asegurado y garantía extendida de laboratorio."