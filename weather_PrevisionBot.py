#Code mis à jour la dernière fois le 06.10.2019
#Prévision météo des 48H prochaines 

import requests

def get_data():

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

    for i in range(48):
        date.append(data['data'][i]['timestamp_local'])
        description.append(data['data'][i]['weather']['description'])
        temperature.append(data['data'][i]['temp'])
        precip.append(data['data'][i]['precip'])
        pop.append(data['data'][i]['pop'])

    print('{:^25}{:^20}{:^20}{:^20}{:^20}'.format("Date", "Description", "Température", "Précipitation accumulée (mm)","Probalitités (%)\n"))
    for i in range(48):
        print('{:^25}{:^20}{:^20}{:^20}{:^20}'.format(str(date[i]), description[i], temperature[i], precip[i], pop[i]))


get_data()