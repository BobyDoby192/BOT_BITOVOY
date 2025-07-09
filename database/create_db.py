import sqlite3

conn = sqlite3.connect("database/shop.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM products")
conn.commit()



cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL
)
""")

cursor.execute("DELETE FROM products")

products = [
    ("Холодильник Samsung RT35K5440SL", 
    "⚙️ Характеристики: No Frost, 300 л\n🛡 Гарантия: 2 года\n🌍 Страна: Южная Корея\n⚡ Энергопотребление: A++", 
    45000, "Холодильники", "https://img.mvideo.ru/Pdb/20025693b2.jpg"),

    ("Холодильник Samsung Wl48690WWW", 
    "⚙️ Характеристики: No Frost, 150 л\n🛡 Гарантия: 2 года\n🌍 Страна: Южная Корея\n⚡ Энергопотребление: A", 
    22500, "Холодильники", "https://img.mvideo.ru/Pdb/20008088b.jpg"),

    ("Стиральная машина Bosch Serie 6", 
    "⚙️ Объем: 6 кг\n🛡 Гарантия: 3 года\n🌍 Страна: Германия\n🔄 1200 об/мин", 
    29000, "Стиральные машины", "https://avatars.mds.yandex.net/i?id=f989280d51c967a04cd61aff828fe8aec3b9b100-4034573-images-thumbs&n=13"),

    ("Посудомоечная машина Whirlpool WFC 3C26", 
    "⚙️ Вместимость: 14 комплектов\n🛡 Гарантия: 2 года\n🌍 Страна: Италия\n🔄 Энергопотребление: A++", 
    33000, "Посудомоечные машины", "https://avatars.mds.yandex.net/i?id=1c29ba36c2bcc00cf79b303eb3fe517df26581d2-3917975-images-thumbs&n=13"),

    ("Электрическая плита Gorenje EIT6156AX", 
    "⚙️ Размер: 60 см\n🛡 Гарантия: 3 года\n🌍 Страна: Словения\n🔥 4 конфорки", 
    25000, "Плиты", "https://avatars.mds.yandex.net/i?id=c277d1f3bf3239c28f744363d6573ca08127284c-4017487-images-thumbs&n=13"),

    ("Кондиционер Mitsubishi Heavy SRK20ZSPR-S", 
    "⚙️ Мощность: 2 кВт\n🛡 Гарантия: 3 года\n🌍 Страна: Япония\n❄️ Инвертор", 
    45000, "Кондиционеры", "https://avatars.mds.yandex.net/i?id=ee1235184ab39f8ef91e5eb805eb7678ab185f15-4904452-images-thumbs&n=13"),

    ("Водонагреватель Electrolux EWH 50 Formax", 
    "⚙️ Объем: 50 л\n🛡 Гарантия: 2 года\n🌍 Страна: Швеция\n🔥 Мощность: 2 кВт", 
    9000, "Водонагреватели", "https://avatars.mds.yandex.net/i?id=4d8527c0f704d9082b3ddbd0f187889a0c376918-8492509-images-thumbs&n=13"),
    
    ("Пылесос Dyson V11", 
    "⚙️ Мощность: 350 Вт\n🛡 Гарантия: 1 год\n🌍 Страна: Великобритания\n💨 Циклонный фильтр", 
    32000, "Пылесосы", "https://avatars.mds.yandex.net/i?id=d537c543fb9f1fcae2518df6d5f61a664c299d8b-6338651-images-thumbs&n=13"),

    ("Микроволновая печь Panasonic NN-SN686S", 
    "⚙️ Объем: 23 л\n🛡 Гарантия: 1 год\n🌍 Страна: Япония\n⚡ Мощность: 1200 Вт", 
    8500, "Микроволновки", "https://avatars.mds.yandex.net/i?id=2fd0476e74c6585da06a7970cd3aa6ac068f5459-9181622-images-thumbs&n=13"),

    ("Кофемашина DeLonghi Magnifica", 
    "⚙️ Тип: автоматическая\n🛡 Гарантия: 2 года\n🌍 Страна: Италия\n☕ Объем: 1.8 л", 
    35000, "Кофемашины", "https://avatars.mds.yandex.net/i?id=b6676307b494a88ab2fe9e4b92004418c3fd12e7-5670683-images-thumbs&n=13"),

    ("Телевизор LG 55UN73006LA", 
    "⚙️ Характеристики: 4K UHD, Smart TV\n🛡 Гарантия: 2 года\n🌍 Страна: Корея\n📺 Матрица: IPS", 
    38000, "Телевизоры", "https://avatars.mds.yandex.net/i?id=1a481acbabed6965e80efbed16414f907022efcd-4219934-images-thumbs&n=13"),

    ("Ноутбук ASUS ROG Strix G15", 
    "⚙️ Процессор: Intel i7\n🛡 Гарантия: 2 года\n🌍 Страна: Тайвань\n💾 RAM: 16 ГБ\n📀 SSD: 512 ГБ", 
    68000, "Ноутбуки", "https://avatars.mds.yandex.net/i?id=18228ccd3b577bc369e28f84e78d6f8cd4fac15e-5232470-images-thumbs&n=13"),

    ("Фотоаппарат Canon EOS 90D", 
    "⚙️ Матрица: 32.5 Мп\n🛡 Гарантия: 1 год\n🌍 Страна: Япония\n📸 Видео 4K", 
    60000, "Фотоаппараты", "https://avatars.mds.yandex.net/i?id=68200e864f52a8c4b863469e3800c77353da70ee-5865446-images-thumbs&n=13"),

    ("Игровая приставка Sony PlayStation 5", 
    "⚙️ Хранение: 825 ГБ SSD\n🛡 Гарантия: 2 года\n🌍 Страна: Япония\n🎮 4K Gaming", 
    55000, "Игровые приставки", "https://avatars.mds.yandex.net/i?id=5157aa413c4d4394d5bf725e9a07a758181fe8ea-5874989-images-thumbs&n=13"),

    ("Смартфон Apple iPhone 14", 
    "⚙️ Дисплей: 6.1 дюйма\n🛡 Гарантия: 1 год\n🌍 Страна: Китай\n📸 Камера: 12 Мп", 
    70000, "Смартфоны", "https://avatars.mds.yandex.net/i?id=16016d623cfbcf8d8267014f9c02444027b2df02-12661511-images-thumbs&n=13"),

    ("Смарт-часы Apple Watch Series 8", 
    "⚙️ Экран: Retina\n🛡 Гарантия: 1 год\n🌍 Страна: Китай\n💧 Водонепроницаемость", 
    40000, "Смарт-часы", "https://avatars.mds.yandex.net/i?id=d4ab8330b32d0432f0d84334fb11b1fbf3942b26-5889273-images-thumbs&n=13"),

    ("Умная колонка Яндекс.Станция", 
    "⚙️ Голосовой помощник Алиса\n🛡 Гарантия: 1 год\n🌍 Страна: Россия\n🔊 Мощный звук", 
    6000, "Умная техника", "https://avatars.mds.yandex.net/i?id=1ecef9f28cf63aed3921bc74b20ec5ded9062bf3-11547032-images-thumbs&n=13"),

]

cursor.executemany("""
INSERT INTO products (name, description, price, category, image_url)
VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()
conn.close()

print("✅ База данных создана и заполнена.")
