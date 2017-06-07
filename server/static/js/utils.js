// Provide tool functions

// Mmrz Code below:
// universal:
window.MMRZ_CODE_Universal_OK = 0
window.MMRZ_CODE_Universal_Error = -40001
window.MMRZ_CODE_Universal_Verification_Fail = -40002

// signup:
window.MMRZ_CODE_Signup_OK = window.MMRZ_CODE_Universal_OK
window.MMRZ_CODE_Username_Not_Available_Error = -400011
window.MMRZ_CODE_Username_Not_Valid = -400012
window.MMRZ_CODE_Password_Not_Valid = -400013

// email
window.MMRZ_CODE_Email_Verification_OK = window.MMRZ_CODE_Universal_OK
window.MMRZ_CODE_Email_Send_OK = window.MMRZ_CODE_Universal_OK
window.MMRZ_CODE_Email_Address_Not_Changed = -400101
window.MMRZ_CODE_Email_Modification_Frequency_Limit_Error = -400102
window.MMRZ_CODE_Email_Send_Frequency_Limit_Error = -400103
window.MMRZ_CODE_Email_VeriCode_Out_Of_Date = -400104

// save current state:
window.MMRZ_CODE_SaveState_Save_OK = window.MMRZ_CODE_Universal_OK
window.MMRZ_CODE_Restore_State_OK = window.MMRZ_CODE_Universal_OK
window.MMRZ_CODE_SaveState_Same_Eigenvalue = -400201
window.MMRZ_CODE_SaveState_Diff_Eigenvalue = -400202



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
    copyright.innerHTML =  "<a style='color: black;' target='_blank' href='/ranking'>&copy </a>" + "2016-" + (new Date()).getFullYear() + " by <a style='color: black;' target='_blank' href='http://github.com/zhanglintc/Mmrz-Sync'>zhanglintc</a>";
    copyright.innerHTML += "<br>";
    copyright.innerHTML += "<a style='color: black; font-size: 10px;' target='_blank' href='http://www.miitbeian.gov.cn'>渝ICP备17002936号</a>";
}

function is_cellphone() {
    userAgentInfo = navigator.userAgent;
    Agents = [
        "Android",
        "iPhone",
        "SymbianOS",
        "Windows Phone",
        "iPad",
        "iPod"
    ];

    flag = false;
    for(v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = true;
            break;
        }
    }

    return flag;
}

function is_word_EN(key_word) {
    regx = /^[a-zA-Z]+$/;

    return regx.test(key_word);
}

function is_word_JA(key_word) {
    regx = /^[\u30a1-\u30f6\u3041-\u3093\uFF00-\uFFFF\u4e00-\u9fa5|ー]+$/;

    return regx.test(key_word);
}

function getQueryString(name) { 
    reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    r = window.location.search.substr(1).match(reg);
    if(r != null) return decodeURI(r[2]); return null; // unescape => decodeURI
}

function get_hujiang_url(key_word) {
    url = "";

    // EN
    if(is_word_EN(key_word)) {
        if(is_cellphone()) {
            url = "http://m.hujiang.com/d/" + key_word;
        }
        else {
            url = "http://dict.hjenglish.com/w/" + key_word;
        }
    }
    // JA
    else {
        if(is_cellphone()) {
            url = "http://m.hujiang.com/d/jp/" + key_word;
        }
        else {
            url = "http://dict.hjenglish.com/jp/jc/" + key_word;
        }
    }

    return url;
}

// 二分查找法，查找并返回字符在数组中的下标
function binarySearch(target, arr, low, high) {
    if (low <= high) {
        if (arr[low] == target) return low;
        if (arr[high] == target) return high;
        mid = Math.ceil((high + low) / 2);

        if (arr[mid] == target) {
            return mid;
        }
        else if(arr[mid] > target) {
            return binarySearch(target, arr, low, mid - 1);
        }
        else {
            return binarySearch(target, arr, mid + 1, high);
        }
    }
    return - 1;
}

function post(url, params) {
    form = document.createElement("form");

    form.action = url;
    form.method = "post";
    form.style.display = "none";

    for(var x in params) {
        opt = document.createElement("input");
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
        password: password,
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

function get_ranking_info(period) {
    ranking_data = [];

    params = {
        period: period,
    }

    $.ajax({
        url: "/get_ranking_info",
        type: "get",
        data: params,
        async: false,
        success:function(rec) {
            ranking_data = JSON.parse(rec);
        }
    });

    return ranking_data;
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

function make_ranking_chart(canvas_id, ranking_data) {
    // ranking_data[i][0]: username
    // ranking_data[i][1]: memorized minutes
    ctx = canvas_id;
    random_string_list = [
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
        'rgba(' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255) + ',' + Math.round(Math.random()*255),
    ]
    data = {
        labels: [
            ranking_data[0][0],
            ranking_data[1][0],
            ranking_data[2][0],
            ranking_data[3][0],
            ranking_data[4][0],
        ],
        datasets: [{
            label: "背诵时长",
            backgroundColor: [
                random_string_list[0] + ',0.2)',
                random_string_list[1] + ',0.2)',
                random_string_list[2] + ',0.2)',
                random_string_list[3] + ',0.2)',
                random_string_list[4] + ',0.2)',
            ],
            borderColor: [
                random_string_list[0] + ',1)',
                random_string_list[1] + ',1)',
                random_string_list[2] + ',1)',
                random_string_list[3] + ',1)',
                random_string_list[4] + ',1)',
            ],
            borderWidth: 1,
            data: [
                ranking_data[0][1],
                ranking_data[1][1],
                ranking_data[2][1],
                ranking_data[3][1],
                ranking_data[4][1],
            ],
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

(function() {
    if(document.domain.search("zhanglintc.work") != -1) {
        location.href="https://mmrz.zhanglintc.co";
    }
}());


