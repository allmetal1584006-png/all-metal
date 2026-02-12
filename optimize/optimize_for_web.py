import os
from PIL import Image, ImageOps

# --- НАСТРОЙКИ ---
INPUT_DIR = "input"  # Папка с исходниками (с логотипом Gemini)
OUTPUT_DIR = "optimized"  # Папка для готовых чистых фото
MAX_WIDTH = 1920  # Максимальная ширина (Full HD)
QUALITY = 85  # Качество WebP

# --- НАСТРОЙКИ ОБРЕЗКИ (Подбери под размер логотипа!) ---
# Сколько пикселей срезать с правого края
CROP_RIGHT = 250
# Сколько пикселей срезать с нижнего края
CROP_BOTTOM = 100
# Включить обрезку? (Поставь False, если не нужно обрезать)
ENABLE_CROP = True


def optimize_and_crop_images():
    # Создаем папки
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"📁 Создана папка '{INPUT_DIR}'. Положи туда фото с логотипами!")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    if not files:
        print(f"⚠️ Папка '{INPUT_DIR}' пуста.")
        return

    print(f"🚀 Найдено {len(files)} файлов. Начинаем обрезку и оптимизацию...")
    print("-" * 40)

    for filename in files:
        try:
            input_path = os.path.join(INPUT_DIR, filename)
            # Меняем расширение на .webp для выходного файла
            file_root, _ = os.path.splitext(filename)
            output_filename = f"{file_root}.webp"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with Image.open(input_path) as img:
                # 1. Исправляем поворот (на всякий случай)
                img = ImageOps.exif_transpose(img)

                # 2. Конвертируем в RGB (для надежности)
                img = img.convert("RGB")

                current_w, current_h = img.size

                # === БЛОК ОБРЕЗКИ (CROPPING) ===
                if ENABLE_CROP:
                    # Вычисляем новые границы
                    # (лево, верх, право, низ)
                    new_right = current_w - CROP_RIGHT
                    new_bottom = current_h - CROP_BOTTOM

                    # Проверка, чтобы не обрезать картинку в минус, если она маленькая
                    if new_right > 0 and new_bottom > 0:
                        # Сама обрезка
                        img = img.crop((0, 0, new_right, new_bottom))
                        print(f"  ✂️ Обрезано: -{CROP_RIGHT}px справа, -{CROP_BOTTOM}px снизу.")
                    else:
                        print("  ⚠️ Картинка слишком мала для такой обрезки, пропускаем кроп.")
                # ===============================

                # 3. Ресайз (если после обрезки она всё ещё огромная)
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    print(f"  📉 Ресайз до ширины {MAX_WIDTH}px")

                # 4. Сохраняем в WebP
                img.save(output_path, "WEBP", quality=QUALITY)

            print(f"✅ Готово: {output_filename}")

        except Exception as e:
            print(f"❌ Ошибка с {filename}: {e}")

    print("-" * 40)
    print(f"🎉 Все фото обработаны и лежат в папке '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    optimize_and_crop_images()