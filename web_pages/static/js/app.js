 
const createMap = ((paEvents) => {
  
    // Create the tile layer that will be the background of our map.
    var streetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    // Create a baseMaps object to hold the streetmap layer.
    var baseMaps = {
        "Street Map": streetmap
    };

    // Create an overlayMaps object to hold the bikeStations layer.
    var overlayMaps = {
        "Paranormal Activity": paEvents
    };

    // Create the map object with options.
    var map = L.map("map-id", {
        center: [40.73, -74.0059],
        zoom: 7,
        layers: [streetmap, paEvents]
    });
       
    // Create a layer control, and pass it baseMaps and overlayMaps. Add the layer control to the map.
    L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
    }).addTo(map);
})

const createMarkers = ((paType) => {

    d3.json(`/api/paranormal/activityType/${paType}`).then((data) => {
        // Pull the "stations" property from response.data.
        var allActivity = data;

        // Initialize an array to hold bike markers.
        var paMarkers = [];

        // Loop through the stations array.
        for (var index = 0; index < allActivity.length; index++) {
            var activity = allActivity[index];

            // For each station, create a marker, and bind a popup with the station's name.
            var paMarker = L.marker([activity.Latitude, activity.Longitude])
                .bindPopup("<h3>" + activity.Title);

            // Add the marker to the bikeMarkers array.
            paMarkers.push(paMarker);
        }

        // Create a layer group that's made from the bike markers array, and pass it to the createMap function.
        createMap(L.layerGroup(paMarkers));
    })
})
      ////////////////////
  
const buildDirectorChart = ((director) => {
  
    console.log(director);
  
    d3.json(`api/directors/${director}`).then((data) => {
  
      console.log(data)
    
      var trace1 = {
        type: 'bar',
        x: data['labels'],
        y: data['scores'],
        marker: {
            color: '#C8A2C8',
        }
      };
      
      var data = [ trace1 ];
      
      var layout = { 
        title: 'Directors',
      };
      
      var config = {responsive: true}
      
      Plotly.newPlot('v-bar', data, layout, config );
    
    })
})
  
  
const optionTypeChanged = ((newType) => {
    createMarkers(newType);
})
  
createMarkers("Amazing")
  
//buildDirectorChart("chaplin")
  
  
  