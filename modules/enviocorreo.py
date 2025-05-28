import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def enviar_correo(destino, asunto, cuerpo):
    correo_remitente = os.getenv("EMAIL_REMITENTE")
    contrasena_app = os.getenv("EMAIL_CONTRASENA")

# Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = correo_remitente
    mensaje['To'] = destino
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
# Conectar con el servidor SMTP de Gmail
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(correo_remitente, contrasena_app)
        servidor.sendmail(correo_remitente, destino, mensaje.as_string())
        servidor.quit()
        print("✅ Correo enviado con éxito")
    except Exception as e:
        print("❌ Error al enviar el correo:", e)