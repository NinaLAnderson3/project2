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
    
    
  
  // Create a Darth Vader Icon
  var IconSize = mData.features[i].properties.SummativeScore
  
// Create an Icon Class TheForce
var TheForceIcon = L.Icon.extend({
  options: {
        iconSize:     IconSize,
        iconAnchor:   [40, -20],
        popupAnchor:  [-3, -76]
    }

})


// Add the Different Icons to TheForce Class
  var VaderIcon = new TheForceIcon({iconUrl: 'icon/Darth-Vader-icon.png'}),
      R2D2icon = new TheForceIcon({iconUrl: 'icon/R2D2-icon.png'}),
      AhsokaIcon = new TheForceIcon({iconUrl: 'icon/Ahsoka-Tano-icon.png'}),
      LukeIcon = new TheForceIcon({iconUrl: 'icon/Luke-Skywalker-01-icon.png'}),
      LeiaIcon = new TheForceIcon({iconUrl: 'icon/Leia-icon.png'}),
      YodaIcon = new TheForceIcon({iconUrl: 'icon/Master-Joda-icon.png'})

function SelectIcon(StarWars) {
  switch(true) {
      case (1.0 <= StarWars && StarWars <= 1.5):
          return YodaIcon;
      case (1.5 <= StarWars && StarWars<= 2.0):
        return LeiaIcon;
      case (2.0 <= StarWars && StarWars<= 2.5):
          return AhsokaIcon;
      case (3.0 <= StarWars && StarWars<= 3.5):
          return LukeIcon;
      case (3.5 <= StarWars && StarWars <= 4.0):
        return VaderIcon;
      default:
        return R2D2icon;
  }
}

// var DarthVader = L.icon({
//   iconUrl: 'icon/Darth-Vader-icon.png',
//   iconSize:     IconSize * 10, // size of the icon
//   iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
//   popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
// });
    var location = mData.features[i].geometry.coordinates;
    console.log(location[1], location [0]);
    // if (location){
      L.marker([location[1], location[0]],{icon: SelectIcon (mData.features[i].properties["2020_tax_rate"])})
      .bindPopup("<h2>"+mData.features[i].properties.County + "</h2> <h3> Summative Score " + mData.features[i].properties.SummativeScore + "</h3> <h4> Tax Rate : " + mData.features[i].properties["2020_tax_rate"] + "</h>")
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
        fillOpacity:countyDepth(features.properties.tax_rate) * 0.75
      }
  }
  }).addTo(myMap);
})


function createFeatures(data){
  // console.log(data)
  }

