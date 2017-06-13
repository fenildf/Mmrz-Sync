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
    favourite ^= 1; // 异或操作, 1 => 0, 0 => 1

    row = [];
    row[0] = word_id;
    row[1] = favourite;
    row[2] = 0;
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
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
            // button_row_obj = $(":button").eq(idx - 1);
            icon_star_black = $(".favourite_star_black_btn").eq(idx - 1);
            icon_star_white = $(".favourite_star_white_btn").eq(idx - 1);

            if(favourite == 1) {
                icon_star_black.css("display", "");
                icon_star_white.css("display", "none");
            } else {
                icon_star_black.css("display", "none");
                icon_star_white.css("display", "");
            }

            $('input[name="favourite"]').eq(idx - 1).val(favourite);
        }
    });
}

function jump_to_hujiang(idx) {
    overlay = $(".td_word");

    if(overlay.length <= 0) {
        return;
    }

    key_word = overlay[idx - 1].innerHTML;

    url = get_hujiang_url(key_word);    
    if(is_cellphone()) {
        layer.open({
            id: "iframe_hujiang",
            type: 2,
            title: ["沪江小D", 'font-size: 20px;'],
            closeBtn: 0,
            moveEnd: function() {
                layer.close(layer.index);
            },
            shadeClose: true,
            resize: false,
            scrollbar: false,
            area: ['280px', '400px'],
            success: function(index){
                layer.setTop(index);
                $("#iframe_hujiang").focus();
            },
            content: url
        });
    }
    else {
        window.open(url);
    }
}

function show_word_meaning(idx) {
    overlay = $(".td_favourite");
    all_show_word = $('input[name="show_word"]')[0].value;

    if(overlay.length <= 0) {
        return;
    }

    if(idx != 'all') {
        overlay[idx - 1].classList.toggle("td_favourite_color");
    }
    else if (all_show_word == 0) {
        for(i = 0; i < overlay.length; i++) {
            overlay[i].classList.add("td_favourite_color");
        }
        $('input[name="show_word"]').eq(0).val("1");
        $("#word_meaning_title").text("※点击隐藏全部");
    }
    else {
        for(i = 0; i < overlay.length; i++) {
            overlay[i].classList.remove("td_favourite_color");
        }
        $('input[name="show_word"]').eq(0).val("0");
        $("#word_meaning_title").text("※点击显示全部");
    }
}