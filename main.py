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

    frame = load_image(frame_path)
    if frame is None:
        return

    # Вычисляем координаты для вставки изображения в рамку
    x_offset = (frame.width - image.width) // 2
    y_offset = (frame.height - image.height) // 2

    frame.paste(image, (x_offset, y_offset))

    result_path = "result.png"
    frame.save(result_path)
    print(f"Изображение с рамкой сохранено: {result_path}")


if __name__ == "__main__":
    main()