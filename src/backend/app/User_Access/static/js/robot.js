let socket;
let baseurl = "http://192.168.0.140:8080/user_access";
let robot;
let target_position = {
    lng: 8,
    lat: 8
};
$(document).ready(function(){
    


    //$("#bluetooth_map tr:eq(7) td:eq(7)").css('background-color','green');
    //$("#bluetooth_map tr:eq(7) td:eq(8)").css('background-color','gray');
    //$("#bluetooth_map tr:eq(8) td:eq(8)").css('background-color','red');
    //setTimeout("step1()",1000); 
    

    $("#control").css("display", "none");
    //socket = io.connect('https://' + document.domain + ':' + location.port, {secure: true});
    socket = io.connect('http://' + document.domain + ':' + location.port);
    let robot_type = location.pathname.split("/")[3];
    let id = location.pathname.split("/")[4];

    socket.on('update', function(robots) {
        $("a").remove(".dropdown-item");
        console.log(robots);
        if(robots.GR.length > 0 || robots.UAV.length > 0) {
            if($.trim($('#dropdown06').text()) == "無機器人連接") {
                $('#dropdown06').text("機器人");
            }
            $.each(robots.UAV, function(idx, UAV) {
                if(robot_type=='UAV' && id==UAV.ID){
                    robot = UAV;
                    update_location(UAV);
                }
                
                $('.dropdown-menu').append('<a class="dropdown-item" href="' + baseurl + '/robot/UAV/' + UAV.ID + '/' + UAV.host + '">無人機' + UAV.ID + '</a>');
            });
            
        }
        else {
            $('#dropdown06').text("無機器人連接");
        }
        renew(robots);

    });
    
    socket.on('get_target', function() {
        alert("無人機發現疑似受困人員");
        $("#bluetooth_map tr:eq(8) td:eq(8)").css('background-color','white');
        target_position = {
            x: 8,
            y: 8
        };
    });
    
    console.log(robot);
    setInterval('update_img()',100);
});

function step1(){
    $("#bluetooth_map tr:eq(7) td:eq(7)").css('background-color','white');
    $("#bluetooth_map tr:eq(7) td:eq(8)").css('background-color','green');
    $("#bluetooth_map tr:eq(8) td:eq(8)").css('background-color','red');
    setTimeout("step2()",1000); 
}

function step2(){
    $("#bluetooth_map tr:eq(7) td:eq(7)").css('background-color','white');
    $("#bluetooth_map tr:eq(7) td:eq(8)").css('background-color','white');
    $("#bluetooth_map tr:eq(8) td:eq(8)").css('background-color','red');
    alert("多足機器人1發現受困人員\nGPS : 25.0399468, 121.5101402\n藍牙三角定位：8, 2");
}


function update_img(){
    d = new Date();
    //$("#rgb").attr({src:'http://192.168.0.170:8080/user_access/rgb/' + robot.rgb + '/' + d.getTime()});
    //$("#red").attr({src:'http://192.168.0.170:8080/user_access/red/' + robot.red + '/' + d.getTime()});
    $("#rgb").attr({src:'http://192.168.0.140:8080/user_access/rgb/' + "UAV1_rgb.jpg"+ '/' + d.getTime()});
    $("#yolo").attr({src:'http://192.168.0.140:8080/user_access/yolo/' + "UAV1_yolo.jpg"+ '/' + d.getTime()});
    //$("#red").attr({src:'http://192.168.0.120:8080/user_access/red/' + "UAV1_red.jpg" + '/' + d.getTime()});
}

function update_location(robot){
    
    renew_one(robot);
    
    if(target_position) {
        $("#bluetooth_map tr:eq(" + target_position.x + ") td:eq("+ target_position.y + ")").css('background-color','red');

        if(x == target_position.x && y == target_position.y) {
            alert("找到受困人員");
        }
        

        let m = {
            x: (target_position.x - x) / 100,
            y: (target_position.y - y) / 100
        };
        let temp_now = robot.position_bluetooth;
        
        for(let i = 0; i < 100; i++) {
            if(Math.floor(temp_now.x) != x || Math.floor(temp_now.y) != y){
                if(Math.floor(temp_now.x) != target_position.x || Math.floor(temp_now.y) != target_position.y) {
                    $("#bluetooth_map tr:eq(" + Math.floor(temp_now.x) + ") td:eq("+ Math.floor(temp_now.y) + ")").css('background-color','gray');
                }
            }
            temp_now.x += m.x;
            temp_now.y += m.y;
        }
    }
}

function move(Move_command) {
    console.log(robot);
    socket.emit('user_control', { 'robot': robot, 'Move_command': Move_command });
}


let now_stretch = 0;
function stretch(){
    if(now_stretch == 0){
        now_stretch = 1;
        $("#stretch").text("關閉操作面板");
        $("#control").css("display", "");
    }
    else {
        now_stretch = 0;
        $("#stretch").text("展開操作面板");
        $("#control").css("display", "none");
    }
    
}
