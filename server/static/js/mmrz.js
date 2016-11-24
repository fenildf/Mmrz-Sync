// functions for mmrz.tpl

function logout() {
    $.cookie('username', "", {path: '/', expires: 7});
    $.cookie('password', "", {path: '/', expires: 7});
    location.reload(true);   
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());
