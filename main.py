import json

from dateutil import parser
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
from tg_botting.bot import Bot

bot = Bot([''])

group_types = ['month', 'day', 'hour']


async def show_error(message):
    await bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                           text='Невалидный запос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')


@bot.listen()
async def on_ready():
    global db, collection
    client = MongoClient("mongodb://swht.su:27017")
    db = client["mydatabase"]
    collection = db["work"]

    print('bot is start')


@bot.listen()
async def on_message_new(message):
    text = message.text.replace('\'', '\"')
    if not text.startswith('{') or not text.endswith('}'):
        return await show_error(message)
    try:
        obj = json.loads(text)
    except Exception:
        return await show_error(message)

    if 'dt_from' not in obj or 'dt_upto' not in obj or 'group_type' not in obj:
        return await show_error(message)

    try:
        datetime_from = parser.parse(obj['dt_from'])
        datetime_to = parser.parse(obj['dt_upto'])
    except Exception:
        return await show_error(message)

    if obj['group_type'] not in group_types:
        lines = ['Допустимо отправлять только следующие запросы:']
        for type in group_types:
            obj['group_type'] = type
            lines.append(str(obj))
        return await bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                      text='\n'.join(lines))
    if obj["group_type"] == "month":
        group_period = relativedelta(months=1)
    elif obj["group_type"] == "day":
        group_period = relativedelta(days=1)
    else:
        group_period = relativedelta(hours=1)

    dataset = []
    labels = []
    current_date = datetime_from
    next_date = current_date + group_period
    while current_date < datetime_to:
        query = {
            "dt": {"$gte": current_date, "$lt": next_date}
        }
        result = collection.aggregate([
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": "$value"}}}
        ])
        total_value = list(result)[0]["total"] if result.alive else 0
        dataset.append(total_value)
        labels.append(current_date.isoformat())
        current_date = next_date
        next_date = current_date + group_period

    while current_date <= datetime_to:
        dataset.append(0)
        labels.append(current_date.isoformat())
        current_date = current_date + group_period

    t = {"dataset": dataset, "labels": labels}
    await bot.send_message(chat_id=message.chat.id,text=str(t).replace('\'','\"'))

bot.run('6301358766:AAEFkRyrHidca-_s1s_mu27QANkPMNJompU')
