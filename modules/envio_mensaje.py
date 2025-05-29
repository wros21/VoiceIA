from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest, GetContactsRequest
from telethon.tl.types import InputPhoneContact
from telethon.errors import UsernameNotOccupiedError, PhoneNumberInvalidError
import os
import re
import asyncio
from dotenv import load_dotenv

load_dotenv()

class TelegramSender:
    def __init__(self, timeout=60, flood_sleep_threshold=60):
        self.api_id = int(os.getenv("API_ID"))
        self.api_hash = os.getenv("API_HASH")
        self.phone = os.getenv("PHONE_NUMBER")
        self.timeout = timeout
        self.flood_sleep_threshold = flood_sleep_threshold
        self.client = None
    
    def __enter__(self):
        # Configurar timeouts en el cliente
        self.client = TelegramClient(
            'mi_sesion', 
            self.api_id, 
            self.api_hash,
            timeout=self.timeout,                    # Timeout para operaciones
            request_retries=3,                       # Reintentos automáticos
            connection_retries=5,                    # Reintentos de conexión
            retry_delay=1,                           # Delay entre reintentos
            flood_sleep_threshold=self.flood_sleep_threshold  # Manejo de flood wait
        )
        self.client.start(phone=self.phone)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.disconnect()
    
    def es_numero_telefono(self, contacto):
        """Determina si el contacto es un número de teléfono"""
        # Patrón para detectar números (con o sin código de país)
        patron = r'^[\+]?[0-9\s\-\(\)]{7,}
    
    async def buscar_por_numero(self, numero):
        """Busca un usuario por número de teléfono"""
        try:
            # Validar que sea un número de Guatemala
            if not self.es_numero_guatemala_valido(numero):
                print(f"❌ Número inválido para Guatemala: {numero}")
                print("💡 Formatos válidos: +50212345678, 50212345678, 12345678")
                return None
            
            numero_limpio = self.limpiar_numero(numero)
            print(f"📱 Número formateado: {numero_limpio}")
            
            # Crear contacto temporal
            contact = InputPhoneContact(
                client_id=0,
                phone=numero_limpio,
                first_name="Contacto Temporal",
                last_name=""
            )
            
            # Usar timeout específico para esta operación
            result = await asyncio.wait_for(
                self.client(ImportContactsRequest([contact])),
                timeout=self.timeout
            )
            
            if result.users and len(result.users) > 0:
                return result.users[0]
            else:
                return None
                
        except ValueError as e:
            print(f"❌ {str(e)}")
            return None
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al buscar número: {numero}")
            return None
        except PhoneNumberInvalidError:
            print(f"❌ Número de teléfono inválido: {numero}")
            return None
        except Exception as e:
            print(f"⚠️ Error al buscar por número: {str(e)}")
            return None
    
    async def buscar_por_username(self, username):
        """Busca un usuario por nombre de usuario"""
        try:
            # Asegurar que el username tenga @ al inicio
            if not username.startswith('@'):
                username = '@' + username
            
            # Usar timeout específico
            user = await asyncio.wait_for(
                self.client.get_entity(username),
                timeout=self.timeout
            )
            return user
            
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al buscar username: {username}")
            return None
        except UsernameNotOccupiedError:
            print(f"❌ Usuario no encontrado: {username}")
            return None
        except Exception as e:
            print(f"⚠️ Error al buscar por username: {str(e)}")
            return None
    
    async def buscar_por_nombre(self, nombre):
        """Busca un usuario por nombre en los contactos"""
        try:
            # Usar la función correcta de Telethon para obtener contactos
            result = await asyncio.wait_for(
                self.client(GetContactsRequest(hash=0)),
                timeout=self.timeout
            )
            
            # Los contactos están en result.users
            contacts = result.users
            
            # Buscar por nombre (case insensitive)
            for contact in contacts:
                if hasattr(contact, 'first_name') and hasattr(contact, 'last_name'):
                    nombre_completo = f"{contact.first_name or ''} {contact.last_name or ''}".strip().lower()
                    if nombre.lower() in nombre_completo:
                        return contact
                
                # También buscar en el username si existe (pero solo para comparar con nombre)
                if hasattr(contact, 'username') and contact.username:
                    if nombre.lower() == contact.username.lower():
                        return contact
            
            return None
            
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al buscar contactos por nombre: {nombre}")
            return None
        except Exception as e:
            print(f"⚠️ Error al buscar por nombre: {str(e)}")
            return None
    
    async def enviar_mensaje_async(self, contacto, mensaje):
        """Envía un mensaje de forma asíncrona"""
        try:
            user = None
            
            # Determinar el tipo de contacto y buscar el usuario
            if self.es_numero_telefono(contacto):
                print(f"🔍 Buscando por número: {contacto}")
                user = await self.buscar_por_numero(contacto)
            else:
                print(f"🔍 Buscando por nombre en contactos: {contacto}")
                user = await self.buscar_por_nombre(contacto)
            
            if user:
                # Enviar mensaje con timeout
                await asyncio.wait_for(
                    self.client.send_message(user, mensaje),
                    timeout=self.timeout
                )
                nombre_usuario = f"{user.first_name or ''} {user.last_name or ''}".strip() or str(user.id)
                print(f"✅ Mensaje enviado correctamente a: {nombre_usuario}")
                return True
            else:
                print(f"❌ No se pudo encontrar el contacto: {contacto}")
                print("💡 Asegúrate de que el contacto esté guardado en tu lista de contactos")
                return False
                
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al enviar mensaje a: {contacto}")
            return False
        except Exception as e:
            print(f"⚠️ Error al enviar mensaje: {str(e)}")
            return False

def enviar_mensaje(contacto, mensaje, timeout=60):
    """Función principal para enviar mensajes (compatible con código anterior)"""
    try:
        with TelegramSender(timeout=timeout) as sender:
            # Si es un número, intentar agregar +502 automáticamente si no lo tiene
            if sender.es_numero_telefono(contacto):
                # Validar y formatear para Guatemala
                if not sender.es_numero_guatemala_valido(contacto):
                    return f"❌ Número inválido para Guatemala: {contacto}. Use formatos: +50212345678, 50212345678, o 12345678"
            
            # Usar el cliente sincronizado para mantener compatibilidad
            import asyncio
            resultado = asyncio.get_event_loop().run_until_complete(
                sender.enviar_mensaje_async(contacto, mensaje)
            )
            
            if resultado:
                return "✅ Mensaje enviado correctamente"
            else:
                return "❌ No se pudo enviar el mensaje"
                
    except Exception as e:
        return f"⚠️ Error general: {str(e)}"

# Función adicional para múltiples contactos
def enviar_mensajes_multiples(contactos, mensaje, timeout=60):
    """Envía el mismo mensaje a múltiples contactos"""
    resultados = []
    
    with TelegramSender(timeout=timeout) as sender:
        import asyncio
        loop = asyncio.get_event_loop()
        
        for contacto in contactos:
            resultado = loop.run_until_complete(
                sender.enviar_mensaje_async(contacto, mensaje)
            )
            resultados.append({'contacto': contacto, 'exitoso': resultado})
    
    return resultados

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplos de contactos válidos (solo número y nombre)
    ejemplos = [
        "+502 1234 5678",      # Número con formato
        "50212345678",         # Número sin formato
        "Juan Pérez",          # Nombre del contacto guardado
        "María García",        # Otro nombre de contacto
    ]
    
    mensaje = "¡Hola! Este es un mensaje de prueba."
    
    # Enviar a un solo contacto
    # enviar_mensaje("+502 1234 5678", mensaje)
    
    # Enviar a múltiples contactos
    # resultados = enviar_mensajes_multiples(ejemplos, mensaje)
    # print("Resultados:", resultados)
        return bool(re.match(patron, contacto.strip()))
    
    def validar_numero_guatemala(self, numero):
        """Valida y formatea números de Guatemala"""
        numero_limpio = re.sub(r'[^\+0-9]', '', numero)
        
        # Si ya tiene código de país +502, validar que tenga 8 dígitos después
        if numero_limpio.startswith('+502'):
            numero_sin_codigo = numero_limpio[4:]
            if len(numero_sin_codigo) == 8 and numero_sin_codigo[0] in ['2', '3', '4', '5', '6', '7', '8', '9']:
                return numero_limpio
            else:
                return None
        
        # Si tiene 502 al inicio (sin +), agregar el +
        elif numero_limpio.startswith('502') and len(numero_limpio) == 11:
            numero_sin_codigo = numero_limpio[3:]
            if numero_sin_codigo[0] in ['2', '3', '4', '5', '6', '7', '8', '9']:
                return f"+{numero_limpio}"
            else:
                return None
        
        # Si son 8 dígitos, agregar +502
        elif len(numero_limpio) == 8 and numero_limpio[0] in ['2', '3', '4', '5', '6', '7', '8', '9']:
            return f"+502{numero_limpio}"
        
        # Si no cumple ningún formato válido de Guatemala
        else:
            return None
    
    def limpiar_numero(self, numero):
        """Limpia y valida el número para Guatemala"""
        numero_validado = self.validar_numero_guatemala(numero)
        if numero_validado:
            return numero_validado
        else:
            raise ValueError(f"Número inválido para Guatemala: {numero}")
    
    def es_numero_guatemala_valido(self, numero):
        """Verifica si es un número válido de Guatemala"""
        try:
            numero_validado = self.validar_numero_guatemala(numero)
            return numero_validado is not None
        except:
            return False
    
    async def buscar_por_numero(self, numero):
        """Busca un usuario por número de teléfono"""
        try:
            numero_limpio = self.limpiar_numero(numero)
            
            # Crear contacto temporal
            contact = InputPhoneContact(
                client_id=0,
                phone=numero_limpio,
                first_name="Contacto Temporal",
                last_name=""
            )
            
            # Usar timeout específico para esta operación
            result = await asyncio.wait_for(
                self.client(ImportContactsRequest([contact])),
                timeout=self.timeout
            )
            
            if result.users and len(result.users) > 0:
                return result.users[0]
            else:
                return None
                
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al buscar número: {numero}")
            return None
        except PhoneNumberInvalidError:
            print(f"❌ Número de teléfono inválido: {numero}")
            return None
        except Exception as e:
            print(f"⚠️ Error al buscar por número: {str(e)}")
            return None
    
    async def buscar_por_username(self, username):
        """Busca un usuario por nombre de usuario"""
        try:
            # Asegurar que el username tenga @ al inicio
            if not username.startswith('@'):
                username = '@' + username
            
            # Usar timeout específico
            user = await asyncio.wait_for(
                self.client.get_entity(username),
                timeout=self.timeout
            )
            return user
            
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al buscar username: {username}")
            return None
        except UsernameNotOccupiedError:
            print(f"❌ Usuario no encontrado: {username}")
            return None
        except Exception as e:
            print(f"⚠️ Error al buscar por username: {str(e)}")
            return None
    
    async def buscar_por_nombre(self, nombre):
        """Busca un usuario por nombre en los contactos"""
        try:
            # Usar la función correcta de Telethon para obtener contactos
            result = await asyncio.wait_for(
                self.client(GetContactsRequest(hash=0)),
                timeout=self.timeout
            )
            
            # Los contactos están en result.users
            contacts = result.users
            
            # Buscar por nombre (case insensitive)
            for contact in contacts:
                if hasattr(contact, 'first_name') and hasattr(contact, 'last_name'):
                    nombre_completo = f"{contact.first_name or ''} {contact.last_name or ''}".strip().lower()
                    if nombre.lower() in nombre_completo:
                        return contact
                
                # También buscar en el username si existe (pero solo para comparar con nombre)
                if hasattr(contact, 'username') and contact.username:
                    if nombre.lower() == contact.username.lower():
                        return contact
            
            return None
            
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al buscar contactos por nombre: {nombre}")
            return None
        except Exception as e:
            print(f"⚠️ Error al buscar por nombre: {str(e)}")
            return None
    
    async def enviar_mensaje_async(self, contacto, mensaje):
        """Envía un mensaje de forma asíncrona"""
        try:
            user = None
            
            # Determinar el tipo de contacto y buscar el usuario
            if self.es_numero_telefono(contacto):
                print(f"🔍 Buscando por número: {contacto}")
                user = await self.buscar_por_numero(contacto)
            else:
                print(f"🔍 Buscando por nombre en contactos: {contacto}")
                user = await self.buscar_por_nombre(contacto)
            
            if user:
                # Enviar mensaje con timeout
                await asyncio.wait_for(
                    self.client.send_message(user, mensaje),
                    timeout=self.timeout
                )
                nombre_usuario = f"{user.first_name or ''} {user.last_name or ''}".strip() or str(user.id)
                print(f"✅ Mensaje enviado correctamente a: {nombre_usuario}")
                return True
            else:
                print(f"❌ No se pudo encontrar el contacto: {contacto}")
                print("💡 Asegúrate de que el contacto esté guardado en tu lista de contactos")
                return False
                
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout al enviar mensaje a: {contacto}")
            return False
        except Exception as e:
            print(f"⚠️ Error al enviar mensaje: {str(e)}")
            return False

def enviar_mensaje(contacto, mensaje, timeout=60):
    """Función principal para enviar mensajes (compatible con código anterior)"""
    try:
        with TelegramSender(timeout=timeout) as sender:
            # Usar el cliente sincronizado para mantener compatibilidad
            import asyncio
            return asyncio.get_event_loop().run_until_complete(
                sender.enviar_mensaje_async(contacto, mensaje)
            )
    except Exception as e:
        print(f"⚠️ Error general: {str(e)}")
        return False

# Función adicional para múltiples contactos
def enviar_mensajes_multiples(contactos, mensaje, timeout=60):
    """Envía el mismo mensaje a múltiples contactos"""
    resultados = []
    
    with TelegramSender(timeout=timeout) as sender:
        import asyncio
        loop = asyncio.get_event_loop()
        
        for contacto in contactos:
            resultado = loop.run_until_complete(
                sender.enviar_mensaje_async(contacto, mensaje)
            )
            resultados.append({'contacto': contacto, 'exitoso': resultado})
    
    return resultados
