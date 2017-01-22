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

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());