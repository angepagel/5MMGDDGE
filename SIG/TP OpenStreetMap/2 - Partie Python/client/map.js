// --------------------- Définition des couches

// Routes
var roads = L.tileLayer.wms("http://localhost:4242/wms", {
    layers: 'roads',
    format: 'image/png',
    transparent: true
});

// Bâtiments
var buildings = L.tileLayer.wms("http://localhost:4242/wms", {
    layers: 'buildings',
    format: 'image/png',
    transparent: true
});

// Terrains naturels
var natural = L.tileLayer.wms("http://localhost:4242/wms", {
    layers: 'natural',
    format: 'image/png',
    transparent: true
});

// Cours d'eau
var waterways = L.tileLayer.wms("http://localhost:4242/wms", {
    layers: 'waterways',
    format: 'image/png',
    transparent: true
});

// Fond de carte
var CartoDB_Positron = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
});


// --------------------- Création et configuration de la carte

var map = L.map('map').setView([45.15, 5.75], 13); // Centré sur Grenoble

// Couche de base
var baseMaps = { "Fond de carte": CartoDB_Positron };

// Couches superposées
var overlayMaps = {
    "Routes": roads,
    "Buildings": buildings,
    "Natural": natural,
    "Waterways": waterways
};

// See https://leafletjs.com/reference.html#control-layers
L.control.layers(baseMaps, overlayMaps).addTo(map);

map.addLayer(CartoDB_Positron);
map.addLayer(natural);
map.addLayer(buildings);
map.addLayer(roads);
map.addLayer(waterways);
