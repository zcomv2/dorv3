# dorv3

1️⃣ Automatic Translation Mode

How it works

If a user sends a message without any prefix, the bot will automatically detect the language and translate it into the six remaining languages.

The translations will appear with the correct syntax used in the chat.

Example:

User: Hello everyone, how are you?

Bot:

    $translate en ja Hello everyone, how are you?
    
    %translate en es Hello everyone, how are you?
    
    &translate en ru Hello everyone, how are you?
    
    /translate en de Hello everyone, how are you?
    
    (translate en it Hello everyone, how are you?
    
    )translate en fr Hello everyone, how are you?
    

⚠ Important Notice for Doraemon Bot

To ensure that Doraemon's translation system works correctly, you must have all the corresponding Limnoria (old Supybot) translation bots active in the same channel.

Each translation bot must be configured with its corresponding prefix symbol to properly receive and respond to the translation messages sent by Doraemon.

If any of these bots are missing or incorrectly set up, translations will fail or not be delivered correctly. ✅

The 6 Limnoria (old Supybot) bots must have the "Google" plugin loaded, as it contains the "translate" function. Also, remember to set the correct prefix symbol for each translation language.

2️⃣ Manual Translation Mode

How to use it

Use the prefix !m<language_code> <message> to manually specify the source language.

The bot will translate the message from the selected language into the other six languages.

Supported Language Codes:

Language

Code

Command Example

Spanish

es

!mes Hello everyone!

English

en

!men Hello everyone!

Japanese

ja

!mja Hello everyone!

Russian

ru

!mru Hello everyone!

German

de

!mde Hello everyone!

Italian

it

!mit Hello everyone!

French

fr

!mfr Hello everyone!

Example:

User: !men Hello everyone!
Bot:
    $translate en ja Hello everyone!
    %translate en es Hello everyone!
    &translate en ru Hello everyone!
    /translate en de Hello everyone!
    (translate en it Hello everyone!
    )translate en fr Hello everyone!

3️⃣ Deactivated Mode

How to use it

If a user starts a message with -, the bot will not translate the message.

This is useful when you want to send a message without triggering the bot.

Example:

User: - This message will not be translated.
Bot: (No response, the bot ignores it.)

Summary of Features

✅ Supported Languages:

Spanish (es)

English (en)

Japanese (ja)

Russian (ru)

German (de)

Italian (it)

French (fr)

🛠 Modes of Operation:

Automatic Translation → No prefix required, bot detects and translates.

Manual Translation → Use !m<language_code> to specify the source language.

Deactivated Mode → Use - at the beginning of a message to prevent translation.

🆕 New Features Added 🚀🔥

✅ Language correction added: Doraemon now automatically corrects spelling and grammar in Spanish, English, Russian, German, Italian, and French before translating.

❌ Japanese (ja) is not corrected but is still translated.

✅ Bot ignoring updated: Doraemon now ignores URLxy-bot, which posts URL titles, and will not read or translate any messages containing URLs (http:// or https://).

✅Undetected Language Handling

If language detection fails:

The original message is saved in cadenas.txt.

A predefined warning (“Language not detected”) is sent in all translation formats.

✅Command kadenas

Users can type kadenas in the channel.

Doraemon will reply with the last 1–6 lines from cadenas.txt (phrases where language detection failed).

Thinking that Doraemon is ignored and the last 6 undetected phrases won't be seen; to fix this, unignore Doraemon and observe the behavior in developer mode.

### 🧩 Undetected Phrase Recognition via JSON Mapping

When the bot cannot detect the language of a message:

- It **cleans the phrase**, removing any known human nicknames (e.g. `Zcom`, `doraemon`, etc.).

- It then checks the cleaned phrase against a predefined **`significados.json`** file.

- If a **matching phrase** is found in the JSON:

  - The associated **meaning** is used as the message to be translated instead of the original phrase.

  - This meaning is then **broadcasted to all translation bots** using their appropriate prefix format.

- If no match is found:

  - The phrase is stored in `cadenas.txt` for future review or training.

  - The bot sends a “language not detected” message in all supported translation prefixes.

This feature allows Doraemon to **handle unknown or ambiguous expressions more intelligently**, improving translation clarity and allowing for community-based learning over time.


Doraemon is now smarter and more efficient in translations! 🚀🔥

[ Codename: #LingoHeroine ]

