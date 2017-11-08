// functions for welcome.tpl

(function() {
    if(verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/memorize";
    }
}());
