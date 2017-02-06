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
        <a id="btn_pass" href="javascript:if(confirm('确定不再记忆此单词?')){hide_secret(true, true);show_word()}">Pass</a>
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
        <span id="words_left"></span>
        <a href="javascript:if(confirm('将在新页面中打开单词本'))show_wordbook()">单词本</a>
      </div>

      <div id="uinfo_board">
        <a href="javascript:individual()" id="user_info"></a>
        <a href="javascript:if(confirm('确认退出帐号 ' + $.cookie('username') + ' ?'))logout()">注销</a>
      </div>

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
          function show_wordbook() {
            window.open("/wordbook?username=" + $.cookie('username'));
          }

          function individual() {
            if($.cookie('username') == "zhanglin" || $.cookie('username') == "smile") {
              if(confirm('将在新页面中查看个人信息'))window.open("/individual?username=" + $.cookie('username'));
            }
            else {
              alert("该功能尚未开放");
            }
          }
      </script>

      <script type="text/javascript">
        Copyright();
      </script>
    </div>
  </body>
</html>