import pandas as pd
import requests

# base uri for the api request 
base_uri = "https://swapi.dev/api/"

# make the api request for
responce = requests.get(base_uri).json()

def starwars_data():
    # request data
    people = requests.get(responce['people']).json()
    planets = requests.get(responce['planets']).json()
    starships = requests.get(responce['starships']).json()

    # make a dataframe of the results
    people_df = pd.DataFrame(people["results"])
    planets_df = pd.DataFrame(planets["results"])
    starships_df = pd.DataFrame(starships["results"])

    # add every person raw to the people df
    while people["next"] != None:
        people = requests.get(people["next"]).json()
        people_df = pd.concat([people_df, pd.DataFrame(people["results"])]).reset_index(drop=True)
                
    # add every person raw to the people df
    while planets["next"] != None:
        planets = requests.get(planets["next"]).json()
        planets_df = pd.concat([planets_df, pd.DataFrame(planets["results"])]).reset_index(drop=True)

    # add every person raw to the people df
    while starships["next"] != None:
        starships = requests.get(starships["next"]).json()
        starships_df = pd.concat([starships_df, pd.DataFrame(starships["results"])]).reset_index(drop=True)
            
    # merge the three dataframes
    star_plan = pd.merge(left=planets_df, right=planets_df, how="left", on="url")
    starwars = pd.merge(left=star_plan, right=people_df, how="inner", left_on="url", right_on="homeworld")

    # save to csv
    starwars.to_csv("./starwar.csv")

    return starwars
        
