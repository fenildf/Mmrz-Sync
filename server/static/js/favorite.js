// functions for favourite.tpl

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());


// 单词收藏 事件处理 （画面收藏小图片触发事件）
function favourite_action(idx, word_id) {
    // row[0]: word_id
    // row[1]: favourite
    // row[2]: memTimes

    favourite = $('input[name="favourite"]')[idx - 1].value;

    row = [];
    row[0] = word_id;
    row[1] = favourite ^ 1; // 异或操作, 1 => 0, 0 => 1
    row[2] = 0;
    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
        row: JSON.stringify(row),
    }

    $.ajax({
        url: "/update_word_favourite",
        type: "post",
        data: params,
        async: true,
        success: function(rec) {
            rec = JSON.parse(rec);

            // 异步处理回来后，改变收藏小图片的样式
            if(favourite == 1) {
                $('.favourite_btn').eq(idx - 1).css("background", 'url(/img/outline_star.png)').css("background-size", 'cover');
            } else {
                $('.favourite_btn').eq(idx - 1).css("background", 'url(/img/christmas_star.png)').css("background-size", 'cover');
            }

            $('input[name="favourite"]').eq(idx - 1).val(favourite ^ 1);
        }
    });
}
