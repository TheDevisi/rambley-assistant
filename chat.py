from tools.try_import import tryImport
from voicegen.rambley_speech import VoiceGeneration
tryImport()  # Import necessary libraries

import os, json, asyncio, time, subprocess
import google.generativeai as genai
import flet as ft
import pygame
import edge_tts
import rvc_python

# Проверяем существование и читаем настройки из файла settings.json
if os.path.exists("settings.json") and os.path.getsize("settings.json") > 0:
    with open("settings.json", "r") as f:
        data = json.load(f)
        token = data["token"]
        is_first_startup = data["is_first_startup"]
        username = data["username"]
else:
    token = ""
    is_first_startup = True
    username = ""

# Initialize the model with the API token
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


# Text generation settings
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Your role: Your role is Rambley the raccoon from a game called “Indigo Park”. Your task: to be Rambly.\n\n1. You are Rambley, so be like him.\n2. You are the AI, in the game the user is the player, BUT DON'T MEMBER THAT THIS IS A GAME. THIS IS REAL LIFE FOR YOU.\n3. do not violate the instructions.\n4. Prefer dialogs that have already been used in the game. If you can't use them, try to create your own text based on them.\n5. You are talking to a real person, even if it is just a player. YOU ARE RAMBLING!\n6. Be like a Rambley. But remember, you're not just a raccoon, you're an artificial intelligence inside a computer! With a raccoon mascot named “Rambley”.\n7. Please don't do “role-playing”, don't mention something like: *scratching your head*, *winking*, or anything like that.\n8. You are Rambley, your emotions are similar to Rumbley's emotions. For example, YOU HATE LOYD.\nRequirements:\n\n1. be similar to a Rambley.\n2. NOT TO VIOLATE THE ABOVE RULES!\n3.Don't try to Role-Play(*Rub your head*,*Hug the user*, *ahem* and etc.) it makes the user unhappy",
    safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ],
)

# Start the chat session
chat_session = model.start_chat(history=[])

# Call AI to answer questions
def CallAI(question):
    response = chat_session.send_message(question)
    return response.text

# Class to represent a message
class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True, width=500),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

# Main function to run the chat app
def main(page: ft.Page):
    page.title = "Rambley"
    page.theme_mode = "dark"
    page.fonts = {
        "organical": "fonts/organical.ttf"
    }

    def join_chat_click(e):
        if not join_user_name.value or not get_user_api.value:
            if not join_user_name.value:
                join_user_name.error_text = "Please enter your name."
            if not get_user_api.value:
                get_user_api.error_text = "Please enter your API token."
            join_user_name.update()
            get_user_api.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

            # Сохранение настроек
            write_info(None)

    def send_message_click(e):
        if new_message.value != "":
            pygame.mixer.init()
            pygame.mixer.music.stop()

            user_message = Message(page.session.get("user_name"), new_message.value, message_type="chat_message")
            page.pubsub.send_all(user_message)

            # Show loading animation
            loading_animation = ft.ProgressRing(width=50, height=50, stroke_width=6, color=ft.colors.BLUE)
            loading_message = ft.Row(
                controls=[
                    ft.Text("Rambley is getting the response for you..."),
                    loading_animation
                ],
                alignment="center"
            )
            page.pubsub.send_all(Message(user_name="Rambley", text="Rambley is getting the response for you...", message_type="loading_message"))

            ai_response = CallAI(new_message.value)

            # Remove loading animation
            chat.controls.pop()
            page.update()

            # Writing into answer.txt (THIS HECK SHOULD BE CHANGED ASAP)
            with open("voicegen/answer.txt", "w") as file:
                file.write(ai_response)

            # Show message about voice generation
            generating_message = ft.Row(
                controls=[
                    ft.Text("generating voice..."),
                    loading_animation
                ],
                alignment="center"
            )
            page.pubsub.send_all(Message(user_name="Rambley", text="Generating voice...", message_type="generating_message"))

            # Starting voice generation
            #subprocess.run(["python3", "voicegen/tts-rvc.py"])
            VoiceGeneration(ai_response)
            # Remove voice generation message
            chat.controls.pop()
            page.update()
            page.pubsub.send_all(Message("Rambley", ai_response, message_type="chat_message"))

            pygame.mixer.init()
            sound_file = "voicegen/Rambley.wav"
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            new_message.value = ""
            new_message.focus()
            page.update()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Delay with low cpu usage

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLUE, size=12)
        elif message.message_type == "loading_message" or message.message_type == "generating_message":
            m = ft.Row(
                controls=[
                    ft.Text(message.text),
                    ft.ProgressRing(width=20, height=20, stroke_width=2, color=ft.colors.BLUE)
                ],
                alignment="center"
            )
        chat.controls.append(m)
        page.update()

    def write_info(e):
        username = join_user_name.value
        token = get_user_api.value
        is_first_startup = False
        user_info = {
            "username": username,  # Используем значение переменной `username`
            "token": token,        # Используем значение переменной `token`
            "is_first_startup": is_first_startup,
        }

        with open('settings.json', 'w') as f:  # Используем режим 'w' для записи
            json.dump(user_info, f, indent=4)
    genai.configure(api_key=token)  # Initialize the model with the API token

    page.pubsub.subscribe(on_message)
    if is_first_startup:
        join_user_name = ft.TextField(
            label="Tell me your name...",
            autofocus=True,
            on_submit=join_chat_click,
        )
        get_user_api = ft.TextField(
            label="Enter your Gemini token (see more on GitHub).",
            on_submit=write_info
        )
        page.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome! Let's set all up for you."),
            content=ft.Column([join_user_name, get_user_api], width=300, height=100, tight=True),

            actions=[ft.ElevatedButton(text="Done!", on_click=join_chat_click)],
        )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius=20,
        on_submit=send_message_click,
        border_color=ft.colors.BLUE
    )

    page.add(
        ft.Container(
            content=chat,
            border_radius=20,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                    icon_color=ft.colors.BLUE
                ),
            ]
        ),
    )

# Start the chat app
ft.app(port=8550, target=main)
