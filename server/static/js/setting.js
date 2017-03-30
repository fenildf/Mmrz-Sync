// functions for setting.tpl

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());

function send_verification_mail() {
    params = {};

    $.ajax({
        url: "/send_verification_mail",
        type: "post",
        data: params,
        async: true,
    });
}

function update_userinfo(email) {
    regx = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;

    is_email_valid = regx.test(email);
    if(is_email_valid) {
        send_verification_mail();
        alert("已向邮箱: " + email + " 发送验证邮件, 请登录相应邮箱进行验证");
    }
    else {
        alert("邮箱格式校验失败, 请确认后重新输入");
    }
}

function update_password() {
    if($("#password_current").val() == "") {
        alert("当前密码不能为空");
        return;
    }
    if($("#password_new").val() == "") {
        alert("新密码不能为空");
        return;
    }
    if($("#password_again").val() == "") {
        alert("密码确认不能为空");
        return;
    }
    if($("#password_again").val() != $("#password_new").val()) {
        alert("两次密码输入不一致");
        return;
    }

    username = $.cookie('username');
    password = $("#password_current").val();
    new_pass = $("#password_again").val();

    params = {
        username: username,
        password: window.btoa(password),
        new_pass: window.btoa(new_pass),
    }

    $.post('/update_password', params, function(rec) {
        rec = JSON.parse(rec);
        if(rec['verified'] == true) {
            $.cookie('username', username,              {path: '/', expires: 365});
            $.cookie('password', window.btoa(new_pass), {path: '/', expires: 365});

            alert("密码修改成功");
        }
        else {
            alert("帐号或密码不正确")
        }
    });
}
