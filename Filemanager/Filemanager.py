import telebot
import json
from telebot.types import Message
import yadisk
import os


token="<BOT_TOKEN>"

y=yadisk.Client(token="<YADISK_TOKEN>")

bot = telebot.TeleBot(token)

def main():
	pass

@bot.message_handler(content_types=['document'])
def handle_docs(message):
	folder = '/' + message.chat.title + '/'
	file_info = bot.get_file(message.document.file_id)
	file_name = message.document.file_name
	downloaded_file = bot.download_file(file_info.file_path)
	storage = "<SERVER_STORAGE_PATH>" + file_name
	destination = dest(folder, file_name)

	with open(storage, 'wb') as temp:
		temp.write(downloaded_file)
	with open(storage, 'rb') as final:
		y.upload(final, destination)

	os.remove(storage)


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
	folder = '/' + message.chat.title + '/'
	file_info = bot.get_file(message.photo[-1].file_id)
	file_name = file_info.file_path.strip()
	if '/' in file_name:
		file_name = file_name.split('/')[-1]

	downloaded_photo = bot.download_file(file_info.file_path)
	storage = "<SERVER_STORAGE_PATH>" + file_name
	destination = dest(folder, file_name)

	with open(storage, 'wb') as temp:
		temp.write(downloaded_photo)
	with open(storage, 'rb') as final:
		y.upload(final, destination)

	os.remove(storage)


def dest(folder, file_name):
	if y.exists(folder):
		destination = folder + file_name
		if y.exists(destination):
			i = 1
			name, extention = file_name.split('.')
			while y.exists(destination):
				file_name = name + '(' + str(i) + ').' + extention
				destination = folder + file_name
				i += 1
	else:
		y.mkdir(folder)
		destination = folder + file_name

	return destination


def handler(event, _):
	message = telebot.types.Update.de_json(event['body'])
	bot.process_new_updates([message])
	return {
        'statusCode': 200,
        'body': '!',
    }



if __name__ == '__main__':
    bot.infinity_polling()