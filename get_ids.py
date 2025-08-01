
import os
import requests

TOKEN = os.getenv("BOT_TOKEN", "7565787276:AAFUaIVgJtydVZD_WEZ_o2k-mJoxcz_I9T0")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_all_chats():
    offset = None
    chats = {}
    while True:
        params = {"limit": 100, "timeout": 0}
        if offset is not None:
            params["offset"] = offset
        resp = requests.get(f"{API_URL}/getUpdates", params=params)
        resp.raise_for_status()
        updates = resp.json().get("result", [])
        if not updates:
            break
        for upd in updates:
            # сразу подтверждаем апдейт, чтобы он не возвращался снова
            offset = upd["update_id"] + 1

            # извлекаем объект chat из любого типа апдейта
            chat = None
            if "message" in upd and upd["message"].get("chat"):
                chat = upd["message"]["chat"]
            elif "edited_message" in upd and upd["edited_message"].get("chat"):
                chat = upd["edited_message"]["chat"]
            elif "channel_post" in upd and upd["channel_post"].get("chat"):
                chat = upd["channel_post"]["chat"]
            elif "my_chat_member" in upd and upd["my_chat_member"].get("chat"):
                chat = upd["my_chat_member"]["chat"]

            if chat:
                chats[chat["id"]] = chat
    return chats

def get_chat_info(chat_id):
    r = requests.get(f"{API_URL}/getChat", params={"chat_id": chat_id})
    r.raise_for_status()
    return r.json()["result"]

def main():
    chats = get_all_chats()
    print(f"Найдено уникальных чатов/групп: {len(chats)}\n")
    for chat_id, c in chats.items():
        info = get_chat_info(chat_id)
        # читаемое имя: title (для групп/каналов) или username или имя+фамилия
        title = info.get("title") \
                or info.get("username") \
                or f"{info.get('first_name','')} {info.get('last_name','')}".strip() \
                or "<без названия>"
        print(f"{title}  ({info['type']}) → ID = {chat_id}")

if __name__ == "__main__":
    main()
