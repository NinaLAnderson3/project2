d3.json("api/leaflet_data", function(err,rows){
    if (err) throw err;
    console.log(rows);
} )