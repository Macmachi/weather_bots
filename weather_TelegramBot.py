#Code mis à jour la dernière fois le 06.10.2019

import requests
import time
import schedule

lastOrageUpdate = "2018-04-02T00:00:00"
lastOrageUpdate2 = "2018-04-02T00:00:00"

def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

#Pluie les prochaines 12 heures check a 6h et 18h heures !
def report12():

    app_id = ''
    city_id = ''
    api_call = 'http://api.weatherbit.io/v2.0/forecast/hourly?city_id=' + city_id + '&key=' + app_id + '&lang=fr&hours=48'

    r = requests.get(api_call)

    date = []
    description = []
    temperature = []
    precip = []
    pop = []

    data = r.json()

    #Pluie
    varPluie = "pluie"

    report12text = "Il va pleuvoir à XYZ\n\nDétails :\n\n"

    #Rempli nos listes avec les données de l'api
    for i in range(23):
        date.append(data['data'][i]['timestamp_local'])
        description.append(data['data'][i]['weather']['description'])
        temperature.append(data['data'][i]['temp'])
        precip.append(data['data'][i]['precip'])
        pop.append(data['data'][i]['pop'])

    for i in range(12):
        if varPluie in description[i] and pop[i]>50 :

                myPhrase = "{}\n{}\nProbabilité {}%\n-------------------------------------\n"
                my_message = myPhrase.format(date[i], description[i], pop[i])
                report12text += my_message

    #On vérifie que le message ne soit pas seulement celui incrémenté par défaut
    if report12text != "Il va pleuvoir à XYZ\n\nDétails :\n\n":
        telegram_bot_sendtext(report12text)

    #if report12text == "Pluie sur XYZ (12h à venir) \n\n":
        #telegram_bot_sendtext("Pas de pluie dans les 12 prochaines heures")

#Orage les prochaines 2 heures check toutes les 15 minutes !
def reportorage():

    app_id = ''
    city_id = ''
    api_call = 'http://api.weatherbit.io/v2.0/forecast/hourly?city_id=' + city_id + '&key=' + app_id + '&lang=fr&hours=48'

    r = requests.get(api_call)

    date = []
    description = []

    data = r.json()

    #Orage
    varOrage = "orage"

    global lastOrageUpdate
    global lastOrageUpdate2

    #Rempli nos listes avec les données de l'api
    for i in range(23):
        date.append(data['data'][i]['timestamp_local'])
        description.append(data['data'][i]['weather']['description'])

    #On vérifie toutes les 15 minutes si dans 2 heures orage
    reportoragetext = "Orage possible d'ici 2 heures \n\n"

    #On ne passe pas par "i" ici car on sait déjà à quel emplacement de la liste regarder.
    if lastOrageUpdate != date[2]:

        #incrémente la nouvelle date
        lastOrageUpdate = date[2]

        if varOrage in description[2]:
            myPhrase = "{}\n({})"
            my_message = myPhrase.format(description[2], date[2])
            reportoragetext += my_message
            telegram_bot_sendtext(reportoragetext)

    #On vérifie toutes les 15 minutes si dans 1 heure orage
    reportoragetext2 = "Orage possible d'ici 1 heure \n\n"

    if lastOrageUpdate2 != date[1]:

        #incrémente la nouvelle date
        lastOrageUpdate2 = date[1]

        if varOrage in description[1]:
            myPhrase = "{}\n({})"
            my_message = myPhrase.format(description[1], date[1])
            reportoragetext2 += my_message
            telegram_bot_sendtext(reportoragetext2)

#Autres (UV, températures extrêmes) vérifie chaque jour à 10 heures les informations suivantes
def reportautres():

    app_id = ''
    city_id = ''
    api_call = 'http://api.weatherbit.io/v2.0/forecast/hourly?city_id=' + city_id + '&key=' + app_id + '&lang=fr&hours=48'

    r = requests.get(api_call)

    date = []
    temperatureRessentie = []

    data = r.json()

    reporttemperaturetext = "Températures extrêmes\n\n"

    temperatureRessentie35 = False
    temperatureRessentie5 = False

    #Rempli nos listes avec les données de l'api
    for i in range(24):
        date.append(data['data'][i]['timestamp_local'])
        temperatureRessentie.append(data['data'][i]['app_temp'])
        #uv.append(data['data'][i]['uv'])

    for i in range(8):
        if 35 < temperatureRessentie[i]: #si plus de 35
            temperatureRessentie35 = True

    for i in range(24):
        if -5 > temperatureRessentie[i]: #si moins de -5
            temperatureRessentie5 = True

    #Vérification des conditions des boucles (évite d'envoyer un message à chaque range(i))
    if temperatureRessentie35 == True:
        myPhrase = "Les températures renssenties seront de plus de 35C° cette après midi. Hydratez-vous!"
        reporttemperaturetext += myPhrase
        telegram_bot_sendtext(reporttemperaturetext)
        temperatureRessentie35 = False

    if temperatureRessentie5 == True:
        myPhrase = "Les températures renssenties seront de -5C° dans les prochaines 24h. Couvrez-vous!"
        reporttemperaturetext += myPhrase
        telegram_bot_sendtext(reporttemperaturetext)
        temperatureRessentie5 = False

schedule.every().day.at("06:01").do(report12)
schedule.every().day.at("14:01").do(report12)
schedule.every(15).minutes.do(reportorage)
schedule.every().day.at("10:00").do(reportautres)

while True:
    schedule.run_pending()
    time.sleep(1)