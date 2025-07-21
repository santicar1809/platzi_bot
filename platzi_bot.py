from openai import OpenAI
import time
import requests
import os 
from get_updates import get_updates
from dotenv import load_dotenv


openai=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKEN = os.getenv("TOKEN")


def send_messages(chat_id,text,token):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params={"chat_id":chat_id,"text":text}
    response = requests.post(url,params=params)
    return response

def get_openai_response(prompt):
    model = 'ft:gpt-4.1-nano-2025-04-14:personal::BuVl0V67'
    system = """
    Eres un asistente de atención a cliente y 
    estudiantes de la plataforma de educación online en tecnologpia, 
    ingles y liderazgo llamada Platzi
    """
    response = openai.chat.completions.create(
        model = model,
        messages = [
            {"role":"system", "content":f'{system}'},
            {"role":"user", "content":f'{prompt}'}],
        max_tokens = 150,
        n = 1,
        temperature = 0.2
    )
    return response.choices[0].message.content.strip()

def main():
    print ('Starting bot..')
    offset = 0
    while True:
        updates = get_updates(TOKEN,offset)
        if updates:
            for update in updates:
                offset = update['update_id'] + 1
                chat_id = update['message']['chat']['id']
                user_message = update['message']['text']
                print(f"Received message: {user_message}")
                gpt_model = get_openai_response(user_message)
                send_messages(chat_id , gpt_model,TOKEN)
        else:
            time.sleep(1)
if __name__=='__main__':
    main()