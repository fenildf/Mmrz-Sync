// functions for mmrz.tpl

function logout() {
    $.cookie('username', "", {path: '/', expires: 7});
    $.cookie('password', "", {path: '/', expires: 7});
    location.reload(true);   
}

function get_wordbook() {
    wordbook = []

    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
    }

    $.ajax({
        url:"/download_wordbook",
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

function init_rows_from_DB() {
    wordbook = get_wordbook();
    window.rows_from_DB = [];
    window.cursor_of_rows = 0;

    for(i = 0; i < wordbook.length; i++) {
        row = wordbook[i];
        row[6] = false;
        if(row[3] < (new Date().getTime() / 1000)) {
            window.rows_from_DB.push(row);
        }
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
    if(window.rows_from_DB.length == 0) {
        alert("本次背诵完毕");
    }
    else {
        $("#label_word").text(window.rows_from_DB[window.cursor_of_rows][0]);
        $("#words_left").text("剩余 " + window.rows_from_DB.length + " 个单词")
    }
}

function show_secret() {
    window.secret_is_hiding = false;
    $("#label_meaning").text(window.rows_from_DB[window.cursor_of_rows][1]);

    $("#btn_view").css("display", "none");
    $("#btn_yes").css("display", "");
    $("#btn_no").css("display", "");
}

function hide_secret(remember, pass) {
    window.secret_is_hiding = true;
    if(window.rows_from_DB.length == 0) {
        alert("no word now");
        return;
    }

    if(remember || pass) {
        row = window.rows_from_DB[window.cursor_of_rows];
        firstTimeFail = row[6];

        if(!firstTimeFail) {
            row[2] += 1;
        }
        if(pass) {
            row[2] = 9;
        }
        // row[3] = COMM::cal_remind_time row[2], "int"
        // row[4] = COMM::cal_remind_time row[2], "str"

        window.rows_from_DB.splice(window.cursor_of_rows, 1);
        move_cursor(false);
    }
    else {
        window.rows_from_DB[window.cursor_of_rows][6] = true; // firstTimeFail: false => true
        move_cursor(true);
    }

    $("#btn_view").css("display", "");
    $("#btn_yes").css("display", "none");
    $("#btn_no").css("display", "none");
    $("#label_meaning").text("");
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
    init_rows_from_DB();
}());
