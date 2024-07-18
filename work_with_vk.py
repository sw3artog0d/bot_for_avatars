import vk_api
import os
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload
import urllib.request
import ssl
import json
from PIL import Image

load_dotenv()
token = os.getenv("TOKEN")

authorize = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(authorize, group_id="202641022")

upload = vk_api.VkUpload(authorize)
attachment = []

def write_message(user_id, message, attachment):
    authorize.method("messages.send", {"user_id": user_id, "message": message, "random_id": get_random_id(), "attachment": attachment})


def max_size_user_image_url(image_sizes):
    max_size = image_sizes[0]["height"] * image_sizes[0]["width"]
    max_size_number = 0

    for size in image_sizes:
        if size["height"] * size["width"] > max_size:
            max_size = size["height"] * size["width"]
            max_size_number += 1
        else:
            continue

    return image_sizes[max_size_number]["url"]


def load_image(path):
    try:
        return Image.open(path)
    except FileNotFoundError:
        print(f"Файл изображения не найден: {path}")
        return None


def upload_image(result_image_path):
        upload_image = upload.photo_messages(photos=result_image_path)[0]
        attachment.append("photo{}_{}".format(upload_image["owner_id"], upload_image["id"]))
        return attachment


def vk_event_loop():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user and event.message.attachments == []:
            received_message = event.message.text
            user_id = event.message.peer_id
            
            if received_message == "Начать" or received_message == "Start":
                with open("frames.json", "r") as fp:
                    available_frames = json.load(fp)
            
                frame_list = ""
                number = 0
                for i in available_frames["available_frames"]:
                    frame_list += f'{number + 1}. {i["frame_name"]}\n'
                    number += 1
                write_message(user_id, f'Доступные рамки:\n{frame_list}\nВыберите номер рамки (число без точки)', [])

            elif 1 <= int(received_message) <= len(available_frames["available_frames"]):
                user_chooice_frame = received_message
                write_message(user_id, "Отличный выбор!", [])
                write_message(user_id, "Теперь отправь свою фотографию с одинаковым соотношением сторон", [])
                continue
            
            else:
                write_message(user_id, "Я не понимаю вас...", [])

        elif event.type == VkBotEventType.MESSAGE_NEW and event.from_user and event.message.attachments != []:
            
            image_sizes = event.message.attachments[0]["photo"]["sizes"]
            
            max_size_url = max_size_user_image_url(image_sizes)

            ssl._create_default_https_context = ssl._create_unverified_context
            user_image_url = max_size_url
            image_path = "./images/user_image.jpg"
            urllib.request.urlretrieve(user_image_url, image_path)

            image = load_image(image_path)
            if image is None:
                return
            frame_path = available_frames["available_frames"][int(user_chooice_frame) - 1]["path"]

            frame = load_image(frame_path).convert('RGBA')
            if frame is None:
                return
            
            # Получите размер базового изображения
            base_width, base_height = frame.size

            # Измените размер изображения наложения
            image = image.resize((base_width, base_height))
        
            # Определите позицию для наложения
            position = (0, 0)
        
            image.paste(frame, position, frame)
            
            result_image_path = "./images/result.png"
            image.save(result_image_path)
            print(f"Изображение с рамкой сохранено: {"result.png"}, {image.size}")

            upload_image(result_image_path)
            
            write_message(user_id, "Вот твоя аватарка!", attachment)

vk_event_loop()