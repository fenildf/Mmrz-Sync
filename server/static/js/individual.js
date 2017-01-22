// functions for individual.tpl

function online_import() {
    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
        quantity: Number($("#quantity").val()),
    }

    $.post('/online_import', params, function(rec) {
        alert("本次成功导入" + $("#quantity").val() + "个单词");
        location.reload(true);
    });
}

function limit_import_number(self) {
    self.value = self.value.replace(/[^0-9]/g, "");
    self.value = (self.value > 200 ? 200 : self.value);
    self.value = (self.value <   1 ?   1 : self.value);
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());