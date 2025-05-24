# modules/multimedia.py
import webbrowser


def handle_multimedia(command):
    if "youtube" in command:
        query = command.replace("reproduce", "").replace("en youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Buscando {query} en YouTube..."

    elif "spotify" in command:
        webbrowser.open("https://open.spotify.com")
        return "Abriendo Spotify..."

    else:
        return "No reconozco ese servicio multimedia."
