import os
import datetime
import random

def handle_uploaded_file(file):
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(f"random_digits: {random_digits}")
    # Получение имени файла и его расширения
    file_name, file_extension = file.name.rsplit('.', 1)
    if file_extension.lower() not in ['jpg', 'jpeg', 'png', 'webp']:
        return False
    # Создание нового имени файла с 6 случайными цифрами
    new_file_name = f"{file_name}_{random_digits}.{file_extension}"
    print(f"new_file_name: {new_file_name}")
    file_path = 'uploads/' + new_file_name

    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return new_file_name
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return False
