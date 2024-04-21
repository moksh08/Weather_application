from django.shortcuts import render
import json 
import urllib.request 
from .models import SearchHistory

def index(request): 
    data = {}
    
    if request.method == 'POST': 
        city = request.POST.get('city', '')
        
        # Ensure there are no spaces in the API URL
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=09ff8ca7b02f5718a4dd67b3a99f6dff'

        try:
            # Fetch data from the API
            source = urllib.request.urlopen(url).read() 
            # Convert JSON data to a dictionary 
            list_of_data = json.loads(source) 
            
            # Extract required data from the dictionary 
            data = { 
                "city": city,
                "country_code": str(list_of_data['sys']['country']), 
                "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']), 
                "temp": str(list_of_data['main']['temp']) + 'k', 
                "pressure": str(list_of_data['main']['pressure']), 
                "humidity": str(list_of_data['main']['humidity']), 
            } 
            
            # Save the search history
            SearchHistory.objects.create(
                city=city,
                country_code=data["country_code"],
                coordinate=data["coordinate"],
                temperature=data["temp"],
                pressure=data["pressure"],
                humidity=data["humidity"]
            )
            
        except Exception as e: 
            print(f'An error occurred: {e}') 
    
    # Retrieve all search history entries
    search_history = SearchHistory.objects.all().order_by('-timestamp')
    
    # Pass the search history to the template
    return render(request, "app/index.html", {"data": data, "search_history": search_history})
