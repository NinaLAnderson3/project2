function countyDepth(tax_rate){
  return tax_rate * .2
}
// Creating map object
var myMap = L.map("map", {
  center: [40.0583, -74.4057],
  zoom: 9
 
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap)

function markerColor(SummativeScore){
  return SummativeScore*10;
}

var layers = {
  County_Name: new L.LayerGroup(),
  Tax_rate: new L.LayerGroup(),
  School_Rating: new L.LayerGroup(),
  School_Score: new L.LayerGroup()
}


var overlays = {
  "County:": layers.County_Name,
  "Tax Rate:": layers.Tax_rate,
  "School Rating": layers.School_Rating,
  "School Score": layers.School_Score

};

//create control for our layers, add overlays
L.control.layers(null,overlays).addTo(myMap)

//create a legend to display info about map
var info = L.control({
  position: "bottomright"
})

// //When the layer control is added, insert a div with the class of "legend"
info.onAdd = function(){
  var div = L.DomUtil.create("div","legend")
  return div;
};

// //add the info legend to the map
info.addTo(myMap);

// Use this link to get the geojson data.
// var link = "static/data/merge__nj_geojson.geojson";
var link = "http://data.ci.newark.nj.us/dataset/db87f66a-6d79-4933-9011-f392fdce7eb8/resource/95db8cad-3a8c-41a4-b8b1-4991990f07f3/download/njcountypolygonv2.geojson"

var markerData = "static/data/final_data.geojson";

d3.json(markerData, function(mData){
  // console.log(mData.features.length)
  for (var i=0; i<mData.features.length; i++) {
    var location = mData.features[i].geometry.coordinates;
    console.log(location[1], location [0]);
    // if (location){
      L.marker([location[1], location[0]])
      .bindPopup("<h2>"+mData.features[i].properties.County)
      .addTo(myMap);

    //   console.log(mData.features[i].geometry.coordinates[1], mData.features[i].geometry.coordinates[0])
    

  }



})

// for (var i=0; i<markers.length; i++) {
           
//   var lon = markers[i][0];
//   var lat = markers[i][1];
//   var popupText = markers[i][2];
  
//    var markerLocation = new L.LatLng(lat, lon);
//    var marker = new L.Marker(markerLocation);
//    map.addLayer(marker);

//    marker.bindPopup(popupText);
// }

// L.marker(mData.features[i].geometry.coordinates).addTo(myMap)

//add all the county markers to a new layer group
// var countyLayer = L.layerGroup(counties);

// var overlayMaps = {
//   Counties: countyLayer
// }

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  createFeatures(data.features);
  // Creating a GeoJSON layer with the retrieved data
  // console.log(data)
  geojson = L.geoJson(data, {
    style: function(features){
      return{
        color: "gray",
        fillColor: "green",
        fillOpacity:countyDepth(features.properties.tax_rate)
      }
  }
  }).addTo(myMap);
})

// L.marker([45.52, -122.67]).addTo(myMap);
L.marker([39.4431,-74.61701363636367])
.bindPopup("Hi")
.addTo(myMap)

function createFeatures(data){
  // console.log(data)
  }

