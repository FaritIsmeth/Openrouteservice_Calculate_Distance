import requests
import pandas
import time

df = pandas.read_csv('[POI Collection_Maintenance]_WS_V.1_[GFG POIs Review] - Sheet39.csv',dtype=str)
#df_length = len(df)
df_length=869
get_source_coordinates={}
get_onemap_coordinates={}
counter=buffer_size=counter_iteration=0
timer=5
iteration_timer=60
api_key="5b3ce3597851110001cf62480dccb722eac64489bf31f70666586529"

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}

while counter != df_length:
    get_source_coordinates[counter] = df.at[counter, 'Source Concatenate']
    get_onemap_coordinates[counter] = df.at[counter, 'OneMap Concatenate']
    print(f'\n\nSearching row {counter+1} of {df_length}, source coordinates: {get_source_coordinates[counter]} and onemap coordinates: {get_source_coordinates[counter]} , {df_length-(counter+1)} rows left.')
    try:
        call = requests.get(f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={get_source_coordinates[counter]}&end={get_onemap_coordinates[counter]}', headers=headers)
        with open('get_address.csv','a') as myfile:
            myfile.write(f'{call.text}\n')
        print(call.status_code, call.reason)
        print(call.text)
        counter +=1
    except:
        print(f"No results found for source coordinates: {get_source_coordinates[counter]} and onemap coordinates: {get_source_coordinates[counter]}, skipping to the next row")
        with open('get_address.csv','a') as myfile:
            myfile.write(f'"Invalid"\n')
        counter += 1
    while timer !=0:
        print(f'Sleeping for {timer} seconds')
        timer -= 1
        time.sleep(1)
    print("-"*50)
    timer=5
    counter_iteration += 1
    if counter_iteration == 100:
        while iteration_timer != 0:
            print(f'100 rows done, sleeping for {iteration_timer} seconds')
            iteration_timer -= 1
            time.sleep(1)
        print("-"*50)
        counter_iteration = 0
        iteration_timer=60