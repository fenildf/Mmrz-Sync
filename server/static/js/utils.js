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
    copyright.innerHTML = "&copy; 2016-" + (new Date()).getFullYear() + " by <a style='color: black;' target='_blank' href='http://zhanglintc.co'>zhanglintc</a>";
}

function getQueryString(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
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
    curTime = parseInt(new Date().getTime() / 1000);

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