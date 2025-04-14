TOKEN = ""
ID = ""  # Can be obtained using 3rd party clients or @userinfobot bot inside TG

LOGPATH = r""

import json
import time

import requests
import telebot

bot = telebot.TeleBot(TOKEN)
send_message = lambda text: bot.send_message(ID, text, parse_mode="Markdown")


def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def main() -> None:
    send_message("Bot enabled.")

    old = ""

    for line in follow(open(LOGPATH, "r", encoding="utf-8")):
        line = line.strip()
        try:
            if line.split()[4] != "[CHAT]" or "Position in queue: " not in line:
                continue
            line = line[line.index("Position in queue: ") + len("Position in queue: "):]
            pos = line[:line.index("\\n")]
            line = "Position in queue: " + pos
            if old == line:
                continue
            old = line
            players = json.loads(requests.get("https://api.mcstatus.io/v2/status/java/2b2t.org").text)["players"]
            message = ["*" + line + "*\n", f"Online: {players['online']}"]
            for i in players["list"]:
                message.append(i["name_clean"])
            message = "\n".join(message)
            send_message(message)
            print(message + "\n")
        except IndexError:
            pass


if __name__ == "__main__":
    try:
        main()
        bot.infinity_polling()
    except KeyboardInterrupt:
        exit(0)
