#!/usr/bin/env python
# coding: utf-8

# Done! Congratulations on your new bot. You will find it at t.me/your_style_changer_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 1563972967:AAETCK5ET3MvxQ_tWsISwwyuTB74zMHzk0U
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api


import telebot
from transfer_model import *
import os

print(device)
bot = telebot.TeleBot('1563972967:AAETCK5ET3MvxQ_tWsISwwyuTB74zMHzk0U');


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот который поможет тебе перенести стиль с одного изображения на другое." +
                     "n\Напиши /help чтобы узнать функции")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Чтобы поменять стиль изображения, " +
                     "сначала отправь мне фото, которое нужно поменять, а потом изображение " +
                     "со стилем, который нужно применить к этмоу фото")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Привет! Я бот который поможет тебе перенести стиль с одного изображения на другое." +
                         "\nНапиши /help чтобы узнать функции")

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


images = {'content': False,
          'style': False,
          'styled_img': False}


@bot.message_handler(content_types=['photo'])
def download_photo(message):
    path = os.path.abspath(os.getcwd()).replace("\\","/") + '/img/'
    print(path)
    if not images['content']:

        content_info = bot.get_file(message.photo[-1].file_id)
        downloaded_content_file = bot.download_file(content_info.file_path)

        with open(path + str(message.chat.id) + '_cont.jpg', 'wb') as content_file:
            content_file.write(downloaded_content_file)
        images['content'] = path + str(message.chat.id) + '_cont.jpg'
        bot.reply_to(message,"Отлично, ты отправил изображение на которое я перенесу стиль." +
                     "Теперь отправь изображение с нужным стилем")
    elif not images['style']:
        style_info = bot.get_file(message.photo[-1].file_id)
        downloaded_style_file = bot.download_file(style_info.file_path)

        with open(path + str(message.chat.id) + '_style.jpg', 'wb') as style_file:
            style_file.write(downloaded_style_file)
        images['style'] = path + str(message.chat.id) + '_style.jpg'

    if images['content'] and images['style']:
        bot.reply_to(message, "Прекрасно! Начинаю обработку фото...\nЭто займет время")
        content_img = image_loader(images['content'])
        style_img = image_loader(images['style'])
        input_img = content_img.clone()

        styled_img = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                                        content_img, style_img, input_img)
        styled_img.save(path + str(message.chat.id) + '_styled.jpg')
        images['styled_img'] = path + str(message.chat.id) + '_styled.jpg'

        with open(path + str(message.chat.id) + '_styled.jpg', 'rb') as f:
            bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, "Готово!")

        for key, item in images.items():
            if images[key]:
                os.remove(item)
                images[key] = False


bot.polling(none_stop=True, interval=0)
