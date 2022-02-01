import pandas as pd
from math import radians, cos, sin, asin, sqrt
from typing import List, Tuple

from .earthquake_seismic_activity import SeismicActivity


SEISMO_SAFE_DATA_CSV_FILENAME = 'C://Users/rkris/SeismoSafe/backend/seismo_safe/model/seismo_safe.csv'


def distance(lat1, lat2, lon1, lon2):

    """
    Function to calculate the distance between two places on the earth places
    using the latitude and longitude system
    """     

    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
      
    # calculate the result
    return(c * r)


class SeismoSafeModel:
    def __init__(self, lat: float, lon: float, area: int):
        
        self.lat = lat
        self.lon = lon
        self.area = area

        self.messages: List[str] = []
        self.earthquakes: List[SeismicActivity] = []

        self.setup()
        self.predict()

    def setup(self) -> None:
        self.df: pd.DataFrame = pd.read_csv(SEISMO_SAFE_DATA_CSV_FILENAME)

        self.df['Distance'] = self.df.apply(lambda x: 
            distance(x['Latitude'], self.lat, x['Longitude'], self.lon), 
            axis=1)
        
        self.df = self.df[self.df['Distance'] < self.area]
        
        # print(self.df)
    
    def predict(self) -> None:
        """
        Function to predict the Seismic activity of an area
        """

        for _, earthquake in self.df.iterrows():
            self.earthquakes.append(SeismicActivity(earthquake['Origin Time'], earthquake['Latitude'], earthquake['Longitude'], earthquake['Magnitude'], earthquake['Location'], earthquake['Distance']))

        if not len(self.df):  # No seismic activity
            self.messages.append("There is no known seismic activities near this " \
                            "location")
        else:

            major_earthquakes = self.df[self.df['Magnitude'] >= 3.5]
            close_earthquakes = self.df[self.df['Distance'] < 15]

            if len(major_earthquakes):
                self.messages.append(f"There have been {len(major_earthquakes)} " \
                                f"Major Seismic activity around this area and " \
                                f"{len(self.df) - len(major_earthquakes)} " \
                                "minor seismic activity recorded")
            else:
                self.messages.append(f"There have been {len(self.df) - len(major_earthquakes)} " \
                                "minor seismic activity recorded")

            if len(close_earthquakes):
                self.messages.append("There have been seismic activities very close " \
                                "to this location.") 
        

    def json(self):
        """
        Converts generated insights by the model into JSON
        
        ```json
        {
            "messages": [],
            "earthquakes": []
        }
        ```
        """
        return {
        "messages": self.messages,
        "earthquakes": [earthquake.to_dict() for earthquake in self.earthquakes]
    }

