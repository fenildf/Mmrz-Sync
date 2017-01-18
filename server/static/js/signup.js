// functions for login.tpl

function prompt_change() {
    $("#prompt").text("");
    $("#username").css("background-color", "white");
    $("#password").css("background-color", "white");
    $("#password_confirm").css("background-color", "white");
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

function password_check() {
    if(!username_check()) {
        return;
    }

    if($("#password").val() == "") {
        $("#prompt").text("不能为空");
        $("#password").css("background-color", "#ffb6c1");
        $("#password").focus();
        return false;
    }
    else {
        $("#prompt").text("");
        $("#password_confirm").focus();
        return true;
    }
}

function signup() {
    username         = $("#username").val();
    password         = $("#password").val();
    password_confirm = $("#password_confirm").val();

    if(!username_check()) {
        return;
    }

    if(!password_check()) {
        return;
    }

    if($("#password_confirm").val() == "") {
        $("#prompt").text("不能为空");
        $("#password_confirm").css("background-color", "#ffb6c1");
        $("#password_confirm").focus();
        return;
    }

    if(password != password_confirm) {
        $("#prompt").text("两次密码输入不一致");
        return;
    }
    else {
        $("#prompt").text("");
    }

    params = {
        username: username,
        password: window.btoa(password),
    }

    $.post('/sign_up', params, function(rec) {
        rec = JSON.parse(rec);
        if(rec['verified'] == true) {
            alert("帐号 " + username + " 注册成功, 请妥善保管");

            location.href="/";
        }
        else {
            $("#prompt").text("用户名已被占用, 请重试");
        }
    });

    return;
}

(function() {
    alert("注意:　功能测试中, 建议不要使用常用密码, 以免泄露");
    alert("目前单词上传功能仅限于MmrzGUI版本有效, 网页版注册账号后暂时无法使用导入单词等全部功能")
}());
