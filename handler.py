import json
import os
import telegram
import logging


logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}

ERROR_RESOPNSE = {
    "statusCode": 400,
    "body": json.dumps('Oops, something went wrong!')
}

character_deaths = os.environ.get("CHARACTER_DEATHS")
sessions = os.environ.get('SESSIONS')

START_ANSWER = ["Hello, human! I'm a sassy bot meant to shade the fuck out of a DM who loves to murder characters :)"]
DEATH_COUNT_ANSWER = [
    "That's a very good question!",
    "So far, there have been {} character deaths.".format(character_deaths),
    "That's a heckin' lot!",
    "Specially taking into account that we're {} sessions in.".format(sessions),
    "That's a CDPS of {:0.2f}%. Deadly!".format(100 * int(character_deaths)/int(sessions))
]

EULOGY_ANSWER = [
    "Let's remember those who fought bravely and fell so that we can fight on:",
    "- Baccus Garibaldi, Banca Privada. Your moneyed ways will be forever remembered.",
    "- Kala Banca Privada. Through Hammer and Sickle, your short but sweet fight continues.",
    "- Talion. He fought bravely for Torm. Undril griefs your passing.",
    "- Albondiel Eru-Ilúvatar. Wintery asshole. Died shortly before her love.",
    "- Droplette. Died in battle fightng fiercely. Your death shall have its vengeance.",
    "- Bismarck. He was the best boy. He smiles at us from his afterlife in doggy heaven.",
    "- F for Summerwise. Our time together was short, but well spent. "
    "May you rest and meet Moonbeam Lillyfall in the endless prairies of Dragon-Heaven.\n",
    "May Othgoroth have mercy on their souls."
]


def configure_telegram():
    telegram_token = os.environ.get('TELEGRAM_TOKEN')
    if not telegram_token:
        logger.error('The TELEGRAM_TOKEN must be set.')
        raise NotImplementedError

    return telegram.Bot(telegram_token)


def hello(event, context):

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if not event.get('httpMethod') == 'POST' and event.get('body'):
        return ERROR_RESOPNSE

    try:
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        logger.info('Message received: {}'.format(update.message))

        answer = []

        if '/start' in text:
            answer = START_ANSWER

        if "I wonder how we're doing in Chult." in text:
            answer = DEATH_COUNT_ANSWER

        if "Let's remember the departed." in text:
            answer = EULOGY_ANSWER

        if answer:
            bot.sendMessage(chat_id=chat_id, text='\n'.join(answer))
            logger.info('Message sent')

    except Exception as ex:
        logging.error("{}".format(ex))

    return OK_RESPONSE
