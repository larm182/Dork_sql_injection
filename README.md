# Dork_sql_injection

Herramienta de Detección de Vulnerabilidades SQL Injection
Python
Tkinter
Bootstrap
Scraping

Una herramienta desarrollada en Python para detectar vulnerabilidades de SQL Injection en sitios web. La herramienta utiliza técnicas de scraping para buscar sitios en Bing, verifica automáticamente si son vulnerables y permite exportar los resultados a un archivo CSV.

Características Principales
Búsqueda personalizada: Utiliza operadores avanzados de Bing (como site: o inurl:) para encontrar sitios específicos.

Detección automática: Verifica si los sitios son vulnerables a SQL Injection mediante pruebas de inyección.

Interfaz gráfica moderna: Diseño estilo Bootstrap gracias a la biblioteca ttkbootstrap.

Exportación de resultados: Guarda los resultados en un archivo CSV para su posterior análisis.

Barra de progreso: Muestra el progreso de la verificación en tiempo real.

Requisitos
Python 3.x

Bibliotecas necesarias:

pip install requests beautifulsoup4 ttkbootstrap

Instrucciones de Uso
Clona el repositorio:
git clone https://github.com/larm182/Dork_sql_injectio.git
cd tu-repositorio

Ejecuta la herramienta:
python Dork_sql_injection.py
Ingresa un dork (por ejemplo, site:.com index.php?id=) y la cantidad de sitios que deseas verificar.

Haz clic en Iniciar búsqueda para comenzar la detección.

Los resultados se mostrarán en una tabla. Puedes copiar la URL o el estado de un resultado haciendo clic derecho.

Exporta los resultados a un archivo CSV haciendo clic en Exportar resultados.

Estructura del Proyecto

Dork_sql_injection/
├── Dork_sql_injectio.py  # Código principal de la herramienta
├── README.md                # Este archivo


Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la herramienta o encuentras algún problema, no dudes en abrir un issue o enviar un pull request.

