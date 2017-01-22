// functions for individual.tpl

function online_import() {
    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
    }

    $.post('/online_import', params, function(rec) {
        alert("导入成功");
        location.reload(true);
    });
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());