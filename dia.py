import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time

# Función para limpiar el precio
def limpiar_precio(precio_texto):
    precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
    return float(precio_limpio)

# Función para extraer productos de una página
def extraer_productos_de_pagina(page_url, categoria, subcategoria):
    productos = []
    try:
        page_response = requests.get(page_url)
        if page_response.status_code != 200:
            print(f'❌ No se pudo acceder a la página {page_url}')
            return productos

        soup = BeautifulSoup(page_response.text, 'html.parser')
        productos_divs = soup.find_all('div', class_='diaio-search-result-0-x-galleryItem')

        for producto_div in productos_divs:
            try:
                nombre = producto_div.find(
                    'span',
                    class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body'
                ).text.strip().replace(',', '')

                precio_texto = producto_div.find(
                    'span',
                    class_='diaio-store-5-x-sellingPriceValue'
                ).text.strip()

                precio = limpiar_precio(precio_texto)

                productos.append({
                    'nombre': nombre,
                    'precio': precio,
                    'categoria': categoria,
                    'subcategoria': subcategoria
                })
            except Exception as e:
                print(f'⚠️ Error procesando producto: {e}')
    except Exception as e:
        print(f'❌ Error general en {page_url}: {e}')
    return productos

# Script principal
def main():
    inicio = time.time()
    estado = "✅ Finalizado sin errores"

    sitemap_url = "https://diaonline.supermercadosdia.com.ar/sitemap/category-1.xml"
    response = requests.get(sitemap_url)

    productos = []
    try:
        if response.status_code == 200:
            print("🗺️ Sitemap cargado con éxito")
            sitemap_soup = BeautifulSoup(response.text, 'xml')
            locs = sitemap_soup.find_all('loc')

            tareas = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                for loc in locs:
                    url_categoria = loc.text.strip()
                    path_parts = urlparse(url_categoria).path.strip('/').split('/')

                    if len(path_parts) >= 2:
                        categoria, subcategoria = path_parts[0], path_parts[1]
                        print(f"🔍 Procesando: {categoria} > {subcategoria}")

                        for page in range(1, 15):
                            page_url = f'https://diaonline.supermercadosdia.com.ar/{categoria}/{subcategoria}?page={page}'
                            tareas.append(executor.submit(
                                extraer_productos_de_pagina, page_url, categoria, subcategoria
                            ))

                for future in as_completed(tareas):
                    productos += future.result()
        else:
            print("❌ No se pudo cargar el sitemap")
            estado = "❌ Falló al cargar sitemap"

    except Exception as e:
        print(f"💥 Ocurrió un error inesperado: {e}")
        estado = f"❌ Error: {e}"

    # Guardar resultados si hubo productos
    if productos:
        df = pd.DataFrame(productos)
        df = df.drop_duplicates(subset=['nombre', 'categoria', 'subcategoria'])
        
        fecha_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        nombre_archivo = f'productos_dia {fecha_str}.csv'
        df.to_csv(nombre_archivo, index=False, encoding='utf-8')
        print("📦 Archivo CSV generado con éxito")

    # Crear informe de ejecución
    fin = time.time()
    duracion = round(fin - inicio, 2)
    fecha = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    df_log = pd.DataFrame([{
        'Fecha de Ejecución': fecha,
        'Duración (segundos)': duracion,
        'Estado': estado
    }])

    df_log.to_excel('informe_ejecucion.xlsx', index=False)
    print("📊 Informe de ejecución generado")

# Ejecutar
if __name__ == "__main__":
    main()