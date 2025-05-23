
# 🛒 Supermarket Price Tracker - DIA Argentina

Este proyecto nace de una necesidad personal y curiosidad técnica: ¿cómo cambian los precios en los supermercados con el tiempo?  
Como muchos, noté que cada vez que iba a hacer las compras, algunos productos estaban un poco más caros... o a veces, en oferta.  
Entonces me pregunté: ¿y si pudiera hacer un seguimiento automático de los precios, como si tuviera una "foto diaria" del supermercado?

Así nació este script de scraping para el sitio de [Supermercados DIA Argentina](https://diaonline.supermercadosdia.com.ar/).

---

## 📌 ¿Qué hace este proyecto?

Este script en Python recorre automáticamente el sitemap del sitio web de DIA y extrae precios de productos por categoría y subcategoría.  
Con cada ejecución, guarda la información en un archivo CSV con la fecha y hora, y también genera un informe de ejecución en Excel.

En resumen, podés:

- Obtener precios actualizados por producto, categoría y subcategoría.
- Crear un historial de precios para analizar aumentos, ofertas o variaciones.
- Visualizar luego esta info en un dashboard (por ejemplo, en Power BI o con Flask).

---

## ⚙️ Tecnologías y librerías utilizadas

- **Python 3.11+**
- `requests` – para hacer solicitudes HTTP
- `BeautifulSoup` (bs4) – para parsear el HTML y XML
- `pandas` – para manipular los datos y generar los archivos
- `concurrent.futures` – para hacer scraping en paralelo y ganar velocidad
- `datetime` y `time` – para manejar fechas y medir el tiempo de ejecución

---

## ▶️ ¿Cómo ejecutar el script?

1. Cloná este repositorio o descargá el archivo `dia.py`.
2. Asegurate de tener Python instalado.
3. Instalá las dependencias (si no las tenés):

   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ```

4. Ejecutá el script desde consola:

   ```bash
   python dia.py
   ```

5. Se generará un archivo CSV con los productos y un informe de ejecución llamado `informe_ejecucion.xlsx`.

---

## 📁 Estructura de archivos generados

- `productos_dia YYYY-MM-DD_HH-MM-SS.csv` → Datos crudos de los productos y precios.
- `informe_ejecucion.xlsx` → Registro con fecha, duración y estado de la ejecución.

---

## 📊 Próximos pasos

- Crear un dashboard web con Flask para visualizar los precios.
- Automatizar la ejecución diaria con una tarea programada (Task Scheduler o cron).
- Implementar un bot de WhatsApp para notificar sobre aumentos u ofertas.
- Almacenar esta información en un origen relacional on promise o cloud.

---

## ❤️ Autor

Hecho con dedicación por Nicolas Pastorini.  
Este proyecto es tanto una herramienta útil como un ejercicio de aprendizaje para practicar scraping, procesamiento de datos y automatización.

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT.  
Podés usarlo, modificarlo y compartirlo libremente. Solo seamos respetuosos con el uso del sitio web fuente.
