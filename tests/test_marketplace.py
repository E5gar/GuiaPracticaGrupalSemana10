import unittest
from models.producto import Producto, Electronico, Libro
from models.descuento import DescuentoMixin
from utils.exceptions import ValidationError, NotFoundError


class TestMarketplacePOO(unittest.TestCase):

    def test_creacion_electronico_ruta_feliz(self):
        item = Electronico(
            sku="ELEC-880",
            nombre="Osciloscopio Digital de Laboratorio",
            precio_base=1200.0,
            stock=10,
            garantia_meses=24,
            garantia_estudiantil=True
        )
        self.assertEqual(item.sku, "ELEC-880")
        self.assertEqual(item.precio_base, 1200.0)
        self.assertEqual(item.stock, 10)
        self.assertEqual(item.garantia_meses, 24)
        self.assertTrue(item.garantia_estudiantil)

    def test_polimorfismo_precio_final_electronico(self):
        item = Electronico(
            sku="ELEC-881",
            nombre="Calculadora Programable Avanzada",
            precio_base=100.0,
            stock=10,
            garantia_meses=12,
            garantia_estudiantil=True
        )
        precio_esperado = round((118.0 + 12.0) * 0.90, 2)
        self.assertEqual(item.calcular_precio_final(), precio_esperado)

    def test_polimorfismo_precio_final_libro_universitario(self):
        libro = Libro(
            sku="LIB-301",
            nombre="Compiladores: Principios, Técnicas y Herramientas",
            precio_base=200.0,
            stock=20,
            autor="Aho, Lam, Sethi, Ullman",
            tipo_libro="universitario"
        )
        precio_esperado = round((200.0 * 0.90) * 0.88, 2)
        self.assertEqual(libro.calcular_precio_final(), precio_esperado)

    def test_polimorfismo_precio_final_libro_literatura(self):
        libro = Libro(
            sku="LIB-302",
            nombre="Ensayo sobre la Ceguera",
            precio_base=100.0,
            stock=15,
            autor="José Saramago",
            tipo_libro="literatura"
        )
        precio_esperado = round(100.0 * 0.95, 2)
        self.assertEqual(libro.calcular_precio_final(), precio_esperado)

    def test_validacion_sku_formato_erroneo(self):
        with self.assertRaises(ValidationError) as ctx:
            Electronico(
                sku="invalido123",
                nombre="Gadget",
                precio_base=50.0,
                stock=5,
                garantia_meses=12
            )
        self.assertEqual(ctx.exception.campo, "SKU")

    def test_validacion_precio_negativo(self):
        with self.assertRaises(ValidationError) as ctx:
            Libro(
                sku="LIB-303",
                nombre="Física Universitaria",
                precio_base=-15.0,
                stock=5,
                autor="Sears Zemansky"
            )
        self.assertEqual(ctx.exception.campo, "precio_base")

    def test_validacion_stock_negativo(self):
        with self.assertRaises(ValidationError) as ctx:
            Electronico(
                sku="ELEC-882",
                nombre="Tablet",
                precio_base=500.0,
                stock=-2,
                garantia_meses=12
            )
        self.assertEqual(ctx.exception.campo, "stock")

    def test_validacion_garantia_excesiva(self):
        with self.assertRaises(ValidationError) as ctx:
            Electronico(
                sku="ELEC-883",
                nombre="Tablet Pro",
                precio_base=500.0,
                stock=10,
                garantia_meses=99
            )
        self.assertEqual(ctx.exception.campo, "garantia_meses")

    def test_despacho_stock_insuficiente(self):
        item = Libro(
            sku="LIB-304",
            nombre="Manual de Laboratorio",
            precio_base=40.0,
            stock=3,
            autor="UNCP"
        )
        with self.assertRaises(ValidationError):
            item.reducir_stock(5)

    def test_mro_jerarquia_c3(self):
        mro_electronico = [cls.__name__ for cls in Electronico.__mro__]
        self.assertEqual(mro_electronico, ["Electronico", "Producto", "DescuentoMixin", "object"])

        mro_libro = [cls.__name__ for cls in Libro.__mro__]
        self.assertEqual(mro_libro, ["Libro", "Producto", "DescuentoMixin", "object"])

    def test_excepcion_clase_base_directa(self):
        prod = Producto(sku="BASE-001", nombre="Producto Abstracto", precio_base=10.0, stock=1)
        with self.assertRaises(NotImplementedError):
            prod.calcular_precio_final()

    def test_mixin_heredado_por_derivadas(self):
        self.assertTrue(issubclass(Electronico, DescuentoMixin))
        self.assertTrue(issubclass(Libro, DescuentoMixin))
        self.assertEqual(DescuentoMixin().aplicar_descuento_semestre(100.0, 150.0), 100.0)

    def test_not_found_error_mensaje(self):
        with self.assertRaises(NotFoundError) as ctx:
            raise NotFoundError(entidad="Material Didáctico", identificador="ELEC-999")
        self.assertEqual(ctx.exception.codigo_error, "ERR_NO_ENCONTRADO")
        self.assertIn("ELEC-999", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
