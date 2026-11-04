from __future__ import annotations
from typing import override
from utils.validators import validar_sku, validar_texto, validar_numero, validar_tipo_libro
from utils.exceptions import ValidationError
from .descuento import DescuentoMixin


class Producto:
    def __init__(self, sku: str, nombre: str, precio_base: float, stock: int, imagen_url: str = ""):
        self.sku = sku
        self.nombre = nombre
        self.precio_base = precio_base
        self.stock = stock
        self.imagen_url = imagen_url

    @property
    def sku(self) -> str:
        return self._sku

    @sku.setter
    def sku(self, valor: str):
        self._sku = validar_sku(valor)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = validar_texto(valor, campo="nombre", min_len=3, max_len=100)

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float):
        self._precio_base = float(validar_numero(valor, tipo=float, min_val=0.5, max_val=25000.0, campo="precio_base"))

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        self._stock = int(validar_numero(valor, tipo=int, min_val=0, max_val=10000, campo="stock"))

    @property
    def imagen_url(self) -> str:
        return self._imagen_url

    @imagen_url.setter
    def imagen_url(self, valor: str):
        self._imagen_url = valor.strip() if valor else "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800"

    def reducir_stock(self, cantidad: int = 1):
        if cantidad > self._stock:
            raise ValidationError(f"Stock insuficiente ({self._stock} disponible) para despachar {cantidad} unidades", campo="stock")
        self._stock -= cantidad

    def calcular_precio_final(self) -> float:
        raise NotImplementedError("Las clases derivadas deben implementar calcular_precio_final()")

    def to_dict(self) -> dict:
        return {
            "sku": self.sku,
            "nombre": self.nombre,
            "tipo": self.__class__.__name__,
            "precio_base": self.precio_base,
            "stock": self.stock,
            "imagen_url": self.imagen_url,
            "precio_final": self.calcular_precio_final()
        }

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self._sku} - {self._nombre} | Base: S/ {self._precio_base:.2f} | Stock: {self._stock}"

    def __del__(self):
        pass


class Electronico(Producto, DescuentoMixin):
    def __init__(self, sku: str, nombre: str, precio_base: float, stock: int, garantia_meses: int, garantia_estudiantil: bool = True, imagen_url: str = ""):
        super().__init__(sku, nombre, precio_base, stock, imagen_url)
        self.garantia_meses = garantia_meses
        self._garantia_estudiantil = bool(garantia_estudiantil)

    @property
    def garantia_meses(self) -> int:
        return self._garantia_meses

    @garantia_meses.setter
    def garantia_meses(self, valor: int):
        self._garantia_meses = int(validar_numero(valor, tipo=int, min_val=0, max_val=60, campo="garantia_meses"))

    @property
    def garantia_estudiantil(self) -> bool:
        return self._garantia_estudiantil

    def calcular_costo_envio(self) -> float:
        if self._stock <= 5:
            return 25.0
        return 12.0

    @override
    def calcular_precio_final(self) -> float:
        igv = self.precio_base * 0.18
        costo_base_con_impuesto = self.precio_base + igv
        costo_envio = self.calcular_costo_envio()
        
        precio_acumulado = costo_base_con_impuesto + costo_envio
        
        if self._garantia_estudiantil:
            precio_acumulado = self.aplicar_descuento_semestre(precio_acumulado, porcentaje=10.0)
            
        if self._stock > 30:
            precio_acumulado -= (self.precio_base * 0.05)
            
        return round(precio_acumulado, 2)

    @override
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "garantia_meses": self.garantia_meses,
            "garantia_estudiantil": self._garantia_estudiantil,
            "costo_envio": self.calcular_costo_envio()
        })
        return data

    @override
    def __str__(self) -> str:
        base_str = super().__str__()
        promo = "Garantía Académica Activa" if self._garantia_estudiantil else "Garantía Regular"
        return f"{base_str} | {self._garantia_meses} meses ({promo}) | Final: S/ {self.calcular_precio_final():.2f}"


class Libro(Producto, DescuentoMixin):
    def __init__(self, sku: str, nombre: str, precio_base: float, stock: int, autor: str, tipo_libro: str = "universitario", imagen_url: str = ""):
        super().__init__(sku, nombre, precio_base, stock, imagen_url)
        self.autor = autor
        self.__tipo_libro = validar_tipo_libro(tipo_libro)

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str):
        self._autor = validar_texto(valor, campo="autor", min_len=3, max_len=80)

    @property
    def tipo_libro(self) -> str:
        return self.__tipo_libro

    @tipo_libro.setter
    def tipo_libro(self, valor: str):
        self.__tipo_libro = validar_tipo_libro(valor)

    @override
    def calcular_precio_final(self) -> float:
        subtotal = self.precio_base
        if self.__tipo_libro == "universitario":
            subtotal = subtotal * 0.90
            subtotal = self.aplicar_descuento_semestre(subtotal, porcentaje=12.0)
        else:
            subtotal = self.aplicar_descuento_semestre(subtotal, porcentaje=5.0)
        return round(subtotal, 2)

    @override
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "autor": self.autor,
            "tipo_libro": self.__tipo_libro
        })
        return data

    @override
    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} | Autor: {self._autor} | Cat: {self.__tipo_libro.capitalize()} | Final: S/ {self.calcular_precio_final():.2f}"