import json
from datetime import datetime

def suffix(d):
    return 'th' if 11<=d<=13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d%10, 'th')
def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

# абсолютная ссылка для картинок
pic_path="https://pics.khabaroff.com/_telega/"

# result.json отдает телеграм
with open('result.json') as json_file:
    data = json.load(json_file)

    for m in data['messages']:

        id_ = m['id']

        date_ = m['date']
        date_short = date_[:10]
        dateFormatted = custom_strftime('%B {S}, %Y', datetime.strptime(date_short, '%Y-%m-%d'))

        # перевод дат с https://medium.com/geekculture/import-your-todoist-tasks-nto-roam-research-fa364050f32d
        
        result = "[[" + dateFormatted + "]]" + '\n [[телеграм]]\n\n'

        message = m['text']

        if 'forwarded_from' in m:
            result += 'Перепост из "' + m['forwarded_from'] + '"\n\n'

        if type(message) == str:
            result = message
        else:
            for i in range(len(message)):

                if type(message[i]) == str:
                    result += message[i]
                else:
                    if 'text' in message[i]:
                        result += message[i]['text']

        if 'photo' in m:
            pic_url = "![](" + pic_path + m['photo'] + ")"
            result += pic_url

        f = open('Телеграм – ' + str(id_) + ".md", "w+")
        f.write(result)
        f.close()
