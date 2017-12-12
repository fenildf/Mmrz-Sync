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
            console.log(rec);
            rec = JSON.parse(rec);
            exist = rec['exist'];
        }
    });

    return exist;
}
