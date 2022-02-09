import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import path
from pydub import AudioSegment
import requests

URL = "http://7bde-87-200-205-229.ngrok.io"

def start(update, context):
    update.message.reply_text(
        "Bot by @Mindspire on  mindspireteam@gmail.com \n\n "
        "EN : Just send me an audio recording of anything, and we'll figure out your holistic mental state! 😏 \n"
    )


def help_command(update, context):
    update.message.reply_text('My only purpose is to tell you how you are feeling. Send a Voice Note')


def detect_mask(update, context):
    bot = context.bot
    file = bot.getFile(update.message.voice.file_id)
    file.download('voice.mp3')

    sound = AudioSegment.from_mp3('voice.mp3')
    sound.export("test.wav", format="wav")

    audio_file = open("test.wav", "rb")
    values = {"file":("test.wav", audio_file, "audio/wav")}
    response = requests.post(URL, files=values)

    data = response.json()
    update.message.reply_text(
            "EN: Looks like your PHQ9 Score is {}. I hope you don't forget it when going out!😉 \n\n".format(data['PHQ9'])
    )

def main():
    updater = Updater(token="token", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
