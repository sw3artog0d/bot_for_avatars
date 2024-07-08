from PIL import Image

def load_image(image_path):
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print(f"Файл изображения не найден: {image_path}")
        return None


def main():
    image_path = "./images/cat_with_lazers.jpg"

    image = load_image(image_path)
    if image is None:
        return

    available_frames = [
        "./images/white_frame.png",
        "./images/green_frame.png",
    ]

    print("Доступные рамки:")
    for i, frame_name in enumerate(available_frames):
        print(f"{i + 1}. {frame_name}")

    # Выбор рамки пользователем
    while True:
        try:
            frame_choice = int(input("Выберите номер рамки: "))
            if 1 <= frame_choice <= len(available_frames):
                break
            else:
                print("Неверный номер рамки.")
        except ValueError:
            print("Введите число.")

    # Получение пути к выбранной рамке
    frame_path = available_frames[frame_choice - 1]

    frame = load_image(frame_path).convert('RGBA')
    if frame is None:
        return
    
    # Получите размер базового изображения
    base_width, base_height = image.size

    # Измените размер изображения наложения
    overlay_img_resized = frame.resize((base_width, base_height))

    # Определите позицию для наложения
    position = (0, 0)

    image.paste(overlay_img_resized, position, overlay_img_resized)
    
    image.save('result.png')
    print(f"Изображение с рамкой сохранено: {'result.png'}")


if __name__ == "__main__":
    main()