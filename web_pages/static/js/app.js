var map = null;

function createMap(paEvents){
  
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
    if (map != undefined){
        map.remove();
    }
    // Create the map object with options.
    map = L.map("map-id", {
        //center: [39.13080446469668, -94.74259079416709],
        center: [40.730610, -73.935242],
        zoom: 3,
        layers: [streetmap, paEvents]
    });
       
    // Create a layer control, and pass it baseMaps and overlayMaps. Add the layer control to the map.
    L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
    }).addTo(map);
}

function createMarkers(paType){

    d3.json(`/api/paranormal/activityType/${paType}`).then((data) => {
        // Pull the "stations" property from response.data.
        var allActivity = data;

        // Initialize an array to hold bike markers.
        var paMarkers = [];        

        // Loop through the stations array.
        for (var index = 0; index < allActivity.length; index++) {
            var activity = allActivity[index];

            var selectColor = activity.Type == 'Amazing' ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png' : activity.Type == 'Big foot' 
                ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png' : activity.Type == 'Haunted' ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png'
                : 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png'
            var selectedIcon = new L.Icon({
                iconUrl: `${selectColor}`,
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
              });

            // For each station, create a marker, and bind a popup with the station's name.
            var paMarker = L.marker([activity.Latitude, activity.Longitude], {icon: selectedIcon})
                .bindPopup(activity.Type + "<br>" + activity.Title + "<br>" + (activity.City ? activity.City : '') + "<br>" + (activity.State ? activity.State : ''));
            // Add the marker to the bikeMarkers array.
            paMarkers.push(paMarker);
        }

        // Create a layer group that's made from the bike markers array, and pass it to the createMap function.
        createMap(L.layerGroup(paMarkers));
    })
}
      ////////////////////
  
function buildBarChart(){
    d3.json(`/api/paranormal/totals`).then((data) => {
    
      var trace1 = {
        type: 'bar',
        x: data['Labels'],
        y: data['Totals'],
        marker: {
            color: '#C8A2C8',
        }
      };
      
      var data = [ trace1 ];
      
      var layout = { 
        title: 'Paranormal Activity',
      };
      
      var config = {responsive: true}
      
      Plotly.newPlot('v-bar', data, layout, config );
    
    })
}
 
function buildPieChart(){
    d3.json(`/api/paranormal/totals`).then((data) => {

    var data = [{
        values: data['Totals'],
        labels: data['Labels'],
        type: 'pie'
      }];
      
      var layout = {
        height: 400,
        width: 500
      };
      
      Plotly.newPlot('pie', data, layout);
   
    })
}

  
function optionTypeChanged(newType){
    createMarkers(newType);
}
  
createMarkers("All")
buildBarChart()
buildPieChart()  
  
  