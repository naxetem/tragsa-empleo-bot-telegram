
# Bot telegram de ofertas de empleo Tragsa

## Descripción

1. **Descarga ofertas de empleo desde URLs.**
2. **Guarda las ofertas en archivos CSV.**
3. **Compara ofertas nuevas con las anteriores.**
4. **Notifica cambios vía Telegram.**

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea y activa un entorno virtual (opcional):
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configura `config.py` con las URLs y credenciales de Telegram:
    ```python
    base_path = ""
    out = base_path + "out/"
    urls = [
        ("https://www.tragsa.es/es/equipo-humano/unete-a-nuestro-equipo/ofertas-empleo-temporal/Paginas/ofertas-especificas-it.aspx", "tragsa_it"),
        ("https://www.tragsa.es/es/equipo-humano/unete-a-nuestro-equipo/ofertas-empleo-temporal/Paginas/ofertas-especificas.aspx", "tragsa_especificas")
    ]

    # telegram
    token = "TU_TOKEN_DE_TELEGRAM"
    chat_id = "TU_CHAT_ID_DE_TELEGRAM" # se puede obtener buscando un bot chat_id en la app de telegram
    ```

## Uso

Ejecuta el script principal:
```sh
python tragsa.py
```

## Ejecución Automática

Es recomendable configurar cron para ejecutar este script regularmente. Para hacerlo, edita tu crontab con `crontab -e` y agrega una línea como esta para ejecutar el script cada día a las 8 AM:
```sh
0 8 * * * /ruta/a/tu/entorno/venv/bin/python /ruta/a/tu/repositorio/tragsa.py
```

## Estructura del Código

- `nuevo(url, file_name)`: Obtiene ofertas desde una URL y guarda en un CSV.
- `anterior(file_name)`: Carga ofertas previas desde un CSV.
- `main()`: Compara ofertas nuevas con las anteriores y notifica cambios.
- `enviar_mensaje_telegram(mensaje)`: Envía un mensaje vía Telegram.



