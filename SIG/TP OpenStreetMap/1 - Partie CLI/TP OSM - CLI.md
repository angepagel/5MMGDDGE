| William LIN | Ange PAGEL | Nelson PEREIRA | Jia YAN | Yin XU |
| ----------- | ---------- | -------------- | ------- | ------ |

# TP OpenStreetMap (Partie CLI)

`10 Janvier 2022` `Ensimag 5MMGDDGE` `Systèmes d'Information Géographique`

[TOC]

## Connexion à la base et premières requêtes

### Connexion à la base avec le client psql

**Question 1 :** Pour vérifier que vous avez bien accès aux tables en interrogation, effectuez une requête pour compter le nombre de nœuds pour les données de la région Rhône-Alpes (= nombre de tuples de la relation `nodes`).

> ```sql
> SELECT COUNT(*) FROM nodes;
> ```
> 
> [Résultat de la requête Q1](resultats/q1.txt)

### Interrogation de base

**Question 2.a :** Quelles sont ses coordonnées géographiques ?

*Indication :* Vous pouvez jeter un coup d'œil sur les fonctions d'accès aux informations géométriques de PostGIS, ici : [ http://postgis.net/docs/manual-2.0/reference.html#Geometry_Accessors](http://postgis.net/docs/manual-2.0/reference.html#Geometry_Accessors)

> ```sql
> SELECT ST_AsText(geom) FROM nodes WHERE id=26686589;
> ```
> 
> [Résultat de la requête Q2](resultats/q2.txt)

**Question 2.b :** Dans quel système de référence ces coordonnées sont-elles exprimées ?

*Indication :* La table `spatial_ref_sys ` contient toutes les informations concernant les systèmes de référence supportés par PostGIS, référencés par SRID (identifiant), et avec une description textuelle de ces systèmes de référence.

> En observant la description de la table nodes à l'aide de la commande `\d nodes`, on remarque que le type de la colonne geom est geometry(Point, 4326). On recherche alors le tuple dont le srid est 4326 dans la table spatial_ref_sys :
>
> ```sql
> SELECT * FROM spatial_ref_sys WHERE srid=4326;
> ```
>
> On observe dans la colonne srtext que le système de référence associé à l’ESPG 4326 est le **WGS84** (https://epsg.io/4326).

### Interrogation attributaire

**Question 3 :** Quelles sont les coordonnées géographiques du centroïde de la mairie de Meylan (la mairie est un chemin qui contient l'attribut `amenity='townhall'` et dont le nom contient « Meylan ».

> ```sql
> SELECT ST_AsText(St_Centroid(linestring)) FROM ways
> WHERE tags->'amenity' = 'townhall'
> 	AND upper(tags->'name') LIKE '%MEYLAN%';
> ```
> 
> [Résultat de la requête Q3](resultats/q3.txt)

**Question 4 :** Compter le nombre de routes (chemins contenant la clé `highway`) par type (par valeur de l'attribut `highway`), ordonné par ordre décroissant.

> ```sql
> SELECT
> 	tags->'highway' AS type,
> 	COUNT(*) as nombre
> FROM ways WHERE tags?'highway'
> GROUP BY tags->'highway' ORDER BY nombre DESC;
> ```
> 
> [Résultat de la requête Q4](resultats/q4.txt)

### Fonctions de mesure

**Question 5.a :** Même question que précédemment (question 4), mais au lieu de compter les routes, affichez leur longueur.

> ```sql
> SELECT
> 	tags->'highway' AS Highway,
> 	SUM(ST_Length(linestring)) AS len
> FROM ways WHERE tags ? 'highway'
> GROUP BY tags->'highway' ORDER BY len DESC;
> ```
> 
> [Résultat de la requête Q5a](resultats/q5a.txt)

**Question 5.b :** En quelle unité cette longueur est-elle exprimée ?

> Cette longueur est exprimée en degrés du SRS WGS 84 (https://epsg.io/4326).

**Question 5.c :** Même question, mais avec toutes les longueurs converties dans le système métrique (km si possible).

> ```sql
> SELECT 
> 	tags->'highway' AS Highway,
> 	SUM(ST_Length(linestring::geography))/1000 AS length
> FROM ways WHERE tags ? 'highway'
> GROUP BY tags->'highway' ORDER BY length DESC;
> ```
> 
> [Résultat de la requête Q5c](resultats/q5c.txt)
> 
> *Note : On divise par 1000 pour avoir les valeurs en kilomètres.*

**Question 6 :** Quelle est l'aire totale des bâtiments l'Ensimag en m² ?

> ```sql
> SELECT
> 	tags->'name' AS nom,
> 	ST_Area(ST_MakePolygon(linestring)::geography) AS metrescarre
> FROM ways WHERE UPPER(tags->'operator') LIKE '%ENSIMAG%';
> ```
>
> [Résultat de la requête Q6 (1)](resultats/q6-1.txt)
> 
> On remarque que le bâtiment H est présent deux fois ; en réalité, les données cartographiques d’OpenStreetMap considèrent le bâtiment H en deux parties, avec d’un côté le RDC, et de l’autre les étages 1 & 2 (qui couvrent la surface du « préau » du RDC).
>
> On calcule l’aire totale des bâtiments de l’Ensimag en m² :
>
> ```sql
> SELECT
> 	SUM(ST_Area(ST_MakePolygon(linestring)::geography)) AS airetotale
> FROM ways WHERE UPPER(tags->'operator') LIKE '%ENSIMAG%';
> ```
>
> [Résultat de la requête Q6 (2)](resultats/q6-2.txt)

### Intersections, etc.

**Question 7 :** Affichez l'ensemble des quartiers de Grenoble, avec, pour chaque quartier, le nombre d'écoles (`amenity='school'`) qu'il contient, le tout ordonné par nombre d'écoles décroissant.

*Indication :* Vous vous appuierez sur les données de la table `quartier ` pour récupérer les contours des quartiers, et sur la table `ways` (données OpenStreetMap) pour les écoles. Vous avez bien sûr une fonction pour faire l'intersection de deux polygones dans PostGIS.

> ```sql
> SELECT
> 	q.quartier,
> 	COUNT(*) AS ecoles
> FROM ways w
> 	INNER JOIN quartier q ON ST_Intersects(ST_Transform(q.geom,4326), w.linestring)
> WHERE w.tags->'amenity' = 'school'
> GROUP BY q.quartier ORDER BY ecoles DESC;
> ```
>
> [Résultat de la requête Q7](resultats/q7.txt)

### Requêtes spatiales hardcore (bonus)

**Question 8 :** Centre géographique de la région Rhône-Alpes. Quelle municipalité (ville, village) constitue le centre géographique de la région ?

*Indications :*

- Vous pouvez interpréter cette notion de centre géographique comme bon vous semble. Une manière possible est de considérer qu'il s'agit de la ville dont la distance maximale aux autres villes est minimale (en d'autres termes, dont la ville la plus éloignée de la région est la moins loin possible).
- Une municipalité est une relation possédant les tags `boundary='administrative'` et `admin_level='8'`.

> Sélectionne l’ensemble des municipalités :
>
> ```sql
> SELECT * FROM relations
> WHERE tags->'boundary' = 'administrative'
> 	AND tags->'admin_level' = '8';
> ```
>
> `Non terminé`

**Question 9 :** Déserts de population. Vous voulez partir en vacances tranquillement. Existe-t-il un endroit en région Rhône-Alpes éloigné de plus de 10 kilomètres d'un bâtiment ?

> `Non terminé`