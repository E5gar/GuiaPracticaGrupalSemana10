#!/usr/bin/env python3
"""Orquestador CLI del Sistema de Gestión de Productos - IS093A Semana 10"""

from models.producto import Producto, Electronico, Libro
from utils.validators import validar_numero, validar_categoria
from utils.exceptions import ValidationError, NotFoundError

def menu():
    print("\n=== GESTIÓN DE PRODUCTOS (CLI) ===")
    print("1. Agregar Producto")
    print("2. Listar Productos")
    print("3. Calcular Precio Final")
    print("4. Salir")
    return input("Opción > ").strip()

def main():
    inventario = {}  # {id: objeto_producto}
    contador_id = 1

    while True:
        try:
            opcion = menu()
            if opcion == "1":
                # TODO: Solicitar datos, validar con utils.validators
                # Crear instancia según categoría, asignar ID, guardar en inventario
                pass
            elif opcion == "2":
                # TODO: Iterar inventario, manejar caso vacío
                pass
            elif opcion == "3":
                # TODO: Buscar producto por ID, llamar calcular_precio_final()
                # Capturar NotFoundError y ValidationError
                pass
            elif opcion == "4":
                print("Cerrando sistema...")
                break
            else:
                raise ValidationError("Opción inválida")
        except ValidationError as e:
            print(f"⚠️ Error de validación: {e}")
        except NotFoundError as e:
            print(f"🔍 No encontrado: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        finally:
            # TODO: Log o cleanup opcional
            pass

if __name__ == "__main__":
    main()