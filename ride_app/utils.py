import math

def distance_km(lat1, lng1, lat2, lng2):

    R = 6371.0  

    p = math.pi / 180.0

    dlat = (lat2 - lat1) * p

    dlng = (lng2 - lng1) * p

    a = (math.sin(dlat/2)**2) + math.cos(lat1*p) * math.cos(lat2*p) * (math.sin(dlng/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


# this calculates the distance b/w 2 location in kilometer
# utils.py is a reusable helper function