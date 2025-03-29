import socket
import time
import re
import language_tool_python
from langdetect import detect
import os
import json

# Cargar mapa de significados desde JSON trilingüe
try:
    with open("significados.json", "r", encoding="utf-8") as jsonfile:
        mapa_significados = json.load(jsonfile)
except:
    mapa_significados = {}

# Lista de nicks humanos para excluir al detectar significado
nicks_humanos_excluir = [
    "doraemon", "SwissalpS", "@amigojapan", "Zcom", "Vox-es-bot`", "Vox-ja-bot`",
    "Vox-ru-bot`", "Vox-it-bot", "Vox-de-bot", "Vox-fr-bot`", "Vox-Assist-bot`",
    "BridgeBot3", "onizu", "Dr-Kormanstein", "LunixAI", "@gwolf", "jcay",
    "@ChanServ", "erry"
]

# Función para limpiar frase de posibles nicks humanos
def limpiar_frase_de_nicks(frase):
    palabras = frase.split()
    return " ".join(p for p in palabras if p not in nicks_humanos_excluir).strip()

# Configuración del bot
server = "irc.libera.chat"
channel = "#VoxAssist"
botnick = "doraemon"
adminname = "Zcom"
exitcode = "bye " + botnick

# Lista de bots conocidos para ignorar
ignored_bots = [
    "Vox-es-bot", "Vox-assist-bot", "lead.libera.chat",
    "Vox-fr-bot", "Vox-ru-bot", "Vox-it-bot", "Vox-de-bot", "URLxy-bot", "Dr-Kormanstein"
]

# Cargar correctores gramaticales (excepto japonés)
spell_checkers = {
    "es": language_tool_python.LanguageToolPublicAPI("es"),
    "en": language_tool_python.LanguageToolPublicAPI("en"),
    "ru": language_tool_python.LanguageToolPublicAPI("ru"),
    "de": language_tool_python.LanguageToolPublicAPI("de"),
    "it": language_tool_python.LanguageToolPublicAPI("it"),
    "fr": language_tool_python.LanguageToolPublicAPI("fr"),
    "ja": None
}

# Regex
url_pattern = re.compile(r'https?://\S+')
nick_prefix_pattern = re.compile(r'^(\w+)[,:]\s*')

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to server: " + server)
irc.connect((server, 6667))

send_irc_message = lambda msg: irc.send(bytes(msg + "\n", "UTF-8"))

send_irc_message(f"USER {botnick} {botnick} {botnick} :Python IRC")
send_irc_message(f"NICK {botnick}")
time.sleep(5)
send_irc_message(f"JOIN {channel}")

get_irc_message = lambda: irc.recv(2048).decode("UTF-8", errors='ignore')

prefix = {
    "ja": "$translate",
    "en": ".translate",
    "es": "%translate",
    "ru": "&translate",
    "de": "/translate",
    "it": "(translate",
    "fr": ")translate"
}

while True:
    message = get_irc_message().strip()
    print(message)

    if "PING" in message:
        send_irc_message("PONG :" + message.split(":")[1])

    if "PRIVMSG" in message:
        parts = message.split('PRIVMSG', 1)
        if len(parts) > 1 and ':' in parts[1]:
            msg_parts = parts[1].split(':', 1)
            sender = msg_parts[0].split('!')[0].strip()
            msg = msg_parts[1].strip()
        else:
            continue

        if sender in ignored_bots or botnick.lower() in msg.lower():
            continue

        if url_pattern.search(msg):
            continue

        if msg.lower().strip() == "kadenas":
            try:
                with open("cadenas.txt", "r") as f:
                    all_lines = [line.strip() for line in f if line.strip()]
                    last_lines = all_lines[-6:]
                    if last_lines:
                        for line in last_lines:
                            send_irc_message(f"PRIVMSG {channel} :{line}")
                    else:
                        send_irc_message(f"PRIVMSG {channel} :No undetected phrases saved.")
            except FileNotFoundError:
                send_irc_message(f"PRIVMSG {channel} :No cadenas.txt file found.")
            continue

        if msg.startswith("-"):
            continue

        manual = False
        idioma_detectado = True

        if msg.startswith("!m") and len(msg) > 3:
            manual_lang = msg[2:4].lower()
            text_to_translate = msg[4:].strip()
            manual = True
        else:
            clean_msg = msg
            match = nick_prefix_pattern.match(clean_msg)
            if match:
                clean_msg = clean_msg[len(match.group(0)):]  # remove nick:
            try:
                clean_msg = clean_msg.strip()
                if not clean_msg:
                    raise ValueError("Empty after cleaning")
                manual_lang = detect(clean_msg)
                text_to_translate = msg
            except:
                idioma_detectado = False
                manual_lang = "unknown"
                text_to_translate = msg

        supported_langs = ["es", "en", "ja", "ru", "de", "it", "fr"]

        if not idioma_detectado or manual_lang not in supported_langs:
            frase_limpia = limpiar_frase_de_nicks(msg)
            if frase_limpia in mapa_significados:
                significado_obj = mapa_significados[frase_limpia]
                for lang in supported_langs:
                    if lang != "es":
                        significado = significado_obj.get(lang, frase_limpia)
                        send_irc_message(f"PRIVMSG {channel} :{prefix[lang]} es {lang} {significado}")
                continue
            with open("cadenas.txt", "a") as f:
                f.write(msg + "\n")
            not_found_prefix = {
                "en": ".translate es en idioma no detectado",
                "ja": "$translate en ja idioma no detectado",
                "es": "%translate en es idioma no detectado",
                "ru": "&translate en ru idioma no detectado",
                "de": "/translate en de idioma no detectado",
                "it": "(translate en it idioma no detectado",
                "fr": ")translate en fr idioma no detectado"
            }
            for code, line in not_found_prefix.items():
                send_irc_message(f"PRIVMSG {channel} :{line}")
            continue

        if not text_to_translate:
            continue

        if manual_lang in spell_checkers and spell_checkers[manual_lang]:
            text_to_translate = spell_checkers[manual_lang].correct(text_to_translate)

        for lang in supported_langs:
            if lang != manual_lang:
                send_irc_message(f"PRIVMSG {channel} :{prefix[lang]} {manual_lang} {lang} {text_to_translate}")

    if exitcode in message:
        send_irc_message("QUIT")
        break

irc.close()

