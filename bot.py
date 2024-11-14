import telebot
import os
import pdfplumber
from googletrans import Translator
from PyPDF2 import PdfReader

API_TOKEN = '7318947115:AAEsdjUjSuVI_mhB8Tmhn-qWQ3iUsbamrXM'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        file = bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = bot.download_file(file_path)

        with open("downloaded_file.pdf", 'wb') as f:
            f.write(downloaded_file)

        translator = Translator()
        with pdfplumber.open('downloaded_file.pdf') as pdf:
            translated_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                translated_text += translator.translate(text, src='auto', dest='ar').text
        
        bot.reply_to(message, translated_text[:4000])

@bot.message_handler(content_types=['document'])
def convert_office_files(message):
    if message.document.mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        bot.reply_to(message, "تم استلام ملف Word.")
    elif message.document.mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        bot.reply_to(message, "تم استلام ملف Excel.")

@bot.message_handler(content_types=['document'])
def read_pdf_and_generate_questions(message):
    if message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        file = bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = bot.download_file(file_path)

        with open("downloaded_file.pdf", 'wb') as f:
            f.write(downloaded_file)

        with pdfplumber.open('downloaded_file.pdf') as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        questions = "سؤال 1: ... \nسؤال 2: ..."
        bot.reply_to(message, questions)

@bot.message_handler(content_types=['document'])
def summarize_pdf(message):
    if message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        file = bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = bot.download_file(file_path)

        with open("downloaded_file.pdf", 'wb') as f:
            f.write(downloaded_file)

        with pdfplumber.open('downloaded_file.pdf') as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        summary = text[:1000]
        bot.reply_to(message, summary)

bot.polling()