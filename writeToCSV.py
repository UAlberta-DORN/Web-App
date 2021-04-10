import csv, requests, json

csvFilePath = r'graphData.csv'
basePath = 'http://127.0.0.1:80/'

#csv_header = ['Date', 'Time', 'currentTemperature', 'currentLighting', 'referenceTemperature', 'referenceLighting', 'manualHeaterControl', 'manualHeaterValue', 'manualBlindControl', 'manualHeightValue', 'manualTiltValue', 'currentHeaterValue', 'currentHeightValue', 'currentTiltValue']
#Default Row:
csv_row = ['2021-02-10', '12:00', '20', '20', '20', '20', 'False', 'False', 'False', '20', '20', 'False', '20', '20']


#During operation, save data to csv file once a minute
Date = '2021-02-10' #Placeholder
csv_row[0] = Date
Time = '12:00' #Placeholder
csv_row[1] = Time

#Get values from API
path = basePath + 'dorn/all'
data = requests.get(path).json()
i = 0
while i < 12:
    csv_row[i+2] = data[i]['value']
    i += 1

#Add row to csv file
with open(csvFilePath, 'a+', encoding='utf-8', newline='') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(csv_row)

