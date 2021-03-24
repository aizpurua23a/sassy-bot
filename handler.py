import json
import os
import telegram
import logging
from random import randint


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
    "- F for Summerwise. Our time together was short, but well spent."
    "May you rest and meet Moonbeam Lillyfall in the endless prairies of Dragon-Heaven.",
    "- Tom Bombadol. He bewitched us all with his music, but in the end he couldn't resist the power of his spells.",
    "- Vom. He kidnapped our hearts and our druid and left. Your shady ass will always be remembered.",
    "- Merion el Sibilino. He was too wise for hiw own good. We hope for his quick escape from Virion's evil hands.",
    "- Saska. The world wasn't ready for a nice yuan-ti ready to look for a cure. We'll cry your loss.",
    "- Kurk. Tom could not eat your soul. We'll try and bring you back to life. For Valkur.\n",

    "May Othgoroth have mercy on their souls."
]

FENTHAZA_ANSWER = ["Do you mean \"Té-en-taza\"?"]

TE_EN_TAZA_ANSWER = ["Give me a wisdom saving throw!"]

GORRITI_ANSWER = ["Did you ever hear the tragedy of Gorriti the town? I thought not. It’s not a story Bob's followers would tell you. Its a story Tim will absolutely tell you..."]

TREN_EXCUSAS_ANSWER = ["Choo Chooooo!"]

HELP_ANSWER = [
    "The following commands are known:",
    "---------------------------------",
    "/help ups!, you are already here, help command.",
    "/r {number_of_dice}d{type_of_dice} {+/-} {int} for letting me roll for you.",
    "r/ is for reddit, not for here.\n",
    "The following strings are answered if found within the message text:",
    "---------------------------------",
    "[I wonder how we're doing in Chult.] Numbers of how many characters has Xabi killed in this campaign.",
    "[Let's remember the departed.] List of all people Xabi has killed.",
    "[Fenthaza] I think this is a typo.",
    "[Té-en-taza] / [Te-en-taza] How you dare? Are you trying to infuriate Xabi?",
    "[Gorriti] Tim is having a nightmare!"
    "[El tren de las excusas] Choo choo!"
]


def configure_telegram():
    telegram_token = os.environ.get('TELEGRAM_TOKEN')
    if not telegram_token:
        logger.error('The TELEGRAM_TOKEN must be set.')
        raise NotImplementedError

    return telegram.Bot(telegram_token)


def get_dice_roll_result(text):
    number_of_dice, type_of_dice = text.replace(' ', '').split('d')
    type_of_dice = type_of_dice.split('+')[0].split('-')[0]

    sum = 0
    for _ in range(int(number_of_dice)):
        sum += randint(1, int(type_of_dice))

    if '+' in text:
        return [str(sum + int(text.split('+')[1]))]

    if '-' in text:
        return [str(sum - int(text.split('-')[1]))]

    return [str(sum)]


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

        if '/r' in text[:2]:
            answer = get_dice_roll_result(text[2:])

        if '/help' in text[:2]:
            answer = HELP_ANSWER

        if "I wonder how we're doing in Chult." in text:
            answer = DEATH_COUNT_ANSWER

        if "Let's remember the departed." in text:
            answer = EULOGY_ANSWER

        if "Fenthaza" in text:
            answer = FENTHAZA_ANSWER

        if "Té-en-taza" in text or "Te-en-taza" in text:
            answer = TE_EN_TAZA_ANSWER
        
        if "Gorriti" in text:
            answer = GORRITI_ANSWER
            
        if "tren" in text or "excusas" in text:
            answer = TREN_EXCUSAS_ANSWER

        if answer:
            bot.sendMessage(chat_id=chat_id, text='\n'.join(answer))
            logger.info('Message sent')

    except Exception as ex:
        logging.error("{}".format(ex))

    return OK_RESPONSE
