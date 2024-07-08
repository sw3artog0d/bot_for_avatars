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
    base_width, base_height = frame.size

    # Измените размер изображения наложения
    image = image.resize((base_width, base_height))

    # Определите позицию для наложения
    position = (0, 0)

    image.paste(frame, position, frame)
    
    image.save('result.png')
    print(f"Изображение с рамкой сохранено: {'result.png'}, {image.size}")


if __name__ == "__main__":
    main()