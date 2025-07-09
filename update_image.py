import sqlite3

conn = sqlite3.connect("database/shop.db")
cursor = conn.cursor()

# Пример: обновим ссылку на изображение у товара с ID = 1
cursor.execute("""
UPDATE products
SET image_url = ?
WHERE id = ?
""", ("https://cdn1.ozone.ru/s3/multimedia-1-5/7087348841.jpg", 2))

conn.commit()
conn.close()

print("✅ Ссылка обновлена.")
