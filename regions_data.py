import requests


def get_data_regions():
    array = {}
    url = 'https://coronavirus-monitor.info/country/russia/'
    page = requests.get(url)
    text = page.text
    left_border = text.find('Смертей')
    right_border = text.find('Показать все')
    text = text[left_border:right_border].split('\n')[5:-3]

    for i in range(0, len(text), 9):
        current_city = text[i + 1][text[i + 1].find('data-region="') + len('data-region="'):
                                   text[i + 1].find('" class')]

        array[current_city] = {}

        current_text = text[i + 2]
        data_confirmed = current_text[current_text.find('data-confirmed="') + len('data-confirmed="'):
                                      current_text.find('" class')]
        array[current_city]['data_confirmed'] = int(data_confirmed)

        if current_text.find('xs"><sup>+') != -1:
            data__today_confirmed = current_text[current_text.find('xs"><sup>+') + len('xs"><sup>+'):
                                                 current_text.find('</sup></div>')]
            array[current_city]['data_today_confirmed'] = int(data__today_confirmed)
        else:
            array[current_city]['data_today_confirmed'] = '-'

        current_text = text[i + 3]
        data_cured = current_text[current_text.find('data-cured="') + len('data-cured="'):
                                  current_text.find('" class')]
        array[current_city]['data_cured'] = int(data_cured)

        if current_text.find('xs"><sup>+') != -1:
            data_today_cured = current_text[current_text.find('xs"><sup>+') + len('xs"><sup>+'):
                                            current_text.find('</sup></div>')]
            array[current_city]['data_today_cured'] = int(data_today_cured)
        else:
            array[current_city]['data_today_cured'] = '-'

        current_text = text[i + 4]
        data_deaths = current_text[current_text.find('data-deaths="') + len('data-deaths="'):
                                   current_text.find('" class')]
        array[current_city]['data_deaths'] = int(data_deaths)

        if current_text.find('xs"><sup>+') != -1:
            data_today_deaths = current_text[current_text.find('xs"><sup>+') + len('xs"><sup>+'):
                                             current_text.find('</sup></div>')]
            array[current_city]['data_today_deaths'] = int(data_today_deaths)
        else:
            array[current_city]['data_today_deaths'] = '-'

        data_deaths_pros = text[i + 5][text[i + 5].find('cell">') + len('cell">'):
                                       text[i + 5].find('</div>')]
        array[current_city]['data_deaths_pros'] = data_deaths_pros
    return array
