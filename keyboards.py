from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📦 Каталог"),
            KeyboardButton(text="🔎 Поиск")
        ],
        [
            KeyboardButton(text="🛒 Корзина"),
            KeyboardButton(text="🗑 Очистить корзину"),
            KeyboardButton(text="✅ Оформить заказ")
        ],
        [
            KeyboardButton(text="📍 О магазине"),
            KeyboardButton(text="📞 Поддержка")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие из меню ↓"
)
