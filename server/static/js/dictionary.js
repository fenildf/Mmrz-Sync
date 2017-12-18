// functions for dictionary.tpl

function is_word_exist(word, pronounce) {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
        word: word,
        pronounce: pronounce,
    };

    $.ajax({
        url: "/is_word_exist",
        type: "post",
        data: params,
        async: false,
        success: function(rec) {
            rec = JSON.parse(rec);
            exist = rec['exist'];
        }
    });

    return exist;
}

function change_one_word_status(idx) {
    word = getQueryString("key_word");
    pronounce = $("#PronounceJp_" + idx).text().replace('[', '').replace(']', '');
    meaning = $("#Comment_" + idx).text();
    pronounce = pronounce + " -- " + meaning;

    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
        word: word,
        pronounce: pronounce,
    }

    if(is_word_exist(word, pronounce) && !confirm("确认删除该单词?")) {
        return;
    }

    $.ajax({
        url: "/change_one_word_status",
        type: "post",
        data: params,
        async: true,
        success: function(rec) {
            rec = JSON.parse(rec);

            mmrz_code = rec['mmrz_code'];
            if(mmrz_code == window.MMRZ_CODE_Universal_Verification_Fail) {
                if(confirm("老用户请登录后添加单词, 新用户请注册后享受相应功能.")) {
                    location.href = "/login";
                }
            }
            else if(mmrz_code == window.MMRZ_CODE_Word_Save_OK) {
                set_added_icon(idx, "yes");
                notie.alert(1, "保存至单词本成功", 1.5);
            }
            else if(mmrz_code ==  window.MMRZ_CODE_Word_Remove_OK) {
                set_added_icon(idx, "no");
                notie.alert(3, "从单词本中删除成功", 1.5);
            }
            else {
                set_added_icon(idx, "none")
            }
        }
    });
}
