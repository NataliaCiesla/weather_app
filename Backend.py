import requests
import pandas as pd
#pip install install unidecode
from unidecode import unidecode
from translate import Translator
from datetime import datetime

# 1 Prepare variables
api_key="b10622bddd0d43cb8c291459240903"
#city="Barcelona"
#city=input("Enter the city to get weather data from: ")#zmienna ktora zawiera polskie znaki
#city_unidecoded= unidecode(city) #zmienna ktora nie zawiera polskich znakow,bedzie sluzyladokomunikacji api bez polskich znakow
#url=f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_unidecoded}&aqi=yes"
#2 Connect to API

while True:
    city=input("Enter the city to get weather data from: ")
    city_unidecoded=unidecode(city)
    url=f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_unidecoded}&aqi=yes"
    try:
        response=requests.get(url) #get=select
        if response.status_code == 200:
            response = response.json()
            break
        else:
            if response.status_code == 400:
        #print("")
                print("Error! Invalid city input.Try again.")
        #exit()
    except:
        print("Unable to connect to Api.")
        exit()


menu_message=f"Select what ypu want to display for {city}: " \
                  "\n1) Temperature" \
                  "\n2) Pressure" \
                  "\n3) Humidity" \
                  "\n4) All above" \
                  "\n Your choice : "

#user_choice=int(input(menu_message))
#while user_choice>4 or user_choice<1:
    #print("Invalid value")
 #   print(f"{user_choice} is not supported option.")
  #  user_choice = int(input(menu_message))

while True:
    try:
        user_choice=int(input(menu_message))
    #if user_choice>0 and user_choice<5:
      #  break
    #jezeli uzytkownik wpisze liczbe z zakresu 1-4
        if 0 < user_choice < 5:
            break #wychodzimy z petli nieskonczonosci
        else:
            print(f"\n{user_choice} is not supported option. Try again")
    except ValueError:
        print("\nInvalid input. Try again.")

    #if user_choice>4 or user_choice<1:
        #print(f"\n{user_choice} is not supported option. Try again")
        #user_choice=int(input((menu_message)))

# 2 Connect to API
response=requests.get(url) #get=select
#print(response.status_code)

#if response.status_code==200:
  #  response=response.json()
#else:
#    if response.status_code==400:
 #   print("Error! Invalid city input.")
 #   exit()

response=response.json()#json-konwerstuje odwoedz z serwera nan strukture ktora bedzie przyjazna dla pythona


#  3 Prepare variables with weather information
temp_c=response['current']['temp_c']
pressure=response['current']['pressure_mb']
humidity=response['current']['humidity']

#4 Display general weather overview message
translator=Translator(to_lang='pl')
weather_text=response['current']["condition"]['text']
weather_text_pl=translator.translate(weather_text)

#print(f"Weather overview: {response['current']['condition']['text']}")
print(f'Weather overview: {weather_text} (PL:{translator.translate(weather_text)})')

#5 Prepare function to display emojis

def display_weather_icon(temp):
    if temp_c > 15:
        print("🌞")
    elif temp_c <= 0:
        print("❄️")
    elif 15 > temp_c > 0:
        print("⛅")
# 6 Display weather data based on the user input
if user_choice==1:
    display_weather_icon(temp=temp_c)
    print(f"Temperature dor{city} is: {response['current']['temp_c']} C degrees.")
elif user_choice==2:
    print(f"Pressure for {city} is: {response['current']['pressure_mb']} mb.")
elif user_choice==3:
    print(f"Humidity for {city} is: {response['current']['humidity']}%")
elif user_choice==4:
    display_weather_icon(temp=temp_c)
    print(f"Temperature for {city} is: {temp_c}°C degrees.")
    print(f"Pressure for {city} is: {pressure} mb")
    print(f"Humidity for {city} is: {humidity}%")
else:
    print("Invalid data.")


#7 Save weather data to file

#Prepare date

current_date = datetime.now()

data={'Miasto': city,
      'Temperatura (C)': temp_c,
      'Wilgotnosc': humidity,
      'Stan pogodowy': weather_text_pl,
      'Data': current_date.strftime('%Y-%m-%d %H:%M')
      }

#Create pandas dataframe
df = pd.DataFrame([data])
#Prepare data
#current_date=datetime.now().strftime('%y%m%d')

#Save data to excelfile
excel_filemane=f'dane_pogoda_{city.lower()}_{current_date.strftime("%Y%m%d")}.xlsx'#lower() zmienia nazwe miasto namale litery
#print(df)
df.to_excel(excel_filemane,index=False,engine='openpyxl')