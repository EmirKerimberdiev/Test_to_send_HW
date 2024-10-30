from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from bot_config import database

diolog_router = Router()
list_of_hw = []


class FINITE_STATE_MACHINE(StatesGroup):
    name = State()
    grupe = State()
    num_hw = State()
    link_to_github = State()


@diolog_router.callback_query(F.data == "add_homework")
async def review_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FINITE_STATE_MACHINE.name)
    await callback.message.answer("Введите ваше имя:")
    await callback.answer()


@diolog_router.message(FINITE_STATE_MACHINE.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FINITE_STATE_MACHINE.grupe)
    await message.answer("Введите название вашей группы")


@diolog_router.message(FINITE_STATE_MACHINE.grupe)
async def grupe_handler(message: types.Message, state: FSMContext):
    await state.update_data(grupe=message.text)
    await state.set_state(FINITE_STATE_MACHINE.num_hw)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="1"),
             types.KeyboardButton(text="2"),
             types.KeyboardButton(text="3"),
             types.KeyboardButton(text="4"),
             types.KeyboardButton(text="5"),
             types.KeyboardButton(text="6"),
             types.KeyboardButton(text="7"),
             types.KeyboardButton(text="8")]
        ],
        resize_keyboard=True
    )

    await message.answer("Введите номер домашнего задания", reply_markup=kb)


@diolog_router.message(FINITE_STATE_MACHINE.num_hw)
async def num_hw_handler(message: types.Message, state: FSMContext):
    num = int(message.text)
    if num > 8 or num < 1:
        await message.answer("Номер группы должен быть в диапазоне от 1 до 8")
        return

    await state.update_data(num_hw=message.text)
    await state.set_state(FINITE_STATE_MACHINE.link_to_github)
    await message.answer("Вставьте ссылку на GitHub репозиторий")


@diolog_router.message(FINITE_STATE_MACHINE.link_to_github)
async def link_to_github_handler(message: types.Message, state: FSMContext):
    if not message.text.startswith("https://github.com/"):
        await message.answer("Ссылка должна начинаться с https://github.com/")
        return

    await state.update_data(link_to_github=message.text)
    data = await state.get_data()
    list_of_hw.append(data)
    print(list_of_hw)

    database.execute(
        query="INSERT INTO homeworks (name, grupe, num_hw, link_to_github)"
              " VALUES (?, ?, ?, ?)",
        params=(
            data['name'],
            data['grupe'],
            data['num_hw'],
            data['link_to_github'])
    )

    await state.clear()
    await message.answer("Домашнее задание добавлено!")
