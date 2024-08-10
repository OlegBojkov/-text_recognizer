
from PIL import Image, ImageDraw, ImageFont

original_image = Image.open('letter_recognition/image.png')
font_path = 'letter_recognition/ofont.ru_Celestina.ttf'

# Текст для добавления
text = "охраняться"

color = (0, 0, 0)

# Максимальная ширина текста - ширина изображения
max_width = original_image.width

# Ищем максимальный размер шрифта, чтобы текст вписался в ширину изображения
font_size = 1
font = ImageFont.truetype(font_path, font_size)
image = original_image.copy()
draw = ImageDraw.Draw(image)
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]

while text_width < max_width:
    font_size += 1
    font = ImageFont.truetype(font_path, font_size)
    image = original_image.copy()
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

# Находим последний размер шрифта, который вписывается в ширину
font_size -= 1
font = ImageFont.truetype(font_path, font_size)
image = original_image.copy()
draw = ImageDraw.Draw(image)
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Позиция для добавления текста (центрирование)
position = ((original_image.width - text_width) // 2, (original_image.height - text_height) // 2)

# Добавление текста и сохранение изображений по одной букве
current_text = ""
prev_bbox_right = 0  # Начальная позиция конца предыдущей буквы
for i, char in enumerate(text):
    current_text += char
    
    # Вычисление ширины текста до текущего символа
    bbox = draw.textbbox((0, 0), current_text, font=font)
    curr_bbox_right = bbox[2]  # Конец текущей буквы
    
    # Вычисление границ для обрезки изображения
    left = max(0, prev_bbox_right - 10)  # Конец предыдущей буквы минус 10 пикселей, но не меньше 0
    right = min(original_image.width, curr_bbox_right + 10)  # Конец текущей буквы плюс 10 пикселей, но не больше ширины изображения
    
    # Обрезка изображения
    cropped_image = original_image.crop((left, 0, right, original_image.height))
    
    # Конвертация обрезанного изображения в RGB перед сохранением
    cropped_image = cropped_image.convert('RGB')
    
    # Сохранение обрезанного изображения
    output_path = f'letter_recognition/output_image_{i+1}.jpg'
    cropped_image.save(output_path)
    print(f"Часть изображения успешно сохранена как '{output_path}'!")
    
    # Обновление позиции конца предыдущей буквы
    prev_bbox_right = curr_bbox_right

print("Все изображения успешно сохранены!")