#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import tiler

PORT_NUMBER = 4242


class WMSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)

            # Traiter les paramètres suivants :
            # - request (doit être égal à "GetMap")
            # - layers (le nom du calque à récupérer – c'est vous qui fixez ce nom)
            # - height (la hauteur de l'image renvoyée)
            # - width (la largeur de l'image renvoyée)
            # - srs (le système de référence spatial, EPSG:3857 dans votre cas)
            # - bbox (les coordonnées de la boîte englobante demandée, exprimées dans le SRS spécifié).
            # Si l'un de ces paramètres est manquant ou incorrect, votre serveur renverra au client un 
            # message d'erreur explicite sous forme de texte.

            # Vérifie la présence des paramètres
            required = ["request", "layers", "width", "height", "srs", "bbox"]
            for parameter in required:
                if parameter not in params:
                    return self.send_error(400, f"Paramètre '{parameter}' manquant")

            # ------- request
            request = params["request"][0]
            if request != "GetMap":
                return self.send_error(400, "Seules les requêtes 'GetMap' sont supportées")

            # ------- layers
            layers = params["layers"][0]

            # ------- width
            try:
                width = int(params.get('width')[0])
            except ValueError: # int conversion failed
                return self.send_error(400, "Le paramètre 'width' doit être un entier")

            # ------- height
            try:
                height = int(params.get('height')[0])
            except ValueError: # int conversion failed
                return self.send_error(400, "Le paramètre 'height' doit être un entier")
            
            # ------- srs, e.g. EPSG:3857
            srs = params.get('srs')[0]
            try :
                srid = int(srs.split(':')[1])
            except IndexError:
                return self.send_error(400, "Le paramètre 'srs' doit être de la forme EPSG:XXXX")
            except ValueError: # int conversion failed
                return self.send_error(400, "Le paramètre 'srs' doit être de la forme EPSG:XXXX")

            # ------- bbox [xmin, ymin, xmax, ymax]
            if len(params.get('bbox')[0].split(',')) != 4:
                return self.send_error(400, "Le paramètre 'bbox' doit être un tableau de 4 flottants")
            try:
                bbox = [float(coord) for coord in params.get('bbox')[0].split(',')]
            except ValueError:
                return self.send_error(400, "Le paramètre 'bbox' doit être un tableau de 4 flottants")

            filename = tiler.draw_tile(bbox[0], bbox[1], bbox[2], bbox[3], srid, width, height, layers)

            return self.send_png_image(filename)

        self.send_error(404, 'Fichier non trouvé : %s' % self.path)

    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def send_png_image(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
