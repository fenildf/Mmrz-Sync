// functions for mmrz.tpl

function search_word_id(target, arr, low, high) {
    if (low <= high) {
        if (arr[low][5] == target) return low;
        if (arr[high][5] == target) return high;
        var mid = Math.ceil((high + low) / 2);
        if (arr[mid][5] == target) {
            return mid;
        }
        else if(arr[mid][5] > target) {
            return binarySearch(target, arr, low, mid - 1);
        } else {
            return binarySearch(target, arr, mid + 1, high);
        }
    }
    return - 1;
}


function logout() {
    $.cookie('username', "", {path: '/', expires: 7});
    $.cookie('password', "", {path: '/', expires: 7});
    location.href="/";
}

function get_tts_url() {
    // 每次都清空相关内容
    document.getElementById("speaker").src = "";
    window.word_tts_url = "";
    window.word_tts_found = false;

    key_word     = window.rows_from_DB[window.cursor_of_rows][0];

    params = {"job_id": window.rows_from_DB[window.cursor_of_rows][5]};

    // 此时会有网络访问
    $.ajax({
        url: "/get_hujiang_tts/?key_word=" + key_word,
        type: "get",
        data: params,
        async: true,
        success: function(rec) {
            // 手机上, 此处如果点击刷新, 将无法发音; 如果是输入地址回车则可以.
            // 如果在此 ajax 前 alert, 则也能获取正常返回值.
            // 此处如果点击刷新, 谁™也不知道为什么有会返回一个 undefined (后台没有问题, 正常返回了的)
            // 当然也有可能是测试环境的问题.
            // 这里没有办法, 临时处理. (估计会永远临时下去了)
            // 2017.02.14 zhanglintc
            if(typeof(rec) == "undefined") {
                $("#speak_btn").css("background", 'url(/img/novoice.png)').css("background-size", 'cover');
                return;
            }

            rec = JSON.parse(rec);

            // 返回的单词相关的内容不是当前的单词，舍弃之
            if(window.rows_from_DB[window.cursor_of_rows][5] != rec["job_id"]) {
                return;
            }

            window.word_tts_found = rec["found"];
            window.word_tts_url = rec["tts_url"];

            if(!window.word_tts_found) {
                $("#speak_btn").css("background", 'url(/img/novoice.png)').css("background-size", 'cover');
            } else {
                $("#speak_btn").css("background", 'url(/img/speaker.png)').css("background-size", 'cover');
            }
        }
    });
}

function get_wordbooks() {
    wordbook = []

    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
    }

    $.ajax({
        url:"/unmemorized_words",
        type:"post",
        data:params,
        async:false,
        success:function(rec) {
            wordbook = JSON.parse(rec);
        }
    });

    return wordbook;
}

function update_row(row) {
    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
        row: JSON.stringify(row),
    }

    $.ajax({
        url:"/update_row",
        type:"post",
        data:params,
        async:true,
    });
}

function get_shortest_remind() {
    shortest_remind = "";

    params = {
        username: $.cookie('username'),
    }

    $.ajax({
        url:"/get_shortest_remind",
        type:"get",
        data:params,
        async:false,
        success:function(rec) {
            shortest_remind = rec;
        }
    });

    return shortest_remind;
}

function init_rows_from_DB() {
    wordbooks = get_wordbooks();
    wordbook_normal = wordbooks['wordbook'];
    wordbook_favourite = wordbooks['wordfavourite'];
    window.rows_from_DB = [];
    window.cursor_of_rows = 0;
    window.null_when_open = false;

    for(i = 0; i < wordbook_normal.length; i++) {
        row = wordbook_normal[i];
        row[6] = false;

        // sqlite数据库中,显示boolean 有三种状态, 0(false)  1(true)  和 null [不会直接返回true和false]
        row[7] = wordbook_favourite[i][1] == 1 ? 1 : 0;

        if(row[3] < (new Date().getTime() / 1000)) {
            window.rows_from_DB.push(row);
        }
    }

    if(window.rows_from_DB.length == 0) {
        window.null_when_open = true;
    }

    window.max_size_this_turn = window.rows_from_DB.length;
}

function move_cursor(need_move) {
    if(window.cursor_of_rows == window.rows_from_DB.length) {
        window.cursor_of_rows = 0;
        return;
    }

    if(!need_move) {
        return;
    }

    window.cursor_of_rows += 1;
    if(window.cursor_of_rows == window.rows_from_DB.length) {
        window.cursor_of_rows = 0;
    }
}

function show_word() {
    window.secret_is_hiding  = true;
    window.secret_is_showing = !window.secret_is_hiding;

    // 单词背诵完毕
    if(window.rows_from_DB.length == 0) {

        if(!window.null_when_open) {
            alert("本次背诵完毕");
            location.reload();
        }

        $("#label_word").text(get_shortest_remind());
        $("#words_count").empty();
        $("#speak_btn").css("display", "none");
        $("#magnifier_btn").css("display", "none");
        $("#favourite_btn").css("display", "none");
    }
    // 尚未背诵完毕
    else {
        // 每次都清空相关内容
        document.getElementById("speaker").src = "";
        is_favourite = window.rows_from_DB[window.cursor_of_rows][7];

        $("#label_word").text(window.rows_from_DB[window.cursor_of_rows][0]);
        $("#mem_times").text(window.rows_from_DB[window.cursor_of_rows][2]);
        $("#words_left").text("剩余 " + window.rows_from_DB.length + " / " + window.max_size_this_turn + " 个单词");
        $("#btn_view").css("display", "");

        if(is_favourite == 1) {
            $("#favourite_btn").css("background", 'url(/img/christmas_star.png)').css("background-size", 'cover');
        } else {
            $("#favourite_btn").css("background", 'url(/img/outline_star.png)').css("background-size", 'cover');
        }
    }

    $("#btn_yes").css("display", "none");
    $("#btn_no").css("display", "none");
    $("#label_meaning").text("");
    $("#speak_btn").css("background", 'url(/img/speaker.png)').css("background-size", 'cover');
}

function show_secret() {
    window.secret_is_hiding  = false;
    window.secret_is_showing = !window.secret_is_hiding;

    to_show = window.rows_from_DB[window.cursor_of_rows][1];
    if(to_show.length > 30) {
        to_show = to_show.substr(0, 30) + "...";
    }
    $("#label_meaning").text(to_show);

    $("#btn_view").css("display", "none");
    $("#btn_yes").css("display", "");
    $("#btn_no").css("display", "");
}

function hide_secret(remember, pass) {
    if(window.rows_from_DB.length == 0) {
        alert("rows_from_DB is null when hide_secret() is called");
        return;
    }

    if(remember || pass) {
        row = window.rows_from_DB[window.cursor_of_rows];
        firstTimeFail = row[6];

        if(!firstTimeFail) {
            row[2] += 1;
        }
        if(pass) {
            row[2] = 8;
        }
        row[3] = cal_remind_time(row[2], "int")
        row[4] = cal_remind_time(row[2], "str")

        // operate DB here
        update_row(row);

        window.rows_from_DB.splice(window.cursor_of_rows, 1);
        move_cursor(false);
    }
    else {
        window.rows_from_DB[window.cursor_of_rows][6] = true; // firstTimeFail: false => true
        move_cursor(true);
    }
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
    init_rows_from_DB();
}());

// 单词收藏 事件处理 （画面收藏小图片触发事件）
function favourite_action() {
    // row[0]: word_id
    // row[1]: favourite
    // row[2]: memTimes

    row = [];

    row[0] = window.rows_from_DB[window.cursor_of_rows][5];
    row[1] = window.rows_from_DB[window.cursor_of_rows][7] ^ 1; // 异或操作, 1 => 0, 0 => 1
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

            local_word_id  = window.rows_from_DB[window.cursor_of_rows][5];
            remote_word_id = rec['verified_info'][0];
            remote_is_favourite = rec['verified_info'][1];

            // 异步处理回来后，改变收藏小图片的样式
            if(remote_word_id == local_word_id) {

                if(remote_is_favourite == 1) {
                    $("#favourite_btn").css("background", 'url(/img/christmas_star.png)').css("background-size", 'cover');
                } else {
                    $("#favourite_btn").css("background", 'url(/img/outline_star.png)').css("background-size", 'cover');
                }
                window.rows_from_DB[window.cursor_of_rows][7] = remote_is_favourite;

            } else {
                word_id_row = search_word_id(remote_word_id, window.rows_from_DB, 0, window.rows_from_DB.length - 1);
                if(word_id_row != -1) {
                    window.rows_from_DB[word_id_row][7] = remote_is_favourite;
                }
            }
        }
    });
}
