import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "http://www.worldometers.info/coronavirus/#countries"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id='main_table_countries_today')
content = results.find_all('td')

content_as_list = []
for entries in content:
    content_as_list.append(entries.text.strip())

#####################################################################
# ONLY WORKS IF USA IS FIRST
counter = 0
for i in range(len(content_as_list)):
    if content_as_list[i] == '1' and content_as_list[i + 1] == 'USA':
        break
    else:
        counter = counter + 1

content_as_list = content_as_list[counter:]
#####################################################################

amt_of_countries = int(len(content_as_list) / 19)

# Initialize column titles
column_title_list = ['rank', 'country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'active_cases', 'continent']

# Initialize empty lists for df
data = []

for i in range(amt_of_countries):
    curr_country = []
    # Rank
    curr_country.append(content_as_list[(i * 19) + 0])
    # Country
    curr_country.append(content_as_list[(i * 19) + 1])
    # total_cases
    curr_country.append(content_as_list[(i * 19) + 2])
    # new_cases
    if len(content_as_list[(i * 19) + 3]) == 0:
        curr_country.append(str(0))
    else:
        curr_country.append(content_as_list[(i * 19) + 3][1:])
    # total_deaths
    if len(content_as_list[(i * 19) + 4]) == 0:
        curr_country.append(str(0))
    else:
        curr_country.append(content_as_list[(i * 19) + 4])
    # new_deaths
    if len(content_as_list[(i * 19) + 5]) == 0:
        curr_country.append(str(0))
    else:
        curr_country.append(content_as_list[(i * 19) + 5][1:])
    # active_cases
    curr_country.append(content_as_list[(i * 19) + 8])
    # continent
    curr_country.append(content_as_list[(i * 19) + 15])

    '''
    print("Rank: " + str(content_as_list[(i * 19) + 0]) + 
        "\nCountry: " + str(content_as_list[(i * 19) + 1]) +
        "\ntotal_cases: " + str(content_as_list[(i * 19) + 2]) +
        "\nnew_cases: " + str(content_as_list[(i * 19) + 3]) +
        "\ntotal_deaths: " + str(content_as_list[(i * 19) + 4]) +
        "\nnew_deaths: " + str(content_as_list[(i * 19) + 5]) +
        "\nactive_cases " + str(content_as_list[(i * 19) + 8]) +
        "\nContinent: " + str(content_as_list[(i * 19) + 15]) + "\n\n")
    '''

    data.append(curr_country)

df = pd.DataFrame(data, columns = column_title_list)

# Delete Excess
df = df.drop(df.index[[220, 221, 222, 223, 224, 225, 226, 227]])

# Save to .csv
df.to_csv('coronavirus_data.csv', index=False)