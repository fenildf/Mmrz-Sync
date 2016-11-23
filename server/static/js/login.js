// functions for login.tpl

prompt_change = function() {
    $("#prompt").text("");
    $("#username").css("background-color", "white");
    $("#password").css("background-color", "white");
}

username_check = function() {
    if($("#username").val() == "") {
        $("#prompt").text("不能为空")
        $("#username").css("background-color", "#ffb6c1");
        $("#username").focus();
        return false;
    }
    else {
        $("#prompt").text("")
        $("#password").focus();
        return true;
    }
}

login = function() {
    username = $("#username").val();
    password = $("#password").val();

    if(!username_check()) {
        return;
    }

    if($("#password").val() == "") {
        $("#prompt").text("不能为空")
        $("#password").css("background-color", "#ffb6c1");
        $("#password").focus();
        return;
    }

    params = {
        username: username,
        password: window.btoa(password),
    }

    $.post('/log_in', params, function(rec) {
        rec = JSON.parse(rec);
        if(rec['verified'] == true) {
            $.cookie('username', username, {path: '/', expires: 7});
            $.cookie('password', password, {path: '/', expires: 7});

            location.href="/memorize";
        }
        else {
            $.cookie('username', "", {path: '/', expires: 7});
            $.cookie('password', "", {path: '/', expires: 7});

            $("#prompt").text("帐号或密码不正确");
        }
    });
}