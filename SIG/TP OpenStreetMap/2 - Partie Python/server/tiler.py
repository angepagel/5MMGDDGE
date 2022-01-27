import os, drawer, database as db
import tiler_colors as colors

# Liste des couches supportées par la fonction draw_tile
supported_layers = {
    # Layer name : associated OSM key
    'roads'      : 'highway',
    'buildings'  : 'building',
    'natural'    : 'natural',
    'waterways'  : 'waterway',
}

def draw_tile(x0, y0, x1, y1, srid, width, height, layer):
    """Génère une tuile représentant les éléments d'une couche donnée dans une région donnée.

    Args:
        x0, y0, x1, y1 (float): Coordonnées de la boîte englobante dans le SRS spécifié
        srid (id): Identifiant du SRS dans lequel sont exprimées les coordonnées de la boîte englobante
        width (int): Largeur de la tuile en pixels
        height (int): Hauteur de la tuile en pixels
        layer (string): Nom de la couche dessinée (voir la liste des couches supportées)

    Returns:
        string: Chemin relatif de la tuile générée (fichier au format PNG)
    """

    # ------- PREPARE --------

    # La couche demandée est-elle supportée par le programme ?
    if layer not in supported_layers:
        return None
    
    # Détermine le chemin et le nom du fichier à créer
    dir = f'tiles/{layer}'
    os.makedirs(dir, exist_ok=True)
    filepath = f"{dir}/{x0}-{y0}-{x1}-{y1}-{layer}.png"

    # La tuile est-elle déjà en cache ?
    if os.path.exists(filepath):
        return filepath

    # ------- MATH MAGIC --------

    # Pour former une jolie tuile, on doit projeter les coordonnées (exprimées dans un SRS
    # défini) sur l'image, composée de pixels ; pour ce faire, on applique successivement
    # deux transformations linéaires à l'ensemble des points :

    # - Une translation, qui ramène l'origine (x0,y0) de la boîte englobante (ex. 5.7, 45.1, ESPG:4326)
    #   à l'origine de l'image (0,0) ;
    translation =  [-x0, -y0]
    def translate(point):
        point.x = point.x + translation[0]
        point.y = point.y + translation[1]
        return point

    # - Une homothétie, qui met à l'échelle (agrandit ou rétrécit) toutes les distances pour qu'elles
    #   deviennent cohérentes avec les dimensions de l'image (il s'agira ici de calculer le rapport 
    #   entre l'image et la boîte englobante).
    #   Note : Si le rapport largeur/longueur de l'image et de la boîte englobante
    #   sont différents, il s'agira en réalité d'une dilatation.
    homothety = [width / abs(x1 - x0), height / abs(y1 - y0)]
    def homothetize(point):
        point.x = point.x * homothety[0]
        point.y = point.y * homothety[1]
        return point

    # (+) Pycairo considère l'origine de l'image dans le coin supérieur gauche : on inverse l'axe Y,
    #     sinon la tuile est retournée ¯\_( ͡° ͜ʖ ͡°)_/¯
    def invert_y(point):
        point.y =  height - point.y
        return point

    # On applique les transformations sur chaque point de la géométrie
    def transform(linestring):
        for point in linestring:
            point = invert_y(homothetize(translate(point)))
        return linestring


    # ------- QUERY --------

    # Représentation en Well-Known-Text (WKT) de la région à visualiser
    wkt = f"POLYGON(({x0} {y0}, {x1} {y0}, {x1} {y1}, {x0} {y1}, {x0} {y0}))"
    # Création de la géométrie et conversion vers l'EPSG:4326 utilisé par la base de données
    container = f"ST_Transform(ST_GeomFromText('{wkt}', {srid}), 4326)"

    # Noter la reconversion de la géométrie vers le SRS d'origine : les vecteurs
    # de translation et d'homothétie on été calculés en utilisant les coordonnées
    # dans le SRS d'origine, et n'auraient plus de sens dans le SRS 4326
    cursor = db.execute_query(f"\
        SELECT\
            ST_Transform(linestring, {srid}),\
            tags->'{supported_layers[layer]}'\
        FROM ways\
        WHERE tags?'{supported_layers[layer]}'\
            AND ST_Contains({container}, linestring);")


    # ------- RENDER --------

    tile = drawer.Image(width, height)
    for row in cursor:
        linestring = row[0]
        type = row[1]
        
        # Chaque point (coordonnées dans un SRS) est projeté sur l'image (matrice de pixels)
        points = transform(linestring)

        # Routes et chemins
        if layer == 'roads':
            road_stroke = colors.roads['default']
            if type in colors.roads:
                road_stroke = colors.roads[type]
            tile.draw_linestring(points, colors.rgba_to_pycairo(*road_stroke))

        # Bâtiments
        elif layer == 'buildings':
            building_fill = colors.buildings['default']
            building_stroke = [0,0,0,0] # no stroke
            if type in colors.buildings:
                building_fill = colors.buildings[type]
            tile.draw_polygon(points, building_stroke, colors.rgba_to_pycairo(*building_fill))

        # Éléments naturels
        elif layer == 'natural':
            natural_fill = colors.natural['default']
            natural_stroke = [0,0,0,0] # no stroke
            if type in colors.natural:
                natural_fill = colors.natural[type]
            tile.draw_polygon(points, natural_stroke, colors.rgba_to_pycairo(*natural_fill))

        # Cours d'eau
        elif layer == 'waterways':
            waterway_stroke = colors.waterways['default']
            if type in colors.waterways:
                waterway_stroke = colors.waterways[type]
            tile.draw_linestring(transform(linestring), colors.rgba_to_pycairo(*waterway_stroke))

    cursor.close()
    db.close_connection()

    tile.save(filepath)
    return filepath


# ------- Question 11 --------
# Écrivez la fonction demandée, ainsi qu'un petit programme qui la teste sur la boîte englobantede longitudes
# comprises entre 5.7 et 5.8, et latitudes comprises entre 45.1 et 45.2, dans le système WGS84.

# draw_tile(5.7, 45.1, 5.8, 45.2, 4326, 256, 256, 'roads')
