import os
from PIL import Image, ImageEnhance, ImageOps

# --- НАСТРОЙКИ ---
INPUT_DIR = "raw_photos"  # Откуда брать
OUTPUT_DIR = "READY_PHOTOS_PRO"  # Куда класть (создаст новую папку)

CATEGORIES = {
    "zabory": "fence",
    "navesy": "canopy",
    "pokraska": "painting",
    "fason": "shaped_part"
}

MAX_WIDTH = 1200  # Оптимально для веба


def process_photos():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"🚀 Начинаем МАГИЮ (Улучшение фото)...")

    for folder_name, file_prefix in CATEGORIES.items():
        src_path = os.path.join(INPUT_DIR, folder_name)
        dest_path = os.path.join(OUTPUT_DIR, folder_name)

        if not os.path.exists(src_path):
            print(f"⚠️ Нет папки {src_path}, пропускаем.")
            continue

        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        files = [f for f in os.listdir(src_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        files.sort()

        print(f"\n📂 Категория: {folder_name} ({len(files)} шт.)")

        for index, filename in enumerate(files):
            try:
                img_path = os.path.join(src_path, filename)

                with Image.open(img_path) as img:
                    # 1. Поворот (если снято вертикально)
                    img = ImageOps.exif_transpose(img)

                    # 2. Ресайз (уменьшаем, если огромная)
                    if img.width > MAX_WIDTH:
                        ratio = MAX_WIDTH / float(img.width)
                        new_height = int(float(img.height) * ratio)
                        img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

                    # --- БЛОК УЛУЧШЕНИЯ (МАГИЯ) ---

                    # A. Добавляем КОНТРАСТ (делаем "глубже")
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.15)  # +15% контраста

                    # B. Добавляем НАСЫЩЕННОСТЬ (цвета сочнее)
                    enhancer = ImageEnhance.Color(img)
                    img = enhancer.enhance(1.1)  # +10% цвета

                    # C. Добавляем РЕЗКОСТЬ (чтобы металл звенел)
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.3)  # +30% резкости

                    # -----------------------------

                    # 3. Сохраняем
                    new_filename = f"{file_prefix}_{index + 1:03d}.webp"
                    save_path = os.path.join(dest_path, new_filename)

                    # Сохраняем в WebP с качеством 85 (золотая середина)
                    img.save(save_path, "WEBP", quality=85)

                    print(f"  ✨ Улучшено: {filename} -> {new_filename}")

            except Exception as e:
                print(f"  ❌ Ошибка: {filename} -> {e}")

    print(f"\n✅ Готово! Фото лежат в папке '{OUTPUT_DIR}'")


if __name__ == "__main__":
    process_photos()