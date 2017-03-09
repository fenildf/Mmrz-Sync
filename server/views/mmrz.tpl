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

    <script type="text/javascript" src="./js/jquery1.8.3.min.js"></script>
    <script type="text/javascript" src="./js/jquery1.4.1.cookie.min.js"></script>
    <script type="text/javascript" src="./js/utils.js"></script>
    <script type="text/javascript" src="./js/mmrz.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/mmrz.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">背诵模式</h2>

      <div class="info">
        <span class="label" id="label_word"></span>
      </div>

      <div class="info" id="view_board">
        <div>
          <button class="btn" id="btn_view">查看</button>
        </div>
        <div>
          <span class="label" id="label_meaning"></span>
        </div>
      </div>

      <div id="btn_board">
        <button class="btn" id="btn_yes">记得住</button>
        <button class="btn" id="btn_no">记不住</button>
      </div>

      <div id="words_count">
        第 <span id="mem_times"></span> 次
        &nbsp;<a id="btn_pass" href="javascript:if(confirm('Pass 会标记该单词非常熟悉, 永远无需再次进入背诵序列.\n\n确定不再记忆此单词?')){hide_secret(true, true);show_word()}">Pass</a>
        <br/>
        <span id="words_left"></span>
      </div>

      <div id="uinfo_board">
        <a href="javascript:individual()" id="user_info"></a>
        <a href="javascript:if(confirm('确认退出帐号 ' + $.cookie('username') + ' ?'))logout()">注销</a>
      </div>

      <audio id="speaker" src=""></audio>

      <button id="speak_btn" onclick="speak_word()"></button>
      <button id="magnifier_btn" onclick="view_hujiang()"></button>
      <button id="favourite_btn" onclick="favourite_action()"></button>

      <div id="copyright"></div>

      <script type="text/javascript">
        KEY_UP    = 38;
        KEY_DOWN  = 40;
        KEY_LEFT  = 37;
        KEY_RIGHT = 39;

        $("#btn_view").css("display", "none");
        $("#btn_yes").css("display", "none");
        $("#btn_no").css("display", "none");

        // UP key: show_word
        $(document).keydown(function(event) {
          if(event.keyCode == KEY_UP) {
            show_word();
          }
        });

        // DOWN key: btn_view
        $(document).keydown(function(event) {
          if(event.keyCode == KEY_DOWN) {
            show_secret();
          }
        });

        // LEFT key: btn_yes
        $(document).keydown(function(event) {
          if(event.keyCode == KEY_LEFT && window.secret_is_showing) {
            hide_secret(true, false);
            show_word();
          }
        });

        // RIGHT key: btn_no
        $(document).keydown(function(event) {
          if(event.keyCode == KEY_RIGHT && window.secret_is_showing) {
            hide_secret(false, false);
            show_word();
          }
        });


        $("#btn_view").click(
          function () {
            show_secret();
          }
        );

        $("#btn_yes").click(
          function () {
            hide_secret(true, false);
            show_word();
          }
        );

        $("#btn_no").click(
          function () {
            hide_secret(false, false);
            show_word();
          }
        );

        function view_hujiang() {
          if(window.rows_from_DB.length <= 0) {
            return;
          }

          key_word = window.rows_from_DB[window.cursor_of_rows][0];

          if(is_word_JA(key_word)) {
            window.open("http://dict.hjenglish.com/jp/jc/" + key_word);
          }
          else if(is_word_EN(key_word)) {
            window.open("http://dict.hjenglish.com/w/" + key_word);
          }
          else {
            console.log("can't recognize");
          }
        }

        function speak_word() {
          speaker = document.getElementById("speaker");

          // 如果 speaker.src 尚未赋值, 则设置为全局 window.word_tts_url (此时会有网络访问)
          if(speaker.src == window.location.href) {
            key_word = window.rows_from_DB[window.cursor_of_rows][0];
            secret_info = window.rows_from_DB[window.cursor_of_rows][1];

            if(is_word_JA(key_word)) {
              if(secret_info.indexOf("--") > 0) {
                key_word = secret_info.split("-")[0];
              }

              speaker.src = "http://fanyi.baidu.com/gettts?lan=jp&text=" + key_word;
            }
            else if(is_word_EN(key_word)) {
              speaker.src = "http://tts.yeshj.com/s/" + key_word;
            }
            else {
              console.log("can't recognize");
            }
          }

          speaker.play();
          $("#speak_btn").css("background", 'url(/img/speaker.gif)').css("background-size", 'cover');

          speaker.addEventListener('ended', function () {  
            $("#speak_btn").css("background", 'url(/img/speaker.png)').css("background-size", 'cover');
          }, false);
        }
      </script>

      <script type="text/javascript">
        show_word();

        $("#user_info").text($.cookie('username'));

        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("背诵模式 -- Debug");
        }
      </script>

      <script type="text/javascript">
        function individual() {
          window.open("/individual?username=" + $.cookie('username'));
        }
      </script>

      <script type="text/javascript">
        Copyright();
      </script>
    </div>
  </body>
</html>