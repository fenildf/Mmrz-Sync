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