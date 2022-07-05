
import logging
import wikipedia

from aiogram import Bot, Dispatcher , executor ,types




logging.basicConfig(level=logging.INFO)

API_TOKEN='API_KEY'

wikipedia.set_lang('uz')


bot=Bot(token=API_TOKEN)
dp =Dispatcher(bot)


@dp.message_handler(commands=['start' ,'boshlash'])
async def send_welcome(message:types.Message):
    await message.reply(f" Assalomu alaykum {message.from_user.first_name} botimizga xush kelibsiz!")



@dp.message_handler()
async def wiki(message:types.Message):
    try:
        qidirish=wikipedia.search(message.text)
        malumot=wikipedia.summary(message.text)
        await message.reply(qidirish)
        await message.reply(malumot)
        
    except:
        await message.reply(message.text ," bo'yicha natija topilmadi")
    
    
         
    





    if __name__ == "__main__":
            executor.start_polling(dp , skip_updates=True)
