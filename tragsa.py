#segunda version con try exxcept y logging para errores.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import telegram
import asyncio
import logging
from config import config

# Crear directorio de salida si no existe
if not os.path.exists(config.out):
    os.makedirs(config.out)

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def nuevo(url, file_name):
    try:
        logger.info(f"Obteniendo ofertas desde {url}")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')[1:]  # Ignorar el encabezado
        ofertas = [
            {
                'Oferta': columns[0].text.strip(),
                'Código': int(columns[1].text.strip()),
                'Empresa': columns[2].text.strip(),
                'Nº de puestos': int(columns[3].text.strip()),
                'Tipo': columns[4].text.strip(),
                'Fecha límite': columns[5].text.strip(),
                'Link': columns[0].find('a')['href'] if columns[0].find('a') else url  # Recuperar el enlace del campo Oferta

            }
            for columns in (row.find_all('td') for row in rows) if columns
        ]
        df_ofertas = pd.DataFrame(ofertas)
        df_ofertas.to_csv(config.out + f'{file_name}_nueva.csv', index=False)
        return df_ofertas
    except Exception as e:
        logger.error(f"Error al obtener ofertas desde {url}: {e}")
        raise

def anterior(file_name):
    try:
        df_anterior = pd.read_csv(config.out + f'{file_name}.csv')
        return df_anterior
    except FileNotFoundError:
        logger.warning(f"No se encontró el archivo anterior para {file_name}. Se asumirá que no hay datos previos.")
        return pd.DataFrame()

# Comparar 2 datasets
async def main():
    for url, file_name in config.urls:
        try:
            df_nuevo = nuevo(url, file_name)
            df_anterior = anterior(file_name)
            if not df_anterior.empty:
                cambios = df_nuevo.merge(df_anterior, indicator=True, how='left')
                cambios = cambios[cambios['_merge'] == 'left_only']
                for _, row in cambios.iterrows():
                        mensaje = (
                            f"Oferta: {row['Oferta']}\n"
                            f"Número de puestos: {row['Nº de puestos']}\n"
                            f"Fecha límite: {row['Fecha límite']}\n"
                            f"<a href='https://www.tragsa.es{row['Link']}'>Link</a>"
                        )
                        await enviar_mensaje_telegram(mensaje)
            os.rename(config.out + f'{file_name}_nueva.csv', config.out + f'{file_name}.csv')
        except Exception as e:
            logger.error(f"Error en el proceso principal para {file_name}: {e}")
            await enviar_mensaje_telegram(f"Error al procesar {file_name}: {e}")

async def enviar_mensaje_telegram(mensaje):
    try:
        bot_token = config.token
        chat_id = config.chat_id
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=mensaje, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error al enviar mensaje de Telegram: {e}")

# Ejecuta main
if __name__ == "__main__":
    asyncio.run(main())