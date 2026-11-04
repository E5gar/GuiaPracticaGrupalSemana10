#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from colorama import init, Fore, Style
from models.producto import Producto, Electronico, Libro
from utils.validators import validar_sku, validar_categoria, validar_numero, validar_texto
from utils.exceptions import ValidationError, NotFoundError, MarketplaceError

init(autoreset=True)


def seed_catalogo() -> dict[str, Producto]:
    items: list[Producto] = [
        Electronico(
            sku="ELEC-101",
            nombre="Calculadora Programable Texas Instruments TI-Nspire CX II CAS",
            precio_base=940.0,
            stock=18,
            garantia_meses=24,
            garantia_estudiantil=True,
            imagen_url="https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?w=800"
        ),
        Electronico(
            sku="ELEC-102",
            nombre="Tableta Digitalizadora Wacom Intuos Pro Paper Edition Lab",
            precio_base=1450.0,
            stock=35,
            garantia_meses=12,
            garantia_estudiantil=True,
            imagen_url="https://images.unsplash.com/photo-1563770660941-20978e870e26?w=800"
        ),
        Electronico(
            sku="ELEC-103",
            nombre="Kit de Laboratorio FPGA Altera Cyclone IV + Osciloscopio Digital",
            precio_base=2150.0,
            stock=4,
            garantia_meses=36,
            garantia_estudiantil=False,
            imagen_url="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800"
        ),
        Libro(
            sku="LIB-201",
            nombre="Sistemas de Control para Ingeniería 8va Edición (Nise)",
            precio_base=180.0,
            stock=45,
            autor="Norman S. Nise",
            tipo_libro="universitario",
            imagen_url="https://images.unsplash.com/photo-1532012164546-f432f2e3edd4?w=800"
        ),
        Libro(
            sku="LIB-202",
            nombre="Manual de Prácticas de Redes Neuronales y Microcontroladores",
            precio_base=85.0,
            stock=120,
            autor="Facultad de Ingeniería de Sistemas UNCP",
            tipo_libro="universitario",
            imagen_url="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"
        ),
        Libro(
            sku="LIB-203",
            nombre="Clean Code: A Handbook of Agile Software Craftsmanship",
            precio_base=140.0,
            stock=15,
            autor="Robert C. Martin",
            tipo_libro="literatura",
            imagen_url="https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800"
        ),
    ]
    return {p.sku: p for p in items}


def exportar_web_data(inventario: dict[str, Producto]):
    data = [p.to_dict() for p in inventario.values()]
    web_dir = Path("web")
    web_dir.mkdir(exist_ok=True)
    with open(web_dir / "productos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def menu() -> str:
    print("\n" + "=" * 58)
    print("  HUANCA ACADEMIC MARKETPLACE | IS093A SEMANA 10")
    print("=" * 58)
    print("  [1] Registrar nuevo material educativo")
    print("  [2] Listar catálogo polimórfico (CLI)")
    print("  [3] Calcular precio final y beneficio semestral por SKU")
    print("  [4] Simular despacho y reducción de stock")
    print("  [5] Sincronizar catálogo con frontend web")
    print("  [6] Salir del sistema")
    print("-" * 58)
    return input("Seleccione opción [1-6] > ").strip()


def registrar_producto(inventario: dict[str, Producto]):
    print("\n--- REGISTRO DE PRODUCTO ---")
    cat = validar_categoria(input("Tipo de material (electronico/libro) > "))
    sku = validar_sku(input("Código SKU (Ej: ELEC-500, LIB-300) > "))
    
    if sku in inventario:
        raise ValidationError(f"El SKU '{sku}' ya se encuentra registrado", campo="SKU")

    nombre = validar_texto(input("Título / Descripción > "), campo="nombre", min_len=3)
    precio = float(validar_numero(input("Precio base en soles (S/) > "), tipo=float, min_val=1.0, campo="precio_base"))
    stock = int(validar_numero(input("Cantidad en stock > "), tipo=int, min_val=0, campo="stock"))
    img = input("URL de imagen (opcional, Enter para omitir) > ").strip()

    if cat == "electronico":
        garantia = int(validar_numero(input("Meses de garantía (0 a 60) > "), tipo=int, min_val=0, max_val=60, campo="garantia_meses"))
        estudiantil_resp = input("¿Aplica beneficio estudiantil de ciclo? (s/n) > ").strip().lower()
        es_estudiantil = estudiantil_resp == "s"
        prod = Electronico(sku, nombre, precio, stock, garantia, es_estudiantil, img)
    else:
        autor = validar_texto(input("Nombre del autor o entidad académica > "), campo="autor", min_len=3)
        tipo_lib = input("Tipo de obra (universitario/literatura) [universitario] > ").strip() or "universitario"
        prod = Libro(sku, nombre, precio, stock, autor, tipo_lib, img)

    inventario[sku] = prod
    exportar_web_data(inventario)
    print(f"\n{Fore.GREEN}[OK]{Style.RESET_ALL} Producto {sku} creado con éxito.")


def listar_productos(inventario: dict[str, Producto]):
    print("\n" + "=" * 80)
    print("  CATÁLOGO GENERAL - MARKETPLACE DIDÁCTICO E INSTRUMENTAL")
    print("=" * 80)
    if not inventario:
        print("  El catálogo está vacío actualmente.")
        return

    for p in inventario.values():
        print(f" • {p}")
    print("=" * 80)
    print(f"Total ítems activos: {len(inventario)}")


def calcular_precio_producto(inventario: dict[str, Producto]):
    print("\n--- CONSULTA DE PRECIO FINAL & DESCUENTOS ---")
    sku_in = input("Ingrese el SKU a liquidar > ").strip().upper()
    
    if sku_in not in inventario:
        raise NotFoundError(entidad="Material Didáctico", identificador=sku_in)
    
    item = inventario[sku_in]
    precio_final = item.calcular_precio_final()
    
    print("\n" + "-" * 50)
    print(f"  Detalle de Liquidación: {item.nombre}")
    print(f"  Tipo de Objeto: {item.__class__.__name__}")
    print(f"  Precio Base: S/ {item.precio_base:.2f}")
    print(f"  Stock Actual: {item.stock} unidades")
    print(f"  PRECIO FINAL CALCULADO: S/ {precio_final:.2f}")
    if isinstance(item, Electronico):
        print(f"  Costo de Envío Protegido: S/ {item.calcular_costo_envio():.2f}")
        print(f"  Beneficio Estudiantil: {'Habilitado' if item.garantia_estudiantil else 'No habilitado'}")
    elif isinstance(item, Libro):
        print(f"  Categoría: {item.tipo_libro.capitalize()}")
        print(f"  Autor: {item.autor}")
    print("-" * 50)


def despachar_producto(inventario: dict[str, Producto]):
    print("\n--- DESPACHO DE MATERIAL EDUCATIVO ---")
    sku_in = input("Ingrese SKU a despachar > ").strip().upper()
    if sku_in not in inventario:
        raise NotFoundError(entidad="Material Didáctico", identificador=sku_in)

    item = inventario[sku_in]
    cant = int(validar_numero(input(f"Cantidad a retirar (disponible {item.stock}) > "), tipo=int, min_val=1, campo="cantidad"))
    item.reducir_stock(cant)
    exportar_web_data(inventario)
    print(f"\n{Fore.GREEN}[OK]{Style.RESET_ALL} Despacho completado. Nuevo stock de {item.sku}: {item.stock} unidades.")


def main():
    inventario = seed_catalogo()
    exportar_web_data(inventario)

    while True:
        try:
            opcion = menu()
            if opcion == "1":
                registrar_producto(inventario)
            elif opcion == "2":
                listar_productos(inventario)
            elif opcion == "3":
                calcular_precio_producto(inventario)
            elif opcion == "4":
                despachar_producto(inventario)
            elif opcion == "5":
                exportar_web_data(inventario)
                print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} Catálogo web sincronizado en 'web/productos.json'.")
            elif opcion == "6":
                print("\nFinalizando sesión en Huanca Academic Marketplace. ¡Éxito académico!\n")
                break
            else:
                raise ValidationError("Opción numérica no reconocida en el menú", campo="opción")
        except ValidationError as err:
            print(f"\n{Fore.YELLOW}[ADVERTENCIA]{Style.RESET_ALL} {err}")
        except NotFoundError as err:
            print(f"\n{Fore.CYAN}[NO ENCONTRADO]{Style.RESET_ALL} {err}")
        except MarketplaceError as err:
            print(f"\n{Fore.RED}[ERROR DOMINIO]{Style.RESET_ALL} {err}")
        except Exception as err:
            print(f"\n{Fore.RED}[ERROR CRITICO]{Style.RESET_ALL} {type(err).__name__} - {err}")
        else:
            pass
        finally:
            pass


if __name__ == "__main__":
    main()
