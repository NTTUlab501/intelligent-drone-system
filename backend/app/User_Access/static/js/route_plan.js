let colors = ['#FF0000', '#FFA600', '#FFFF00', '#00FF00','#00FFFF','#0000FF','#FF00FF','#808080','#008000'];
let lat_1km = 1 / 111;
let lng_1km = 0.01;
let lat_50m = lat_1km / 20;
let lng_50m = lng_1km / 20;

function route_plan(robots) {
    $.each(scopes, function (idx, scope) {
        scope.setMap(null);
    });
    $.each(paths, function (idx, path) {
        path.setMap(null);
    });
    scopes.length = 0;;
    paths.length = 0;;
    draw_scope(4);
    draw_path(4);

}

function draw_path(paths_json) {
    console.log(paths_json)
    $.each(paths_json, function (idx, path_json) {
        let path = new google.maps.Polyline({
            path: path_json,
            geodesic: true,
            strokeColor: colors[idx], // 折線顏色
            strokeOpacity: 1.0, // 折線透明度
            strokeWeight: 3 // 折線粗度
        });
        path.setMap(map);
        paths.push(path);
    });
    /*
    for (let i = 0; i < uav_quantity; i++) {
        let coordinate = [];
        let lat = uluru.lat - lat_1km / 2 + lat_50m / 2;
        let lng = uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * i + lng_50m / 2;
        let op = 1;
        for(; lat < uluru.lat + lat_1km / 2; lat += lat_50m) {
            console.log('lat: ' + lat);
            for(; lng < uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * (i + 1)
                && lng > uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * i; lng += lng_50m * op) {
                    coordinate.push({ lat: lat, lng,lng });
                    console.log('lng: ' + lng);
                }
            op *= -1;
            lng += lng_50m * op;
        }
        console.log(coordinate);
        let path = new google.maps.Polyline({
            path: coordinate,
            geodesic: true,
            strokeColor: colors[i], // 折線顏色
            strokeOpacity: 1.0, // 折線透明度
            strokeWeight: 3 // 折線粗度
        });
        path.setMap(map);
        paths.push(path);
    }
    */
}

function draw_scope(scopes_json) {
    $.each(scopes_json, function (idx, scope_json) {
        let scope = new google.maps.Polygon({
            path: scope_json,
            strokeColor: colors[idx], // 線條顏色
            strokeOpacity: 0.8, // 線條透明度
            strokeWeight: 5, // 線條粗度
            fillColor: colors[idx], // 多邊形裡填滿的顏色
            fillOpacity: 0.24 // 多邊形裡，填滿顏色的透明度
        });
        scope.setMap(map);
        scopes.push(scope);
    });
    /*
    for (let i = 0; i < uav_quantity; i++) {
        let coordinate = [
            { lat: uluru.lat - lat_1km / 2, lng: uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * i },//左下
            { lat: uluru.lat + lat_1km / 2, lng: uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * i },//左上
            { lat: uluru.lat + lat_1km / 2, lng: uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * (i + 1) },//右上
            { lat: uluru.lat - lat_1km / 2, lng: uluru.lng - lng_1km / 2 + lng_1km / uav_quantity * (i + 1) },//右下
        ];
        let scope = new google.maps.Polygon({
            path: coordinate,
            strokeColor: colors[i], // 線條顏色
            strokeOpacity: 0.8, // 線條透明度
            strokeWeight: 5, // 線條粗度
            fillColor: colors[i], // 多邊形裡填滿的顏色
            fillOpacity: 0.24 // 多邊形裡，填滿顏色的透明度
        });
        scope.setMap(map);
        scopes.push(scope);
    }
    */
}

function plan(){
    /*
    let position = {
        lat: center_marker.position.lat(),
        lng: center_marker.position.lng()
    };
    */
    let position = {
        lat: 0,
        lng: 0
    };
    console.log("get_target");
    socket.emit('get_target', position);
    //map.setCenter(position);
}