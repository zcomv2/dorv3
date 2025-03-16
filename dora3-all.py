import socket
import time
import re
import language_tool_python  # Corrector gramatical
from langdetect import detect

# Configuración del bot
server = "irc.libera.chat"
channel = "#VoxAssist"
botnick = "doraemon"
adminname = "Zcom"
exitcode = "bye " + botnick

# Lista de bots conocidos para ignorar
ignored_bots = [
    "Vox-es-bot", "Vox-ja-bot", "Vox-Assist-bot", "lead.libera.chat",
    "Vox-fr-bot", "Vox-ru-bot", "Vox-it-bot", "Vox-de-bot", "URLxy-bot"
]

# Cargar correctores gramaticales para los 7 idiomas soportados (excepto japonés)
spell_checkers = {
    "es": language_tool_python.LanguageToolPublicAPI("es"),
    "en": language_tool_python.LanguageToolPublicAPI("en"),
    "ru": language_tool_python.LanguageToolPublicAPI("ru"),
    "de": language_tool_python.LanguageToolPublicAPI("de"),
    "it": language_tool_python.LanguageToolPublicAPI("it"),
    "fr": language_tool_python.LanguageToolPublicAPI("fr"),
    "ja": None  # No corrector disponible para japonés, pero sigue en traducción
}

# Expresión regular para detectar URLs
url_pattern = re.compile(r'https?://\S+')

# Conectar al servidor IRC
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to server: " + server)
irc.connect((server, 6667))

# Enviar mensajes al servidor
def send_irc_message(message):
    irc.send(bytes(message + "\n", "UTF-8"))

# Registrarse en el servidor
send_irc_message("USER " + botnick + " " + botnick + " " + botnick + " :Python IRC")
send_irc_message("NICK " + botnick)
time.sleep(5)
send_irc_message("JOIN " + channel)

# Leer mensajes del servidor
def get_irc_message():
    return irc.recv(2048).decode("UTF-8", errors='ignore')

# Bucle principal
while True:
    message = get_irc_message().strip()
    print(message)
    
    if "PING" in message:
        send_irc_message("PONG :" + message.split(":")[1])
    
    if "PRIVMSG" in message:
        # Extraer el nombre del usuario y el mensaje completo después de ':'
        parts = message.split('PRIVMSG', 1)
        if len(parts) > 1 and ':' in parts[1]:
            msg_parts = parts[1].split(':', 1)
            sender = msg_parts[0].split('!')[0].strip()
            msg = msg_parts[1].strip()
        else:
            continue  # Si no hay mensaje después de ':' ignorar

        # Ignorar mensajes de otros bots o si el bot se menciona a sí mismo
        if sender in ignored_bots or botnick.lower() in msg.lower():
            continue

        # Ignorar mensajes que contengan URLs
        if url_pattern.search(msg):
            continue

        # Modo desactivado: Si el mensaje empieza con '-' no traducir nada
        if msg.startswith("-"):
            continue

        # Verificar si el mensaje es en modo manual (!mXX <mensaje>)
        if msg.startswith("!m") and len(msg) > 3:
            manual_lang = msg[2:4].lower()
            text_to_translate = msg[4:].strip()
        else:
            # Modo automático: Detección del idioma
            try:
                manual_lang = detect(msg)
                text_to_translate = msg
            except:
                manual_lang = "unknown"
                text_to_translate = ""

        # Si no hay texto válido, continuar
        if not text_to_translate:
            continue

        # **Corrección ortográfica para los idiomas soportados (excepto japonés)**
        if manual_lang in spell_checkers and spell_checkers[manual_lang]:
            text_to_translate = spell_checkers[manual_lang].correct(text_to_translate)

        # Generar las traducciones adecuadas
        response_ja = response_en = response_es = response_ru = response_de = response_it = response_fr = ""
        
        if manual_lang == "es":
            response_ja = "$translate es ja " + text_to_translate
            response_en = ".translate es en " + text_to_translate
            response_ru = "&translate es ru " + text_to_translate
            response_de = "/translate es de " + text_to_translate
            response_it = "(translate es it " + text_to_translate
            response_fr = ")translate es fr " + text_to_translate
        elif manual_lang == "en":
            response_ja = "$translate en ja " + text_to_translate
            response_es = "%translate en es " + text_to_translate
            response_ru = "&translate en ru " + text_to_translate
            response_de = "/translate en de " + text_to_translate
            response_it = "(translate en it " + text_to_translate
            response_fr = ")translate en fr " + text_to_translate
        elif manual_lang == "ja":
            response_es = "%translate ja es " + text_to_translate
            response_en = ".translate ja en " + text_to_translate
            response_ru = "&translate ja ru " + text_to_translate
            response_de = "/translate ja de " + text_to_translate
            response_it = "(translate ja it " + text_to_translate
            response_fr = ")translate ja fr " + text_to_translate

        # Enviar traducciones si hay un idioma válido detectado
        if response_ja:
            send_irc_message("PRIVMSG " + channel + " :" + response_ja)
        if response_en:
            send_irc_message("PRIVMSG " + channel + " :" + response_en)
        if response_es:
            send_irc_message("PRIVMSG " + channel + " :" + response_es)
        if response_ru:
            send_irc_message("PRIVMSG " + channel + " :" + response_ru)
        if response_de:
            send_irc_message("PRIVMSG " + channel + " :" + response_de)
        if response_it:
            send_irc_message("PRIVMSG " + channel + " :" + response_it)
        if response_fr:
            send_irc_message("PRIVMSG " + channel + " :" + response_fr)
    
    # Comprobar si el bot debe desconectarse
    if exitcode in message:
        send_irc_message("QUIT")
        break

# Cerrar la conexión
irc.close()
