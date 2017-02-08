// functions for individual.tpl

function online_import() {
    if($("#quantity").val() == "") {
        alert("导入数量不能为空");
        return;
    }

    if(Number($("#quantity").val()) == 0) {
        alert("不能导入0个单词");
        return;
    }

    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
        quantity: Number($("#quantity").val()),
    }

    $.post('/online_import', params, function(rec) {
        alert("本次成功导入" + Number($("#quantity").val()) + "个单词");
        location.reload(true);
    });
}

function limit_import_number(self) {
    self.value = self.value.replace(/[^0-9]/g, "");
    self.value = (self.value > 200 ? 200 : self.value);
    self.value = (self.value <   0 ?  "" : self.value);
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
            $.cookie('username', username, {path: '/', expires: 365});
            $.cookie('password', new_pass, {path: '/', expires: 365});

            alert("密码修改成功");
        }
        else {
            alert("帐号或密码不正确")
        }
    });
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());