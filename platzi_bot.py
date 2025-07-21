from openai import OpenAI
import time
import requests
import os 
from get_updates import get_updates
from dotenv import load_dotenv


openai=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKEN = os.getenv("TOKEN")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")


def send_messages(chat_id,text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params={"chat_id":chat_id,"text":text}
    response = requests.post(url,params=params)
    return response

async def handle_message(data):
    try:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # Llama a OpenAI
        system = """
    Eres un asistente de atención a cliente y 
    estudiantes de la plataforma de educación online en tecnologpia, 
    ingles y liderazgo llamada Platzi
    """
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages = [
            {"role":"system", "content":f'{system}'},
            {"role":"user", "content":f'{text}'}],
        max_tokens = 150,
        n = 1,
        temperature = 0.2
    
        )
        answer = response.choices[0].message.content.strip()
        send_messages(chat_id, answer)

    except Exception as e:
        print("Error procesando mensaje:", e)


def get_openai_response(prompt):
    model = OPENAI_MODEL
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
#if __name__=='__main__':
#    main()