// functions for dictionary.tpl

function is_word_exist() {
    params = {
        username: $.cookie('username'),
        password: $.cookie('password'),
        word: 'こわごわ',
        pronounce: 'こわごわ -- 提心吊胆、心惊胆战',
    };

    $.ajax({
        url: "/is_word_exist",
        type: "post",
        data: params,
        async: false,
        success: function(rec) {
            console.log(rec);
        }
    });
}
