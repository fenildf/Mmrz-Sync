<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <!-- 可能是适配移动端用的 -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    %if need_https:
      <!-- Refer to: https://segmentfault.com/q/1010000005872734 -->
      <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    %end

    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0"/>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="format-detection" content="telephone=no">

    <script type="text/javascript" src="./js/jquery1.8.3.min.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/jquery1.4.1.cookie.min.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/utils.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/mmrz.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./layer/layer.js?{{static_file_version}}"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/mmrz.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <script type="text/javascript" src="./js/notie.js?{{static_file_version}}"></script>
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
          <span class="label" id="label_meaning" onclick="make_new_layer()"></span>
        </div>
      </div>

      <div id="btn_board">
        <button class="btn" id="btn_yes">记得住</button>
        <button class="btn" id="btn_no">记不住</button>
      </div>

      <div id="words_count">
        第 <span id="mem_times"></span> 次
        &nbsp;<a id="btn_pass" href="javascript:if(confirm('Pass 会标记该单词非常熟悉, 永远无需再次进入背诵序列.\n\n确定不再记忆此单词?')){hide_secret(true, true);show_word()}">Pass</a>
        &nbsp;<a id="btn_undo" style="color: gray" href="javascript:if(confirm('如果你手抖点错了记得住和记不住, 你可以使用本功能撤销.\n\n是否要回到上一个单词?')){restore_last_word()}">↺</a>
        <br/>
        <span id="words_left"></span>
      </div>

      <div id="uinfo_board">
        <a href="javascript:individual()" id="user_info"></a>
        <a href="javascript:if(confirm('确认退出帐号 ' + $.cookie('username') + ' ?'))logout()">注销</a>
      </div>

      <audio id="speaker" src=""></audio>

      <button id="speak_png_btn" onclick="speak_word()"></button>
      <button id="speak_gif_btn" onclick="speak_word()" style="display: none"></button>

      <button id="magnifier_btn" onclick="view_hujiang()"></button>

      <button id="favourite_star_white_btn" onclick="favourite_action()"></button>
      <button id="favourite_star_black_btn" onclick="favourite_action()" style="display: none"></button>

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
        period_state_check();

        if(is_state_cache_available()) {
          if(confirm("检测远端有未完成的背诵状态, 是否需要恢复?")) {
            restore_remote_saved_state();
          }
        }

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

      <div style="display: none;">
        <script src="https://s11.cnzz.com/z_stat.php?id=1261540749&web_id=1261540749" language="JavaScript"></script>
      </div>
    </div>
  </body>
</html>