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

This documentation covers everything you need to use Doraemon Bot effectively in the chat. 🚀

