
// Store API link
var url = "static/data/merge__nj_geojson.geojson"
var markerData = "static/data/final_data.geojson"




// // function circleSize(mag) {
//   return mag * 40000;
// }

function circleColor(){
  var location = L.geoJSON(mData)
  console.log(location)
}

function circleColor(SummativeScore) {
  if (SummativeScore <= 25) {
      return "red";
  } else if (SummativeScore <= 50) {
      return "green";
  } else if (SummativeScore <= 60) {
      return "yellow";
  } else if (SummativeScore <= 75) {
      return "orange";
  } else if (SummativeScore <= 90) {
      return "red"
  } else {
      return "purple";
  };
}



function createMap(njCounties) {

    // Define satelitemap and light map layers
    var satelitemap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.satellite",
      accessToken: API_KEY
    });
  
    var light = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "light-v10",
    accessToken: API_KEY
  });

  var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
    tileSize: 512,
    maxZoom: 18,
    zoomOffset: -1,
    id: "mapbox/streets-v11",
    accessToken: API_KEY
});
  
    // Define a baseMaps object to hold our base layers
    var baseMaps = {
      "Satelite Map": satelitemap,
      "Light Map": light,
      "Street Map": streetmap
    };
  
    // create layers
    var techPlates = new L.layerGroup();
    var NewnjCounties = new L.layerGroup();
  
  
  
    // Create our map, giving it the satelitemap and njCounties layers to display on load
    var myMap = L.map("map", {
      center: [40.7128, -74.0060],
      zoom: 3,
      layers: [satelitemap, light, streetmap]
    });
    satelitemap.addTo(myMap);
    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
//     L.control.layers(baseMaps, overlayMaps, {
//       collapsed: false
//     }).addTo(myMap);
//   njCounties.addTo(NewnjCounties)
//   NewnjCounties.addTo(myMap)
  
      //perform a GET request to te github tectonic URL
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
      });
  
  } //end of create map function
  
  // Perform a GET request to the USGS URL
  // d3.json(url, function(data) {
  //     // Once we get a response, send the data.features object to the createFeatures function
  //     createFeatures(data.features);
  //   });
    
  function createFeatures(earthquakeData) {
    console.log(earthquakeData);
    var njCounties = L.geoJSON(earthquakeData, {
      // Define a function we want to run once for each feature in the features array
      // Give each feature a popup describing the place and time of the earthquake
     onEachFeature : function (feature, layer) {
    
        layer.bindPopup("<h3>" + feature.properties.place +
          "</h3><hr><p>" + new Date(feature.properties.time) + "</p>" + "<p> Magnitude: " +  feature.properties.mag + "</p>")
        },     pointToLayer: function (feature, latlng) {
          return new L.circle(latlng,
            {radius: circleSize(feature.properties.mag),
            fillColor: circleColor(feature.properties.mag),
            fillOpacity: depthColor(feature.geometry.coordinates[2]),
            stroke: false
        })
      }
      });
      // Sending our njCounties layer to the createMap function
      createMap(njCounties);
    }
  
  