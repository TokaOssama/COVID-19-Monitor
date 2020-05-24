import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
# POST to API
payload = {'country': 'Italy'}
URL = 'https://api.statworx.com/covid'
response = requests.request("POST", url=URL, data=json.dumps(payload))

# Convert to data frame
df = pd.DataFrame.from_dict(json.loads(response.text))
# print(df.info())
# print(df.head())
# print(df["cases_cum"])

fig = plt.figure(figsize= (8, 6))
plt.plot(df["cases_cum"], 'bo')
fig.suptitle("Country: Italy")
plt.xlabel("Number of days since 1/1/2020")
plt.ylabel("Number of cases")
plt.show()

# url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"
#
# headers = {
#     'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
#     'x-rapidapi-key': "b6096bb964msh0f75e8faa61784cp10b2d6jsn0f3e403692d3"
#     }
#
# response = requests.request("GET", url, headers=headers)
#
# df = pd.DataFrame.from_dict(json.loads(response.text))
# print(df.info())
#
# print(df['countries_stat'])
# filter_by_country = {}
# for dict in df['countries_stat']:
#     if dict['country_name'] not in filter_by_country:
#         filter_by_country[dict['country_name']] = dict
#
# print(filter_by_country['Egypt'])
