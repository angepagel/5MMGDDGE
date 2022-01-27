
# https://cairographics.org/documentation/pycairo/2/reference/context.html#cairo.Context.set_source_rgba
# 
# Une représentation "naturelle" d'une couleur est un quadruplet (R,G,B,A), où
# chaque composante (hormis la couche Alpha) est un nombre entier compris entre 0 et 255.
# 
# Pycairo lit les composantes R,G,B d'une couleur comme valeurs décimales comprises
# entre 0 et 1 : le rôle de cette fonction est de convertir une couleur exprimée en
# "RGBA classique" vers un format lisible par Pycairo (ex: [255, 204, 51, 1] -> [1, 0.8, 0.2, 1])
def rgba_to_pycairo(r, g, b, a):
    return [r/255, g/255, b/255, a]


roads = {
    # https://wiki.openstreetmap.org/wiki/Key:highway
    'default': [211, 219, 237, 1],          #d3dbed
    # ------- Roads -------
    'motorway': [233, 144, 160, 1],         #e990a0
    'trunk': [249, 178, 156, 1],            #f9b29c
    'primary': [252, 214, 164, 1],          #fcd6a4
    'secondary': [247, 250, 191, 1],        #f7fabf
    # 'tertiary': [254, 254, 254, 1],         #fefefe
    # 'unclassified': [254, 254, 254, 1],     #fefefe
    # 'residential': [254, 254, 254, 1],      #fefefe
    # ------- Link roads -------
    'motorway_link': [233, 144, 160, 1],    #e990a0
    'trunk_link': [249, 178, 156, 1],       #f9b29c
    'primary_link': [252, 214, 164, 1],     #fcd6a4
    'secondary_link': [247, 250, 191, 1],   #f7fabf
    # 'tertiary_link': [254, 254, 254, 1],    #fefefe
    # ------- Special road types -------
    # 'service': [254, 254, 254, 1],          #fefefe
    'pedestrian': [221, 221, 233, 1],       #dddde9
    # 'track': [172, 131, 39, 1],             #ac8327
    # 'road': [221, 221, 221, 1],             #dddddd
    # ------- Paths -------
    # 'footway': [255, 128, 114, 1],          #ff8072
    # 'path': [249, 152, 141, 1],             #f9988d
}

buildings = {
    # https://wiki.openstreetmap.org/wiki/Key:building
    'default': [214, 209, 200, 1],          #d6d1c8
    # ------- Accomodation -------
    'apartments': [233, 144, 160, 1],       #e990a0
    'house': [249, 178, 156, 1],            #f9b29c
    # ------- Commercial -------
    # 'commercial': [254, 254, 254, 1],       #fefefe
    # 'industrial': [254, 254, 254, 1],       #fefefe
    'office': [252, 214, 164, 1],           #fcd6a4
    'supermarket': [247, 250, 191, 1],      #f7fabf
    # ------- Religious -------
    # 'cathedral': [254, 254, 254, 1],        #fefefe
    # 'church': [254, 254, 254, 1],           #fefefe
    # 'house': [254, 254, 254, 1],            #fefefe
}

natural = {
    # https://wiki.openstreetmap.org/wiki/Key:natural
    'default': [0, 0, 0, 0],                #invisible
    # ------- Vegetation -------
    'grassland': [206, 236, 177, 1],        #ceecb1
    'heath': [214, 217, 159, 1],            #d6d99f
    'wood': [157, 202, 138, 1],             #9dca8a
    # ------- Water related -------
    'beach': [255, 241, 187, 1],            #fff1bb
    'water': [180, 208, 208, 1],            #b4d0d0
}

waterways = {
    # https://wiki.openstreetmap.org/wiki/Key:waterway
    'default': [89, 106, 212, 1],           #596ad4
    # ------- Natural watercourses -------
    'river': [171, 212, 224, 1],            #abd4e0
    # ------- Man made waterways -------
    'canal': [171, 212, 224, 1],            #abd4e0
}
