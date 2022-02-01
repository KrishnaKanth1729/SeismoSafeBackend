class SeismicActivity:
    def __init__(self, time: str, lat: float, lon:float,
                magnitude: float, location: str, distance: float):
        
        self.time = time[:-4]
        self.lat = lat
        self.lon = lon
        self.magnitude = magnitude
        self.location = location
        self.distance = distance
        
        self.__str__ = self.__repr__
    
    def to_dict(self) -> dict:
        """
        Converts a <SeismicActivity> object to a python dict representation
        """
        
        return {
            "time": str(self.time[:-3]),
            "lat": self.lat,
            "lon": self.lon,
            "magnitude": self.magnitude,
            "location": self.location,
            "distance": self.distance
        }
    
    def __repr__(self) -> str:
        return f"<SeismicActivity time={self.time} lat={self.lat} \
        lon={self.lon} magnitude={self.magnitude} location={self.location}>"
    
    