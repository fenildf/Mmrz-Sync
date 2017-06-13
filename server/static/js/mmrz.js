// functions for mmrz.tpl

// rows_from_DB:
// [0]word           -- char[255]
// [1]pronounce      -- char[255]
// [2]memTimes       -- int
// [3]remindTime     -- int
// [4]remindTimeStr  -- char[255]
// [5]wordID         -- int
// [6]firstTimeFail  -- bool
// [7]is_favourite   -- int => 1 as true, 0 as false


// Global Variables:
// window.rows_from_DB          -- 本次需要背诵单词的列表
// window.cursor_of_rows        -- 当前背诵进度游标的位置
// window.last_rows_from_DB     -- 缓存的上一次单词列表的状态(仅用于undo功能)
// window.last_cursor_of_rows   -- 还窜的上一次游标的状态(仅用于undo功能)
// window.word_tts_found        -- 是否从Mmrz-Sync服务器成功获取了发音(因为函数未使用, 所以该变量也未使用)
// window.word_tts_url          -- 从Mmrz-Sync服务器获取的发音数据地址(因为函数未使用, 所以该变量也未使用)
// window.null_when_open        -- 从服务器获取到的待背诵列表是否一开始就为空(若为空则直接显示相应提示给用户)
// window.max_size_this_turn    -- 用于存储本次获取到的班次列表的大小(仅于显示, current/max中的max部分)
// window.secret_is_hiding      -- 单词含义是否处于隐藏中(true为隐藏中, false为显示中)
// window.secret_is_showing     -- 单词含义是否处于显示中, 总是为secret_is_hiding取反(true为显示中, false为隐藏中)
// window.last_save_timestamp   -- 上一次状态检查时间, 若本次距离上次超过一分钟, 则上传当前背诵进度

function init() {
    // jump to main path if not verified
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }

    // init global variables
    window.last_rows_from_DB = null;
    window.last_cursor_of_rows = null;
    window.last_save_timestamp = Date.parse(new Date()) / 1000;

    // init rows
    init_rows_from_DB();    
}

function search_word_id(target, arr, low, high) {
    if(low <= high) {
        if(arr[low][5] == target) return low;
        if(arr[high][5] == target) return high;
        mid = Math.ceil((high + low) / 2);
        if(arr[mid][5] == target) {
            return mid;
        }
        else if(arr[mid][5] > target) {
            return binarySearch(target, arr, low, mid - 1);
        }
        else {
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

function tik_tik() {
    params = {
        username: $.cookie('username'),
    }

    $.ajax({
        url: "/tik_tik",
        type: "post",
        data: params,
        async: true,
    });
}

function period_state_check() {
    timestamp = Date.parse(new Date()) / 1000;

    if(timestamp - window.last_save_timestamp >= 60) {
        // verify_eiginvalue() only if cursor_of_rows moved or rows_from_DB.length reduced
        if(window.cursor_of_rows != 0 || window.rows_from_DB.length != window.max_size_this_turn) {
            // verify eiginvalue, if OK, call save_current_state() in verify_eiginvalue()
            verify_eiginvalue();
        }
        window.last_save_timestamp = timestamp;
    }

    setTimeout(period_state_check, 5 * 1000);
}

function is_state_cache_available() {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
    };

    state_cached = false;
    $.ajax({
        url: "/is_state_cache_available",
        type: "post",
        data: params,
        async: false,
        success:function(rec) {
            rec = JSON.parse(rec);
            state_cached = rec['state_cached'];
        }
    });

    return state_cached;
}

function verify_eiginvalue() {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
        "rows_length": window.rows_from_DB.length,
        "current_cursor": window.cursor_of_rows,
    };

    $.ajax({
        url: "/verify_eiginvalue",
        type: "post",
        data: params,
        async: true,
        success:function(rec) {
            rec = JSON.parse(rec);
            if(rec["mmrz_code"] == window.MMRZ_CODE_SaveState_Diff_Eigenvalue) {
                save_current_state();
                notie.alert(1, "当前背诵状态已保存至远端", 1.5);
            }
        }
    });
}

function save_current_state() {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),

        // 特征值
        "rows_length": window.rows_from_DB.length,
        "current_cursor": window.cursor_of_rows,

        // 当前状态
        "max_size_this_turn": window.max_size_this_turn,
        "current_state": JSON.stringify(window.rows_from_DB),
    };

    $.ajax({
        url: "/save_current_state",
        type: "post",
        data: params,
        async: true,
        success:function(rec) {
            console.log(rec);
        }
    });
}

function restore_remote_saved_state() {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
    };

    $.ajax({
        url: "/restore_remote_saved_state",
        type: "post",
        data: params,
        async: false,
        success:function(rec) {
            rec = JSON.parse(rec);
            window.cursor_of_rows = rec["current_cursor"];
            window.max_size_this_turn = rec["max_size_this_turn"];
            window.rows_from_DB = rec["data"];

            show_word();

            clear_state_cached_flag();
            layer.msg("恢复状态成功", {'time': 1000});
        }
    });
}

function restore_last_word() {
    if(window.last_rows_from_DB != null) {
        window.rows_from_DB = window.last_rows_from_DB;
        window.cursor_of_rows = window.last_cursor_of_rows;

        window.last_rows_from_DB = null;
        window.last_cursor_of_rows = null;
        $("#btn_undo").css("color", "gray");

        row = window.rows_from_DB[window.cursor_of_rows];
        update_row(row, false);

        show_word();

        layer.msg("恢复上一个单词成功", {'time': 1000});
    }
    else {
        alert("然而并没有可供恢复的单词");
    }
}

function clear_state_cached_flag() {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
    };

    $.ajax({
        url: "/clear_state_cached_flag",
        type: "post",
        data: params,
        async: true,
        success:function(rec) {
            console.log("clear_state_cached_flag OK");
        }
    });
}

function get_wordbooks() {
    wordbook = []

    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
    };

    $.ajax({
        url: "/unmemorized_words",
        type: "post",
        data: params,
        async: false,
        success:function(rec) {
            wordbook = JSON.parse(rec);
        }
    });

    return wordbook;
}

function update_row(row, update_whole_row) {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
        row: JSON.stringify(row),
        update_whole_row: update_whole_row,
    };

    $.ajax({
        url: "/update_row",
        type: "post",
        data: params,
        async: true,
    });
}

function get_shortest_remind() {
    shortest_remind = "";

    params = {
        username: $.cookie('username'),
    };

    $.ajax({
        url: "/get_shortest_remind",
        type: "get",
        data: params,
        async: false,
        success: function(rec) {
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

    inspire_words = [
        "每天都要坚持背诵哦",
        "做的很好, 继续保持",
        "每天100, 一年就是3w个单词",
        "加油, 加油, 你是最棒的",
        "今日奋斗榜上有你的名字吗",
        "常来看看有没有新单词需要背诵",
    ];

    // 单词背诵完毕
    if(window.rows_from_DB.length == 0) {

        if(!window.null_when_open) {
            clear_state_cached_flag();
            alert( "恭喜完成本轮背诵\n\n" + inspire_words[Math.round(Math.random() * (inspire_words.length - 1))] );
            location.reload();
        }

        $("#label_word").text(get_shortest_remind());
        $("#words_count").empty();

        set_speaker_icon("none");
        $("#magnifier_btn").css("display", "none");
        set_favourite_icon("none");
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
            set_favourite_icon("black");
        } else {
            set_favourite_icon("white");
        }
    }

    $("#btn_yes").css("display", "none");
    $("#btn_no").css("display", "none");
    $("#label_meaning").text("");
    set_speaker_icon("png");
}

function show_secret() {
    if(window.rows_from_DB.length == 0) {
        console.log("rows_from_DB is null when show_secret() is called");
        return;
    }

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
        console.log("rows_from_DB is null when hide_secret() is called");
        return;
    }

    window.last_rows_from_DB = $.extend(true, [], window.rows_from_DB);
    window.last_cursor_of_rows = window.cursor_of_rows;
    $("#btn_undo").css("color", "blue");

    tik_tik();

    if(remember || pass) {
        row = window.rows_from_DB[window.cursor_of_rows];
        firstTimeFail = row[6];

        // 第一次背诵即成功, 背诵次数加1. 同时如果是pass, 直接置为8次
        if(!firstTimeFail) {
            row[2] = pass ? 8 : row[2] + 1; // pass为8, 否则次数加1

            // 正常计算下次提醒时间
            row[3] = cal_remind_time(row[2], "int");
            row[4] = cal_remind_time(row[2], "str");
        }
        // 第一次背诵失败, 背诵次数减1. 同时下次背诵时间按照第0次计算(即5分钟后提醒)
        else {
            row[2] = pass ? 8 : row[2] - 1; // pass为8, 否则次数减1
            row[2] = row[2] <= 0 ? 0 : row[2]; // 如果已经是负数了则调整为0次

            // 统一按照第0次计算下次提醒时间
            row[3] = cal_remind_time(0, "int");
            row[4] = cal_remind_time(0, "str");
        }

        // operate DB here
        update_row(row, false);

        window.rows_from_DB.splice(window.cursor_of_rows, 1);
        move_cursor(false);
    }
    else {
        window.rows_from_DB[window.cursor_of_rows][6] = true; // firstTimeFail: false => true
        move_cursor(true);
    }
}

function view_hujiang() {
    if(window.rows_from_DB.length <= 0) {
        return;
    }

    key_word = window.rows_from_DB[window.cursor_of_rows][0];

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

function speak_word() {
    speaker = document.getElementById("speaker");

    key_word = window.rows_from_DB[window.cursor_of_rows][0];
    secret_info = window.rows_from_DB[window.cursor_of_rows][1];

    if(is_word_EN(key_word)) {
        speaker.src = "http://tts.yeshj.com/s/" + key_word;
    }
    else {
        if(secret_info.indexOf("--") > 0) {
            key_word = secret_info.split("-")[0];
            key_word = key_word.replace(/\d/g, "");
        }
        speaker.src = "http://fanyi.baidu.com/gettts?lan=jp&text=" + key_word;
    }

    speaker.play();

    set_speaker_icon("gif");

    speaker.addEventListener('ended', function () {
        set_speaker_icon("png");
    }, false);
}

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

            local_word_id  = window.rows_from_DB[window.cursor_of_rows][5];
            remote_word_id = rec['verified_info'][0];
            remote_is_favourite = rec['verified_info'][1];
            message_str = rec['message_str'];

            // 异步处理回来后，改变收藏小图片的样式
            if(remote_word_id == local_word_id) {

                if(remote_is_favourite == 1) {
                    notie.alert(1, message_str, 2);
                    set_favourite_icon("black");
                } else {
                    notie.alert(1, message_str, 2);
                    set_favourite_icon("white");
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

function make_new_layer() {
    if(window.secret_is_hiding) {
        return;
    }

    layer.open({
        id: "iframe_edit",
        type: 2,
        title: ["修改单词", 'font-size: 20px;'],
        closeBtn: 0,
        moveEnd: function() {
            layer.close(layer.index);
        },
        shadeClose: false,
        resize: false,
        area: ['280px', '400px'],
        content: './layer_edit'
    });
}

(function() {
    init();
}());


