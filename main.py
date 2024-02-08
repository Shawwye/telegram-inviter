import os
import asyncio
from telethon import TelegramClient, functions
from telethon.tl.types import InputPeerChat

api_id = '21273201'
api_hash = '12483496e31e7cd597d3af225bbf886b'

async def invite_user_to_group(client, group_username, user_username):
    group = await client.get_entity(group_username)

    user = await client.get_entity(user_username)

    try:
        await client(functions.channels.InviteToChannelRequest(
            channel=group,
            users=[user]
        ))
        print(f"Пользователь {user_username} приглашен в группу {group_username}")
    except Exception as e:
        print(f"Ошибка: {e}")

async def main():
    sessions_folder = 'sessions'
    sessions_files = os.listdir(sessions_folder)
    print("Доступные сессии:")
    for idx, session in enumerate(sessions_files, start=1):
        print(f"{idx}. {session}")
    session_idx = int(input("Выберите номер сессии: "))
    session_path = os.path.join(sessions_folder, sessions_files[session_idx - 1])

    delay = int(input("Введите задержку между инвайтами (в секундах): "))
    group_username = input("Введите ссылку на группу: ")

    async with TelegramClient(session_path, api_id, api_hash) as client:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            users = [user.strip() for user in users]

        for user_username in users:
            await invite_user_to_group(client, group_username, user_username)
            await asyncio.sleep(delay)

asyncio.run(main())
