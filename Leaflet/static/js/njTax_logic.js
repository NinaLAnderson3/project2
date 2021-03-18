function countyDepth(tax_rate){
  return tax_rate * .2
}

// Creating map object
var myMap = L.map("map", {
  center: [40.0583, -74.4057],
  zoom: 9
 
});
function markerColor(){
  var location = L.geojson([mData.features.geomtery.coordinates[1], 
    mData.features.geomtery.coordinates[0]])
  console.log(circleLocation)
}

//Create function for color of marker
function markerColor(SummativeScore) {
  if (SummativeScore <= 45) {
      return "red";
  } else if (SummativeScore <= 55) {
      return "yellow";
  } else if (SummativeScore <= 75) {
      return "blue";
  } else if (SummativeScore <= 85) {
      return "purple";
  }  else {
      return "green";
  };
}


// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap)

// function markerColor(SummativeScore){
//   return SummativeScore*10;
// }

var layers = {
  County_Name: new L.LayerGroup(),
  Tax_rate: new L.LayerGroup(),
  School_Rating: new L.LayerGroup(),
  Crime_counts: new L.LayerGroup(),
}


var overlays = {
  "County:": layers.County_Name,
  "Tax Rate:": layers.Tax_rate,
  "School Rating": layers.School_Rating,
  "Crime Counts": layers.Crime_counts

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

//create icons
// var icons = {
//   County_Name: L.ExtraMarkers.icon({
//   icon:"ion-settings",
//   iconColor:"white",
//   markerColor: "yellow",
//   shape: "star"
// }),

// Tax_rate: L.ExtraMarkers.icon({
  
// })


// }

// Use this link to get the geojson data.
var link = "static/data/merge__nj_geojson.geojson";

var markerData = "static/data/final_nj.geojson";

d3.json(markerData, function(mData){
  // console.log(mData.features.length)
  for (var i=0; i<mData.features.length; i++) {
    var location = mData.features[i].geometry.coordinates;
    var rating = mData.features[i].properties.SummativeRating;
    // console.log(location[1], location [0]);
    console.log(rating)
    // if (location){
<<<<<<< HEAD
      L.circleColor([location[1], location[0]])
=======
      L.circleMarker([location[1], location[0]], {
        stroke: true,
        fillOpacity: 1,
        color: "black",
        fillColor: markerColor(rating),
        radius: 10})
>>>>>>> 40c9758ce8f74d7f6237b346a15d101000e67a0a
      .bindPopup("<h2>"+mData.features[i].properties.County+"</h2>"+"<br>"+"Summative Score" + 
      mData.features[i].properties.SummativeRating)
      .addTo(myMap);

    //   console.log(mData.features[i].geometry.coordinates[1], mData.features[i].geometry.coordinates[0])
    

  }



})

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  createFeatures(data.features);
  // Creating a GeoJSON layer with the retrieved data
  // console.log(data)
  geojson = L.geoJson(data, {
    style: function(features){
      return{
        color: "gray",
        fillColor: "orange",
        fillOpacity:countyDepth(features.properties.tax_rate)
      }
  }
  }).addTo(myMap);
})

// L.marker([45.52, -122.67]).addTo(myMap);
// L.marker([39.4431,-74.61701363636367])
// .bindPopup("Hi")
// .addTo(myMap)

function createFeatures(data){
  // console.log(data)
  }

