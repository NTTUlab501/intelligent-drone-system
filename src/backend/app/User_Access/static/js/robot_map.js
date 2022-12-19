let markers = [];
let uluru = { lat: 0, lng: 0 };
let map;
let scopes = [];
let paths = [];
let center_marker;
let robot_marker;
/*
let scope = [
    { lat: uluru.lat - 1 / 111 / 2, lng: uluru.lng - 0.01 / 2},
    { lat: uluru.lat - 1 / 111 / 2, lng: uluru.lng + 0.01 / 2},
    { lat: uluru.lat + 1 / 111 / 2, lng: uluru.lng + 0.01 / 2},
    { lat: uluru.lat + 1 / 111 / 2, lng: uluru.lng - 0.01 / 2}
]
*/

function initMap() {
    navigator.geolocation.watchPosition((position) => {
        uluru.lat = position.coords.latitude;
        uluru.lng = position.coords.longitude;

        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 16,
            center: uluru,
            scaleControl: true,
            mapTypeControl: false,
            zoomControl: false,
            streetViewControl: false,
            fullscreenControl: false
        });

        center_marker = new google.maps.Marker({
            position: uluru,
            map: map
        });

        map.addListener("click", (mapsMouseEvent) => {
            center_marker.setMap(null);
            center_marker = new google.maps.Marker({
                position: mapsMouseEvent.latLng,
                map: map
            });
          });
    });
    

    

    

    //let bermudaTriangle = new google.maps.Polygon({
    //    path: scope,
    //    strokeColor: '#f1c40f', // 線條顏色
    //    strokeOpacity: 0.8, // 線條透明度
    //    strokeWeight: 5, // 線條粗度
    //    fillColor: '#f1c40f', // 多邊形裡填滿的顏色
    //    fillOpacity: 0.24 // 多邊形裡，填滿顏色的透明度
    //});
    //bermudaTriangle.setMap(map);
    

}

/*
function initMap() {
    navigator.geolocation.watchPosition((position) => {
        uluru.lat = position.coords.latitude;
        uluru.lng = position.coords.longitude;

        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 16,
            center: uluru,
            scaleControl: true,
            mapTypeControl: false,
            zoomControl: false,
            streetViewControl: false,
            fullscreenControl: false
        });

        //center_marker = new google.maps.Marker({
        //    position: uluru,
        //    map: map
        //});
    });
}  
*/
function renew(robots) {
    $.each(markers, function (idx, marker) {
        marker.marker.setMap(null);
    });
    markers.length = 0;
    $.each(robots.UAV, function (idx, UAV) {
        marker = new google.maps.Marker({
            position: UAV.position_GPS,
            map: map
        });
        let infow = new google.maps.InfoWindow({
            content: 'UAV' + UAV.ID
        });
        //infow.open(map, marker);
        marker.addListener('click', () => infow.open(map, marker));
        markers.push({ 'marker': marker, 'infow': infow });
    });
}

function renew_one(robot) {
    if(robot_marker)robot_marker.setMap(null);

    robot.position_GPS = uluru;
    //console.log(robot.position_GPS);
    robot_marker = new google.maps.Marker({
        position: robot.position_GPS,
        map: map
    });

}