import webbrowser

def handle_multimedia(command):
    command = command.lower()

    if "youtube" in command and ("música" in command or "musica" in command):
        webbrowser.open("https://www.youtube.com/results?search_query=música")
        return "Reproduciendo música en YouTube"

    elif "pon música" in command or "pon musica" in command:
        webbrowser.open("https://www.youtube.com/results?search_query=música")
        return "Poniendo música en YouTube"

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Abriendo YouTube"

    elif "spotify" in command:
        webbrowser.open("https://open.spotify.com")
        return "Abriendo Spotify..."

    else:
        return "No reconozco ese servicio multimedia."
