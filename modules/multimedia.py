import webbrowser
import subprocess
import sys
import os
import re

def handle_multimedia(command):
    """
    Maneja comandos multimedia con diferentes modos de reproducción
    """
    command = command.lower()
    
    # Determinar modo de reproducción preferido
    browser_mode = any(word in command for word in ["youtube", "navegador", "pantalla", "video"])
    
    if "youtube" in command and ("música" in command or "musica" in command):
        search_term = extract_music_search(command)
        if browser_mode or "video" in command:
            return play_youtube_browser(search_term)
        else:
            return play_youtube_choice(search_term)
        
    elif any(phrase in command for phrase in ["pon música", "pon musica", "reproduce música", "reproduce musica"]):
        search_term = extract_music_search(command) or "música"
        return play_youtube_choice(search_term)
        
    elif "youtube" in command:
        search_term = extract_youtube_search(command)
        if search_term:
            return open_youtube_with_search(search_term)
        else:
            webbrowser.open("https://www.youtube.com")
            return "Abriendo YouTube"
            
    elif "spotify" in command:
        return handle_spotify(command)
        
    else:
        return "No reconozco ese servicio multimedia."

def extract_music_search(command):
    """
    Extrae términos de búsqueda musical del comando
    """
    # Patrones comunes para música
    patterns = [
        r"música de ([\w\s]+)",
        r"musica de ([\w\s]+)", 
        r"pon ([\w\s]+)",
        r"reproduce ([\w\s]+)",
        r"(rock|pop|jazz|clásica|classical|reggaeton|salsa|bachata|merengue|electronic|electrónica|rap|hip hop|blues|country)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            result = match.group(1).strip()
            # Filtrar palabras comunes
            if result not in ["música", "musica", "algo", "una", "canción"]:
                return result
    
    return "música"

def extract_youtube_search(command):
    """
    Extrae términos de búsqueda para YouTube
    """
    # Remover "youtube" y palabras comunes
    search = re.sub(r'\b(youtube|en|abre|abrir|busca|buscar)\b', '', command)
    search = search.strip()
    
    if len(search) > 3:
        return search
    return None

def play_youtube_choice(search_term):
    """
    Ofrece opción entre reproducción en navegador o solo audio
    """
    # Para tu asistente de voz, decidir automáticamente
    # Si prefieres siempre navegador, cambiar a play_youtube_browser
    return play_youtube_browser(search_term)

def play_youtube_browser(search_term):
    """
    Reproduce música en YouTube en el navegador (con video)
    """
    try:
        # Método 1: Selenium para autoplay real
        if check_selenium():
            return play_with_selenium_autoplay(search_term)
        
        # Método 2: URL optimizada para autoplay
        else:
            return play_youtube_optimized_autoplay(search_term)
            
    except Exception as e:
        return play_youtube_optimized_autoplay(search_term)

def play_with_selenium_autoplay(search_term):
    """
    Usa selenium para abrir YouTube y reproducir automáticamente
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        import time
        
        # Configurar Chrome para autoplay
        chrome_options = Options()
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor") 
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Ejecutar en background para no bloquear el asistente
        driver = webdriver.Chrome(options=chrome_options)
        
        # Buscar en YouTube
        search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
        driver.get(search_url)
        
        # Esperar y hacer clic en el primer video
        wait = WebDriverWait(driver, 10)
        
        # Buscar el primer video clickeable
        video_selectors = [
            "a#video-title",
            "h3.ytd-video-renderer a",
            ".ytd-video-renderer a[href*='/watch']"
        ]
        
        for selector in video_selectors:
            try:
                first_video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                first_video.click()
                break
            except:
                continue
        
        # Esperar a que cargue el video
        time.sleep(2)
        
        # Intentar hacer clic en play si está pausado
        try:
            play_button = driver.find_element(By.CSS_SELECTOR, ".ytp-play-button")
            if "ytp-play-button" in play_button.get_attribute("class"):
                play_button.click()
        except:
            pass
            
        return f"Reproduciendo '{search_term}' en YouTube"
        
    except ImportError:
        return "Para reproducción automática instala: pip install selenium"
    except Exception as e:
        return play_youtube_optimized_autoplay(search_term)

def play_youtube_optimized_autoplay(search_term):
    """
    Abre YouTube con parámetros optimizados para autoplay
    """
    search_query = search_term.replace(' ', '+')
    
    # URLs con diferentes estrategias de autoplay
    urls = [
        f"https://www.youtube.com/results?search_query={search_query}&autoplay=1",
        f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAQ%253D%253D",  # Solo videos
    ]
    
    webbrowser.open(urls[0])
    return f"Buscando '{search_term}' en YouTube - Haz clic en un video para reproducir"

def handle_spotify(command):
    """
    Maneja comandos de Spotify con control de reproducción
    """
    # Primero abrir Spotify
    spotify_opened = open_spotify_app()
    
    # Si se pide reproducción específica
    if any(word in command for word in ["reproduce", "pon", "música", "musica"]):
        search_term = extract_music_search(command)
        if search_term and search_term != "música":
            return control_spotify_macos(search_term)
        else:
            return control_spotify_macos()
    
    return spotify_opened

def open_spotify_app():
    """
    Abre la aplicación de Spotify
    """
    try:
        # Windows
        if sys.platform == "win32":
            spotify_paths = [
                os.path.expanduser("~\\AppData\\Roaming\\Spotify\\Spotify.exe"),
                "spotify"  # Si está en PATH
            ]
            
            for path in spotify_paths:
                try:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        return "Spotify abierto"
                    else:
                        subprocess.Popen([path])
                        return "Spotify abierto"
                except:
                    continue
        
        # macOS
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Spotify"])
            return "Spotify abierto"
        
        # Linux
        elif sys.platform == "linux":
            subprocess.Popen(["spotify"])
            return "Spotify abierto"
        
        # Fallback a Spotify Web
        webbrowser.open("https://open.spotify.com")
        return "Abriendo Spotify Web"
        
    except Exception as e:
        webbrowser.open("https://open.spotify.com")
        return "Abriendo Spotify Web"

def open_youtube_with_search(search_term):
    """
    Abre YouTube con búsqueda específica
    """
    search_query = search_term.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(url)
    return f"Buscando '{search_term}' en YouTube"

def check_selenium():
    """
    Verifica si selenium está disponible
    """
    try:
        import selenium
        from selenium import webdriver
        return True
    except ImportError:
        return False

def check_command_exists(command):
    """
    Verifica si un comando existe en el sistema
    """
    try:
        result = subprocess.run([command, "--version"], 
                              capture_output=True, 
                              timeout=5)
        return result.returncode == 0
    except:
        return False

# Función para configurar el modo de reproducción preferido
def set_playback_mode(mode="browser"):
    """
    Configura el modo de reproducción preferido
    mode: "browser" para YouTube con video, "audio" para solo audio
    """
    global PLAYBACK_MODE
    PLAYBACK_MODE = mode
    return f"Modo de reproducción configurado a: {mode}"

# Variable global para modo de reproducción
PLAYBACK_MODE = "browser"

def control_spotify_macos(search_term=None):
    """
    Controla Spotify en macOS usando AppleScript
    """
    if sys.platform != "darwin":
        return "Control de Spotify solo disponible en macOS"
    
    try:
        import time
        
        # Primero asegurar que Spotify esté abierto
        open_script = '''
        tell application "Spotify"
            activate
        end tell
        '''
        subprocess.run(["osascript", "-e", open_script], check=True)
        
        # Esperar un momento para que Spotify se abra completamente
        time.sleep(2)
        
        if search_term:
            # Buscar música específica
            search_script = f'''
            tell application "Spotify"
                activate
                tell application "System Events"
                    tell process "Spotify"
                        -- Usar Command+L para ir a la barra de búsqueda
                        key code 37 using command down
                        delay 0.5
                        -- Escribir el término de búsqueda
                        keystroke "{search_term}"
                        delay 1
                        -- Presionar Enter para buscar
                        key code 36
                        delay 2
                        -- Presionar Enter otra vez para reproducir el primer resultado
                        key code 36
                    end tell
                end tell
            end tell
            '''
            
            subprocess.run(["osascript", "-e", search_script], check=True)
            return f"Buscando y reproduciendo '{search_term}' en Spotify"
            
        else:
            # Solo reproducir lo que esté en la playlist actual
            play_script = '''
            tell application "Spotify"
                activate
                play
            end tell
            '''
            
            subprocess.run(["osascript", "-e", play_script], check=True)
            return "Reproduciendo música en Spotify"
            
    except subprocess.CalledProcessError:
        return "Error al controlar Spotify - Asegúrate de que esté instalado"
    except Exception as e:
        return f"Error al controlar Spotify: {str(e)}"

def pause_spotify_macos():
    """
    Pausa Spotify en macOS
    """
    if sys.platform != "darwin":
        return "Control de Spotify solo disponible en macOS"
    
    try:
        pause_script = '''
        tell application "Spotify"
            pause
        end tell
        '''
        subprocess.run(["osascript", "-e", pause_script], check=True)
        return "Música pausada en Spotify"
    except:
        return "Error al pausar Spotify"

def next_track_spotify_macos():
    """
    Siguiente canción en Spotify macOS
    """
    if sys.platform != "darwin":
        return "Control de Spotify solo disponible en macOS"
    
    try:
        next_script = '''
        tell application "Spotify"
            next track
        end tell
        '''
        subprocess.run(["osascript", "-e", next_script], check=True)
        return "Siguiente canción en Spotify"
    except:
        return "Error al cambiar canción"

# Ejemplo de uso mejorado
if __name__ == "__main__":
    print("=== Sistema Multimedia Mejorado ===")
    
    # Verificar capacidades
    print("Capacidades disponibles:")
    print(f"  Selenium: {'✓' if check_selenium() else '✗'}")
    
    # Test commands
    test_commands = [
        "pon música rock",
        "youtube música clásica", 
        "reproduce reggaeton en youtube",
        "spotify reproduce algo",
        "abre youtube videos de gatos"
    ]
    
    for cmd in test_commands:
        print(f"\nComando: '{cmd}'")
        result = handle_multimedia(cmd)
        print(f"Resultado: {result}")
    