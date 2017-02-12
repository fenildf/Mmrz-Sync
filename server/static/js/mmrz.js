// functions for mmrz.tpl

function logout() {
    $.cookie('username', "", {path: '/', expires: 7});
    $.cookie('password', "", {path: '/', expires: 7});
    location.href="/";
}

function get_wordbook() {
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
            rec = JSON.parse(rec);
            wordbook = rec['wordbook'];
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
    wordbook = get_wordbook();
    window.rows_from_DB = [];
    window.cursor_of_rows = 0;
    window.null_when_open = false;

    for(i = 0; i < wordbook.length; i++) {
        row = wordbook[i];
        row[6] = false;
        if(row[3] < (new Date().getTime() / 1000)) {
            window.rows_from_DB.push(row);
        }
    }

    if(window.rows_from_DB.length == 0) {
        window.null_when_open = true;
    }
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

        $("#words_count").empty();

        if(!window.null_when_open) {
            alert("本次背诵完毕");
            location.reload();
        }

        $("#label_word").text(get_shortest_remind());
        $("#words_left").text("剩余 " + window.rows_from_DB.length + " 个单词");
        $("#mem_times").text("");
        $("#btn_pass").text("");
        $("#speak_btn").css("display", "none");
    }
    // 尚未背诵完毕
    else {
        // 每次都清空相关内容
        document.getElementById("speaker").src = "";
        window.word_tts_url = "";

        key_word = window.rows_from_DB[window.cursor_of_rows][0];
        params = {};

        // 此时会有网络访问
        $.ajax({
            url: "/get_hujiang_tts/?key_word=" + key_word,
            type: "get",
            data: params,
            async: true,
            success: function(rec) {
                window.word_tts_url = rec;
            }
        });

        $("#label_word").text(window.rows_from_DB[window.cursor_of_rows][0]);
        $("#mem_times").text(window.rows_from_DB[window.cursor_of_rows][2]);
        $("#words_left").text("剩余 " + window.rows_from_DB.length + " 个单词");
        $("#btn_view").css("display", "");
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
