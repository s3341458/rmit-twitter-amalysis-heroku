'''
Created on 10/03/2014

@author: chengyu
'''


import os
from webPart.models import Query,Region

def populate():
    addRegion("VIC", -39.004956, -36.197002, 141.679688, 147.65625)
    addRegion("NSW", -35.5, -29.360716, 141.328125, 153.28125)
    addRegion("QUS", -28.670332, -18.56989, 138.396289, 155.720215)
    addRegion("NT",-25.667934, -10.497363, 129.462891, 138.076172)
    addRegion("WA",-35.341266, -14.973087, 113.048828, 128.847656)
    addRegion("SA",-38.00001,-26.5,130.000001,141.00001)
    addRegion("TAS", -44.003349, -40.758351, 144.84375, 148.710938)


    # Print out what we have added to the user.


def addQuery(term):
    p = Query.objects.get_or_create(searchTerm = term)[0]
    return p

def addRegion(name, latib, latit, longb ,longt ):
    c = Region.objects.get_or_create(regionName=name, latitudeBottom = latib, latitudeTop = latit , longtitudeBottom = longb, longtitudeTop = longt)[0]
    return c

# Start execution here!
if __name__ == '__main__':

    populate()
