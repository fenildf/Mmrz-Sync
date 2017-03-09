// Provide tool functions

Array.prototype.contains = function (obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
}

function Copyright() {
    copyright.innerHTML = "<a style='color: black;' target='_blank' href='/ranking'>&copy </a>" + "2016-" + (new Date()).getFullYear() + " by <a style='color: black;' target='_blank' href='http://github.com/zhanglintc/Mmrz-Sync'>zhanglintc</a>";
}

function is_cellphone() {
    var userAgentInfo = navigator.userAgent;
    var Agents = ["Android", "iPhone",
                "SymbianOS", "Windows Phone",
                "iPad", "iPod"];
    var flag = false;
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = true;
            break;
        }
    }
    return flag;
}

function getQueryString(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

// 二分查找法，查找并返回字符在数组中的下标
function binarySearch(target, arr, low, high) {
    if (low <= high) {
        if (arr[low] == target) return low;
        if (arr[high] == target) return high;
        var mid = Math.ceil((high + low) / 2);
        if (arr[mid] == target) {
            return mid;
        }
        else if(arr[mid] > target) {
            return binarySearch(target, arr, low, mid - 1);
        } else {
            return binarySearch(target, arr, mid + 1, high);
        }
    }
    return - 1;
}

function post(url, params) {
    var form = document.createElement("form");

    form.action = url;
    form.method = "post";
    form.style.display = "none";

    for(var x in params) {
        var opt = document.createElement("input");
        opt.name = x;
        opt.value = params[x];
        form.appendChild(opt);
    }

    document.body.appendChild(form);
    form.submit();

    return form;
}

function verify_user(username, password) {
    verified = false;

    params = {
        username: username,
        password: window.btoa(password),
    }

    $.ajax({
        url:"/log_in",
        type:"post",
        data:params,
        async:false,
        success:function(rec) {
            rec = JSON.parse(rec);
            if(rec['verified'] == true) {
                verified = true;
            }
            else {
                verified = false;
            }
        }
    });

    return verified;
}

function cal_remind_time(memTimes, type) {
    curTime = Math.floor(new Date().getTime() / 1000);

    switch(memTimes) {
    case 0:
        remindTime = curTime + (60 * 5); // 5 minutes
        break;
    case 1:
        remindTime = curTime + (60 * 30); // 30 minutes
        break;
    case 2:
        remindTime = curTime + (60 * 60 * 12); // 12 hours
        break;
    case 3:
        remindTime = curTime + (60 * 60 * 24); // 1 day
        break;
    case 4:
        remindTime = curTime + (60 * 60 * 24 * 2); // 2 days
        break;
    case 5:
        remindTime = curTime + (60 * 60 * 24 * 4); // 4 days
        break;
    case 6:
        remindTime = curTime + (60 * 60 * 24 * 7); // 7 days
        break;
    case 7:
        remindTime = curTime + (60 * 60 * 24 * 15); // 15 days
        break;
    default:
        remindTime = curTime;
        break;
    }

    switch(type) {
    case "int":
        return remindTime;
    case "str":
        return new Date(remindTime * 1000);
    }
}

function getRadioValue(radio) {
    var obj = window.document.getElementsByName(radio);

    for(i = 0; i < obj.length; i++) {
        if(obj[i].checked == true) {
            return obj[i].value;
        }
    }
}

function get_weekly_mmrz_time(username) {
    weekly_data = [];

    params = {
        username: username,
    }

    $.ajax({
        url: "/get_weekly_mmrz_time",
        type: "get",
        data: params,
        async: false,
        success:function(rec) {
            weekly_data = JSON.parse(rec);
        }
    });

    return weekly_data;
}

function make_weekly_chart(canvas_id, weekly_data) {
    ctx = canvas_id;
    random_string_list = [
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
    ]
    data = {
        labels: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        datasets: [{
            label: "背诵时长",
            backgroundColor: [
                // 'rgba(255, 99, 132, 0.2)',
                // 'rgba(54, 162, 235, 0.2)',
                // 'rgba(255, 206, 86, 0.2)',
                // 'rgba(75, 192, 192, 0.2)',
                // 'rgba(153, 102, 255, 0.2)',
                // 'rgba(255, 159, 64, 0.2)',
                // 'rgba(133, 187, 86, 0.2)',
                random_string_list[0] + ',0.2)',
                random_string_list[1] + ',0.2)',
                random_string_list[2] + ',0.2)',
                random_string_list[3] + ',0.2)',
                random_string_list[4] + ',0.2)',
                random_string_list[5] + ',0.2)',
                random_string_list[6] + ',0.2)',
            ],
            borderColor: [
                // 'rgba(255, 99, 132, 1)',
                // 'rgba(54, 162, 235, 1)',
                // 'rgba(255, 206, 86, 1)',
                // 'rgba(75, 192, 192, 1)',
                // 'rgba(153, 102, 255, 1)',
                // 'rgba(255, 159, 64, 1)',
                // 'rgba(133, 187, 86, 1)',
                random_string_list[0] + ',1)',
                random_string_list[1] + ',1)',
                random_string_list[2] + ',1)',
                random_string_list[3] + ',1)',
                random_string_list[4] + ',1)',
                random_string_list[5] + ',1)',
                random_string_list[6] + ',1)',
            ],
            borderWidth: 1,
            data: weekly_data,
        }]
    };
    options = {
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };
    myBarChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options,
    });
}

function setParking_DeckPlaceholder() {
    if(getRadioValue("area") == "A") {
        parking_deck.placeholder = "A区范围: 001 - " + SERIAL_INFO.data[0].length;
    }
    else if(getRadioValue("area") == "B") {
        parking_deck.placeholder = "B区范围: 001 - " + SERIAL_INFO.data[1].length;
    }
    else {
        parking_deck.placeholder = "C区范围: 001 - " + SERIAL_INFO.data[2].length;
    }
}