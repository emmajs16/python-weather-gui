# GUI setup
try:
##     for Python2
  from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

window = Tk()
window.title("Weather Or Not")
window.geometry('800x800')
window.configure(background='#e5c3c6', cursor = "umbrella")

# API setup
import json
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# title label and label position
title = Label(window, text="Weather Or Not", font=("BodoniSvtyTwoOSITCTT-Bold", 50),bg='#e5c3c6') #attributes include text and font, and font size
title.grid(column=1, row=0, columnspan=1)

#city label
city_label = Label(window, text="City:", font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6') #attributes include text and font, and font size
city_label.grid(column=0, row=2)

# city input
city = Entry(window,width=15)
city.grid(column=0, row=3)
city.configure(font=("BodoniSvtyTwoOSITCTT-Book", 20))

#state label
state_label = Label(window, text="State:", font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6') #attributes include text and font, and font size
state_label.grid(column=2, row=2)

# state input
state = Entry(window,width=15)
state.grid(column=2, row=3)
state.configure(font=("BodoniSvtyTwoOSITCTT-Book", 20))

# activity label
activity_label = Label(window, text="What are your plans for today?", font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6') #attributes include text and font, and font size
activity_label.grid(column=1, row=4)
# activity input
selected_activity = IntVar()
rad1 = Radiobutton(window,text='Relax', value=1, variable=selected_activity,bg='#e5c3c6')
rad2 = Radiobutton(window,text="Exercise", value=2, variable=selected_activity,bg='#e5c3c6')
rad3 = Radiobutton(window,text='School', value=3, variable=selected_activity,bg='#e5c3c6')
rad4 = Radiobutton(window,text='Work', value=4, variable=selected_activity,bg='#e5c3c6')
rad1.grid(column=0, row=5)
rad2.grid(column=2, row=5)
rad3.grid(column=0, row=6)
rad4.grid(column=2, row=6)
# temperature label
temp_label = Label(window, font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6')#attributes include text and font, and font size
temp_label.grid(column=0, row=8,columnspan=3)
# interest suggestion label
suggestion_label =  Label(window, font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6')
suggestion_label.grid(column=0, row=9,columnspan=3)
# recommendation label
recommendation_label =  Label(window, font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6')
recommendation_label.grid(column=0, row=10,columnspan=3)
# Previously searched cities list
previous_cities_label =  Label(window, font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6',text= "Previously Searched Cities:")
previous_cities_label.grid(column=0, row=12,columnspan=3)


# FUNCTION
previously_searched_cities = []
def clicked():
    # get the city and state search results from the user input field
    city_search = city.get()
    state_search = state.get()
    url = urlopen("https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{}%2C%20{}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys".format(city_search.replace(" ",""),state_search.replace(" ","")))
    result = dict(json.load(url))
    temperature = int(result.get('query').get('results').get('channel').get('item').get('condition').get('temp'))
    condition = result.get('query').get('results').get('channel').get('item').get('condition').get('text')
    temp_label.configure(text="It is {} degrees and {} in {}".format(temperature,condition.lower(),city.get().capitalize()))
    
    if city_search not in previously_searched_cities:
        previously_searched_cities.append(city_search)
    
    # if the temp is less than 45 wear a coat
    if temperature <= 45:
        recommendation_label.configure(text="You should wear a coat today!")
    # if it's raining outside bring an umbrella
    if condition == "rain" or condition == "thunderstorms":
        recommendation_label.configure(text="You should bring an umbrella today!")      
    # good weather
    good_weather = True
    if condition == "rain" or condition == "snow" or condition == "thunderstorms" or temperature <= 45:
        good_weather = False
    # if the weather is good, don't display any clothing recommendations
    else:
        recommendation_label.configure(text="")
        
        
    # ACTIVITY RECOMMENDATIONS
    activity = selected_activity.get()
    if activity == 1:
        # relax
        if good_weather:
            suggestion_label.configure(text="It's a beautiful day to go outside and relax!")
        else:
            suggestion_label.configure(text="Today is a good day to relax inside!")           
    elif activity == 2:
        # exercise
        if good_weather:
            suggestion_label.configure(text="Today is a good day to exercise outside!")
        else:
            suggestion_label.configure(text="It might be better to exercise inside today.")
    elif activity == 3:
        # school
        if good_weather:
            suggestion_label.configure(text="You could walk to class today!")
        else:
            suggestion_label.configure(text="Luckily, you aren't missing out on a pretty day by being at school.")
    elif activity == 4:
        # work
        if good_weather:
            suggestion_label.configure(text="It's a great day to be outside after work!")
        else:
            suggestion_label.configure(text="Luckily, you aren't missing out on a pretty day by working inside.")
            
    # Display previously searched cities
    for i in range(0,len(previously_searched_cities)):
        city_text = previously_searched_cities[i].capitalize()
        previous_cities_label =  Label(window, font=("BodoniSvtyTwoOSITCTT-Bold", 25),bg='#e5c3c6',text= city_text)
        previous_cities_label.grid(column=0, row=13+i,columnspan=3)


# create button
btn = Button(window, text="Enter", font=("BodoniSvtyTwoOSITCTT-Bold", 25),command=clicked)
btn.grid(column=1, row=7)

