from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from aiogram.fsm.state import any_state

router = Router()


@router.message(StateFilter(any_state))
async def handler_unknown(message: Message):
    await message.answer(LEXICON['unknown'])
