import numpy as np
import pandas as pd
import openpyxl

url = 'https://github.com/mledoze/countries/blob/master/dist/countries.csv?raw=true'
data = pd.read_csv(url)

# 1) 10 самых маленьких и самых больших стран мира по территории
smallest_countries = data.nsmallest(10, 'area')
largest_countries = data.nlargest(10, 'area')

print("Самые маленькие страны мира:", "\n", smallest_countries.values)
print("Самые большие страны мира:", "\n", largest_countries.values)

# 2) Все франкоязычные страны мира
francophone_countries = data[data['languages'].str.contains('French', na=False)]

print("Франкоязычне страны мира:", "\n", francophone_countries.values)

# 3) Только островные государства
print("Только островные государства:")
for i in range(len(data)):
    if str(data.iloc[i]['name']).__contains__("Island"):
        print(data.iloc[i])

# 4) Все страны, находящиеся в южном полушарии
print("Все страны, находящиеся в южном полушарии:")
for i in range(len(data)):
    if float(str(data.iloc[i]['latlng']).split(',')[1]) < 0:
        print(data.iloc[i])

# Группировка стран по первой букве и территории
grouped_by_first_letter = data.groupby(data['name'].str[0])
grouped_by_area = data.groupby('area')

# Сохранение в таблицу Excel
output_columns = ['name', 'capital', 'area', 'latlng']
output_data = data[output_columns]
output_data.to_excel('countries.xlsx', index=False)