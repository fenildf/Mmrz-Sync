<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <!-- 可能是适配移动端用的 -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0"/>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="format-detection" content="telephone=no">

    <script type="text/javascript" src="./js/jquery1.8.3.min.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/jquery1.4.1.cookie.min.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/utils.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/dictionary.js?{{static_file_version}}"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css?{{static_file_version}}">
    <link rel="stylesheet" type="text/css" href="./css/dictionary.css?{{static_file_version}}">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <!-- 必须放在 body 中, 原因不明 -->
    <script type="text/javascript" src="./js/notie.js?{{static_file_version}}"></script>
    <div id="center_board">
      <h2 id="title">查单词</h2>

      <div id="center_center">
        <div class="info">
          <input class="edit_area" type="text", id="dictionary_key_word" onkeypress='if(event.keyCode==13){query_hujiang()}'>
          <button id="query" onclick="query_hujiang()">查询</button>
        </div>

        %if not defines:
          <p>查询失败: {{key_word}}</p>
        %else:
          %idx = -1
          %for define in defines:
            %idx += 1
            <p>
              <span class="PronounceJp_list" id="PronounceJp_{{idx}}">[{{define["PronounceJp"]}}]</span>
              <button class="button_yes_list" id="button_no_{{idx}}" onclick="change_one_word_status({{idx}})" style="width: 30px; height: 30px; background: url(/img/added_no.png); background-size: cover; border: 0; vertical-align: middle;"></button>
              <button class="button_no_list" id="button_yes_{{idx}}" onclick="change_one_word_status({{idx}})" style="width: 30px; height: 30px; background: url(/img/added_yes.png); background-size: cover; border: 0; vertical-align: middle;"></button>
            </p>
            <p id="Comment_{{idx}}">{{define["Comment"]}}</p>
            <hr>
          %end
        %end
          

        <div id="copyright"></div>
      </div>
    </div>

    <script type="text/javascript">
      key_word = getQueryString("key_word");
      $("#dictionary_key_word").val(key_word);

      domain = document.domain;
      if(domain == "localhost" || domain == "127.0.0.1") {
        $("#title").text("查单词 -- Debug");
      }

      function query_hujiang() {
        key_word = $("#dictionary_key_word").val();
        if(!key_word) {
          return;
        }
        else {
          location.href = "./dictionary?key_word=" + key_word;
        }
      }

      for(i = 0; i < $(".PronounceJp_list").length; i++) {
        pronounce = $("#PronounceJp_" + i).text();
        pronounce = pronounce.replace('[', '').replace(']', '');
        if(is_word_exist(key_word, pronounce)) {
          set_added_icon(i, "yes");
        }
        else {
          set_added_icon(i, "no");;
        }
      }
    </script>

    <script type="text/javascript">
        Copyright();
    </script>

    <div style="display: none;">
      <script src="https://s11.cnzz.com/z_stat.php?id=1261540749&web_id=1261540749" language="JavaScript"></script>
    </div>
  </body>
</html>