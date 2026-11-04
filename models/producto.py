from __future__ import annotations
from typing import override

class Producto:
    def __init__(self, nombre: str, precio_base: float, stock: int):
        # TODO: Encapsular atributos, validar rangos, asignar con @property
        self.nombre = nombre
        self.precio_base = precio_base
        self.stock = stock

    def calcular_precio_final(self) -> float:
        raise NotImplementedError("Subclases deben implementar este método")

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.nombre} | S/ {self.precio_base} | Stock: {self.stock}"

    def __del__(self):
        print(f"🗑️ Destruyendo instancia: {self.nombre}")

class Electronico(Producto):
    def __init__(self, nombre: str, precio_base: float, stock: int, garantia_meses: int):
        # TODO: Llamar super(), validar garantía, atributo protegido
        pass

    @override
    def calcular_precio_final(self) -> float:
        # TODO: Aplicar IGV (18%) + descuento si stock > 50
        pass

class Libro(Producto):
    def __init__(self, nombre: str, precio_base: float, stock: int, autor: str):
        # TODO: Llamar super(), validar autor, atributo privado __autor
        pass

    @override
    def calcular_precio_final(self) -> float:
        # TODO: Precio base - 10% si es libro de texto
        pass