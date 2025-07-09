from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
from keyboards import main_menu

router = Router()

DB_PATH = "database/shop.db"
# region    
class CatalogState(StatesGroup):
    waiting_for_product_choice = State()
    viewing_product = State()

def get_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_products_by_category(category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products WHERE category = ?", (category,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price, image_url FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def add_to_cart(user_id, product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM cart WHERE user_id=? AND product_id=?", (user_id, product_id))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE cart SET quantity=quantity+1 WHERE user_id=? AND product_id=?", (user_id, product_id))
    else:
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", (user_id, product_id))
    conn.commit()
    conn.close()
# endregion    
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Добро пожаловать в магазин бытовой техники!\n\nВыберите действие из меню ниже 👇",
        reply_markup=main_menu
    )

@router.message(F.text == "📦 Каталог")
async def show_categories(message: Message):
    categories = get_categories()
    buttons = [
        [InlineKeyboardButton(text=cat, callback_data=f"category:{cat}")]
        for cat in categories
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите категорию товара:", reply_markup=keyboard)

@router.message(F.text == "🗑 Очистить корзину")
async def clear_cart(message: Message):
    user_id = message.from_user.id
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    await message.answer("🗑 Корзина очищена.")

@router.message(F.text == "✅ Оформить заказ")
async def checkout_handler(message: Message):
    await message.answer("✅ Заказ оформлен! Мы свяжемся с вами в ближайшее время.\n(на самом деле — нет🙂)")

@router.message(F.text == "📍 О магазине")
async def about_handler(message: Message):
    await message.answer(
        "🏪 <b>TehMag — магазин бытовой техники Биба и Боба</b>\n"
        "📍 Адрес: Пушкина, ул. Колотушкина, д. 777\n"
        "🕘 Время работы: никогда \n"
        "🚚 Доставка по всей России(но это не точно)\n"
        "📦 Более 10 000 товаров в наличии!(тоже не факт)",
        parse_mode="HTML"
    )

@router.message(F.text == "📞 Поддержка")
async def support_handler(message: Message):
    await message.answer(
        "Тут вам не момогут,уходите"
    )


@router.callback_query(F.data.startswith("category:"))
async def show_products(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("category:")[1]
    products = get_products_by_category(category)

    if not products:
        await callback.message.answer(f"В категории «{category}» пока нет товаров.")
        await callback.answer()
        return

    await state.update_data(product_list=products, category=category)

    text = f"📋 Товары в категории <b>{category}</b>:\n\n"
    for i, (prod_id, name, price) in enumerate(products, 1):
        text += f"{i}️⃣ <b>{name}</b> – {price}₽\n"

    text += "\nВведите номер товара, чтобы посмотреть подробнее."
    await callback.message.answer(text, parse_mode="HTML")
    await state.set_state(CatalogState.waiting_for_product_choice)
    await callback.answer()

@router.message(CatalogState.waiting_for_product_choice)
async def handle_product_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    product_list = data.get("product_list", [])
    category = data.get("category")

    if not message.text.isdigit():
        await message.answer("❌ Введите номер товара из списка.")
        return

    choice = int(message.text)
    if not (1 <= choice <= len(product_list)):
        await message.answer("❌ Номер товара вне диапазона.")
        return

    product_id = product_list[choice - 1][0]
    product = get_product_by_id(product_id)

    if not product:
        await message.answer("❌ Товар не найден.")
        return

    name, description, price, image_url = product

    await state.update_data(selected_product_id=product_id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_list")],
        [InlineKeyboardButton(text="➕ Добавить в корзину", callback_data="add_to_cart")]
    ])

    if image_url:
        await message.answer_photo(
            image_url,
            caption=f"<b>{name}</b>\n💰 Цена: {price}₽\n\n{description}",
            reply_markup=markup,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"<b>{name}</b>\n💰 Цена: {price}₽\n\n{description}",
            reply_markup=markup,
            parse_mode="HTML"
        )

    await state.set_state(CatalogState.viewing_product)


@router.callback_query(F.data == "back_to_list")
async def back_to_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    product_list = data.get("product_list")

    if not category or not product_list:
        await callback.message.answer("⚠️ Категория утеряна. Выберите заново.")
        await state.clear()
        return

    text = f"📋 Товары в категории <b>{category}</b>:\n\n"
    for i, (prod_id, name, price) in enumerate(product_list, 1):
        text += f"{i}️⃣ <b>{name}</b> – {price}₽\n"
    text += "\nВведите номер товара, чтобы посмотреть подробнее."

    await callback.message.answer(text, parse_mode="HTML")
    await state.set_state(CatalogState.waiting_for_product_choice)
    await callback.answer()



@router.callback_query(F.data == "add_to_cart")
async def add_selected_to_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("selected_product_id")
    category = data.get("category")
    product_list = data.get("product_list", [])
    user_id = callback.from_user.id

    if product_id is not None:
        add_to_cart(user_id, product_id)
        await callback.message.answer("✅ Товар добавлен в корзину.")
        await state.update_data(selected_product_id=product_id)
        await state.set_state(CatalogState.viewing_product)
    else:
        await callback.message.answer("❌ Ошибка: товар не выбран.")
    await callback.answer()



from aiogram.fsm.state import State, StatesGroup

class SearchState(StatesGroup):
    waiting_for_query = State()


@router.message(F.text == "🔎 Поиск")
async def ask_search_query(message: Message, state: FSMContext):
    await message.answer("🔍 Введите название или часть названия товара:")
    await state.set_state(SearchState.waiting_for_query)

@router.message(SearchState.waiting_for_query)
async def handle_search(message: Message, state: FSMContext):
    query = message.text.lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()

    if not results:
        await message.answer("❌ Ничего не найдено по запросу.")
        return

    text = "🔎 Найденные товары:\n\n"
    for i, (pid, name, price) in enumerate(results, 1):
        text += f"{i}️⃣ <b>{name}</b> – {price}₽\n"

    await message.answer(text, parse_mode="HTML")
    await state.clear()


@router.message(F.text == "🛒 Корзина")
async def show_cart(message: Message, state: FSMContext):
    await state.clear() 
    user_id = message.from_user.id
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.name, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user_id,))
    items = cursor.fetchall()
    conn.close()

    if not items:
        await message.answer("🛒 Ваша корзина пуста.")
        return

    text = "🧾 <b>Ваша корзина:</b>\n\n"
    total = 0
    for name, qty, price in items:
        text += f"• <b>{name}</b> — {qty} шт. x {price}₽ = {qty * price}₽\n"
        total += qty * price

    text += f"\n💰 <b>Итого: {total}₽</b>"

    await message.answer(text, parse_mode="HTML")


