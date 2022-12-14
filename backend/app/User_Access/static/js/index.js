let socket;
let baseurl = "http://192.168.0.140:8080/user_access";
let target_position = {
    x: -1,
    y: -1
};
//let target_scope;

var text;

text = document.getElementById('chat').value;
//text = text + "\nGPS: 23.5757884, 120.4694816\nAQI Level: 2\n\nGPS: 23.5757884, 120.4694816\nAQI Level: 2\n\nGPS: 23.5757884, 120.4694816\nAQI Level: 2";
//document.getElementById('chat').value = text;

var aqi = 1;
//update_aqi(aqi);
//setInterval('update_aqi(aqi)',1000);


$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port);

    target = prompt("請輸入偵測區域中心座標");
    target_position.x = parseFloat(target.split(",")[0]);
    target_position.y = parseFloat(target.split(",")[1]);
    //target_scope = prompt("請輸入搜索區域半徑（km）");
    //socket.emit('get_taget_scope_input', target_scope);
    socket.emit('get_taget_position_input', target_position);
    
    /*socket.on('update', function(robots) {
        $("a").remove(".dropdown-item");
        if(robots.UAV.length > 0) {
            if($.trim($('#dropdown06').text()) == "無機器人連接") {
                $('#dropdown06').text("機器人");
            }
            /*$.each(robots.GR, function(idx, GR) {
                update_location(GR);
                $('.dropdown-menu').append('<a class="dropdown-item" href="' + baseurl + '/robot/GR/' + GR.ID + '/' + GR.host + '">多足機器人' + GR.ID + '</a>');
            });
            $.each(robots.UAV, function(idx, UAV) {
                update_location(UAV);
                $('.dropdown-menu').append('<a class="dropdown-item" href="' + baseurl + '/robot/UAV/' + UAV.ID + '/' + UAV.host + '">無人機' + UAV.ID + '</a>');
            });
        }
        else {
            $('#dropdown06').text("無機器人連接");
        }
        renew(robots);
    });*/

    socket.on('plan_update', function(result) {
        if(result.state == 'fail') {
            alert(result.message);
        }
        else if(result.state == 'OK') {
            $.each(scopes, function (idx, scope) {
                scope.setMap(null);
            });
            scopes.length = 0;
            $.each(paths, function (idx, path) {
                path.setMap(null);
            });
            paths.length = 0;
            draw_scope(result.scopes);
            draw_path(result.paths)
            console.log(result.scopes);
        }
    });
	
    /*socket.on('get_uav_find', function(data) {
        alert(data.robot.type + data.robot.ID.toString() + " 發現疑似受困人員\n位置：" + data.position.x.toString() + ", " + data.position.y.toString());
    });*/
    
    socket.on('get_dpu_detect', function(robot) {
        //alert(robot.type + robot.ID.toString() + " 位置：" + position_GPS.lat.toString() + ", " + position_GPS.lng.toString() + "\nAQI : " + robot.AQI_dpu);
        update_aqi(robot.AQI_dpu, robot.position_GPS.lat, robot.position_GPS.lng)
    });

});

function update_aqi(AQI, lat, lng){
	text = document.getElementById('chat').value;
	text = text + "\nAQI Level : " + AQI + "\nLatitude : " + lat + "\nLongitude : " + lng + "\n";
	document.getElementById('chat').value = text;
    var textarea = document.getElementById('chat');
    textarea.scrollTop = textarea.scrollHeight;
}

/*
function update_location(robot){
    let x = robot.position_bluetooth.x - 1;
    let y = robot.position_bluetooth.y - 1;
    for(let i=0;i<10;i++){
        for(let j=0;j<10;j++){
            $("#bluetooth_map tr:eq(" + i + ") td:eq("+ j + ")").css('background-color','white');
        }
    }
    
    $("#bluetooth_map tr:eq(" + x + ") td:eq("+ y + ")").css('background-color','green');
}*/