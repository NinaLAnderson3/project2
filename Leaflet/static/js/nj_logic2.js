// Store API link
var link = "static/data/merge__nj_geojson.geojson"

var schoolData = "static/data/final_data.geojson"

var myMap = L.map("map", {
    center: [40.0583, -74.4057],
    zoom: 9
   
  });

function countyDepth(tax_rate){
  return tax_rate * .2
}

function markerColor(){
    var location = L.geoJSON(markerData)
    console.log(location)
  }

  function markerColor(SummativeScore) {
    if (SummativeScore <= 30) {
        return "white";
    } else if (SummativeScore <= 45) {
        return "green";
    } else if (SummativeScore <= 60) {
        return "yellow";
    } else if (SummativeScore <= 75) {
        return "orange";
    } else if (SummativeScore <= 95) {
        return "red"
    } else {
        return "purple";
    };
  }

  L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap)

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

  

  function createFeatures(markerColor){
      console.log(markerColor);
      var schoolInfo = L.geoJSON(markerColor,{
          onEachFeature : function(feature, layer){
              layer.bindPopup("hi" + mData)
          }
      })
  }

  function createFeatures(data){
    // console.log(data)
    }