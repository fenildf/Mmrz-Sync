// functions for setting.tpl

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());

function send_verification_mail(email) {
    params = {
        "username": $.cookie("username"),
        "mailAddr": email
    };

    mmrz_code = 0;
    $.ajax({
        url: "/send_verification_mail",
        type: "post",
        data: params,
        async: false,
        success:function(rec) {
            rec = JSON.parse(rec);
            mmrz_code = rec["mmrz_code"];
        }
    });

    return mmrz_code;
}

function update_userinfo(email) {
    regx = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;

    is_email_valid = regx.test(email);
    if(is_email_valid) {
        mmrz_code = send_verification_mail(email);
        if(mmrz_code == window.MMRZ_CODE_Email_Address_Not_Changed) {
            console.log("个人邮件信息没有变化");
        }
        else if(mmrz_code == window.MMRZ_CODE_Email_Send_OK) {
            alert("已向邮箱: " + email + " 发送验证邮件, 请登录相应邮箱进行验证\n\n若未收到邮件, 请检查垃圾邮件文件夹");
        }
        else if(mmrz_code == window.MMRZ_CODE_Email_Modification_Frequency_Limit_Error) {
            alert("七天之内只能修改一次邮箱");
        }
        else if(mmrz_code == window.MMRZ_CODE_Email_Send_Frequency_Limit_Error) {
            alert("每五分钟之内只能发送一次验证邮件");
        }
        else {
            console.log("发送邮件的默认处理: 无处理");
        }
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
