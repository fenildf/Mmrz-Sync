// functions for individual.tpl

function show_wordbook() {
    window.open("/wordbook?username=" + $.cookie('username'));
}

function show_favoritebook() {
    window.open("/favoritebook?username=" + $.cookie('username'));
}

function show_setting() {
    window.open("/setting?username=" + $.cookie('username'));
}

function upload_file() {
    if(is_cellphone()) {
        alert("不支持移动端上传词典, 请使用电脑上传");
        return;
    }

    $("#username").val($.cookie("username"));
    $("#password").val(window.btoa($.cookie("password")));

    file_input = document.getElementById("file_input");
    file_input.click();

    file_input.onchange = function() {
        file_ext = file_input.value.split('.').pop().toLowerCase();
        if(file_ext != "mmz" && file_ext != "yb") {
            alert("仅支持 *.mmz 和 *.yb 上传");
            return;
        }

        if(file_input.files[0].size > 1024 * 1024 * 5) {
            alert("不可上传大于 5Mb 的文件");
            return;
        }

        oData = new FormData(document.forms.namedItem("file_upload_form"));
        oReq = new XMLHttpRequest();  
        oReq.open("POST", "/upload_lexicon" , true);
        oReq.send(oData);

        oReq.upload.onprogress = function(event){
            rate = Math.floor(100 * event.loaded / event.total);
        }

        oReq.onload = function(oEvent) {
            if (oReq.status == 200) {
                alert("上传成功");
            }
            else {
                alert("上传失败");
            }
            location.reload(true);
        };
    }
}

function online_import() {
    if($("#lexicon_in_use").text().indexOf("--") >= 0) {
        alert("尚未上传单词本, 请先上传一个单词本");
        return;
    }

    if($("#quantity").val() == "") {
        alert("导入数量不能为空");
        return;
    }

    if(Number($("#quantity").val()) == 0) {
        alert("不能导入0个单词");
        return;
    }

    params = {
        username: $.cookie('username'),
        password: window.btoa($.cookie('password')),
        quantity: Number($("#quantity").val()),
    }

    $.post('/online_import', params, function(rec) {
        rec = JSON.parse(rec);
        added = rec['added'];
        alert("本次成功导入" + Number(added) + "个单词");
        location.reload(true);
    });
}

function limit_import_number(self) {
    self.value = self.value.replace(/[^0-9]/g, "");
    self.value = (self.value > 200 ? 200 : self.value);
    self.value = (self.value <   0 ?  "" : self.value);
}

(function() {
    if(!verify_user($.cookie('username'), $.cookie('password'))) {
        location.href="/";
    }
}());