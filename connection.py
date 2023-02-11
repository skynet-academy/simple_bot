from dotenv import load_dotenv
import os
import requests
import json
import telebot

load_dotenv()

NOTION_KEY = os.getenv("NOTION_KEY")
NOTION_BASE_URL = os.getenv("NOTION_BASE_URL")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_URL_API = os.getenv("TELEGRAM_URL_API")



def create_task(title, content):
  print(title, content)
  headers = {
          'Authorization': f'Bearer {NOTION_KEY}',
          'Content-Type': 'application/json',
          'Notion-Version': '2022-06-28'
          }
  search_params = {"filter": {"value": "page", "property": "object"}}
  search_response = requests.post(
      f'https://api.notion.com/v1/search', 
      json=search_params, headers=headers)

  search_results = search_response.json()['results']

  #page_id = search_results[0]["id"]
  page_id = NOTION_PAGE_ID

  create_page_body = {
      "parent": { "database_id": page_id },
      "properties": {
          "title": {
        "title": [{
            "type": "text",
            "text": { "content": title } }]
          }
      },
      "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{
              "type": "text",
              "text": {
                  "content": content
              }
          }]
        }
      }
    ]
  }

  create_response = requests.post(
       NOTION_BASE_URL,
       json=create_page_body, headers=headers)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
  title = message.text.split()[0]
  content = " ".join(message.text.split()[1:])

  create_task(title, content)  
  bot.send_message(chat_id='5202539966',text="recibido")
  bot.reply_to(message, message.text)

bot.infinity_polling()
