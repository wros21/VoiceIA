from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_mensaje(numero, mensaje):
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    phone = os.getenv("PHONE_NUMBER")

    try:
        with TelegramClient('mi_sesion', api_id, api_hash) as client:
            client.start(phone=phone)

            contact = InputPhoneContact(
                client_id=0,
                phone=numero,
                first_name="Contacto",
                last_name=""
            )

            result = client(ImportContactsRequest([contact]))

            if result.users and len(result.users) > 0:
                user = result.users[0]
                client.send_message(user.id, mensaje)
                print("✅ Mensaje enviado correctamente a:", numero)
                return True
            else:
                print("❌ El número", numero, "no está registrado en Telegram o no se pudo importar el contacto.")
                return False
    except Exception as e:
        print("⚠️ Ocurrió un error al enviar el mensaje:", str(e))
        return False