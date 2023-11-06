from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery

from keyboards.kb_utils import notification_methods_kb
from lexicon.lexicon import LEXICON

router = Router()

# Базовые команды или кнопки


@router.message(CommandStart(), StateFilter(default_state))
async def handler_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'], reply_markup=notification_methods_kb)

# Раздел с обработкой кнопок и команд для добавления напоминаний


@router.callback_query(F.data == 'add_notification', StateFilter(default_state))
async def handler_callback_add_notification_command(callback: CallbackQuery, state:FSMContext):
    await callback.message.edit_text(text=LEXICON['/add_notification'])


@router.message(Command(commands='add_notification'), StateFilter(default_state))
async def handler_add_notification_command(message: Message, state:FSMContext):
    await message.answer(text=LEXICON['/add_notification'])


# Раздел с обработкой кнопок и команд для удаления напоминаний

@router.callback_query(F.data == 'remove_notification', StateFilter(default_state))
async def handler_callback_remove_notification_command(callback: CallbackQuery, state:FSMContext):
    await callback.message.edit_text(text=LEXICON['/remove_notification'])


@router.message(Command(commands='remove_notification'), StateFilter(default_state))
async def handler_remove_notification_command(message: Message, state:FSMContext):
    await message.answer(text=LEXICON['/remove_notification'])

