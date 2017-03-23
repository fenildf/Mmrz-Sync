// functions for login.tpl

function prompt_change() {
    $("#prompt").text("");
    $("#username").css("background-color", "white");
    $("#password").css("background-color", "white");
}

function username_check() {
    if($("#username").val() == "") {
        $("#prompt").text("不能为空");
        $("#username").css("background-color", "#ffb6c1");
        $("#username").focus();
        return false;
    }
    else {
        $("#prompt").text("");
        $("#password").focus();
        return true;
    }
}

function login() {
    username = $("#username").val();
    password = $("#password").val();

    if(!username_check()) {
        return;
    }

    if($("#password").val() == "") {
        $("#prompt").text("不能为空");
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
            $.cookie('username', username,              {path: '/', expires: 365});
            $.cookie('password', window.btoa(password), {path: '/', expires: 365});

            location.href="/memorize";
        }
        else {
            $.cookie('username', "", {path: '/', expires: 365});
            $.cookie('password', "", {path: '/', expires: 365});

            $("#prompt").text("帐号或密码不正确");
        }
    });
}

(function() {
    if(verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/memorize";
    }
}());
