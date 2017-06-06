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
    <script type="text/javascript" src="./js/signup.js?{{static_file_version}}"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/signup.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">注册</h2>

      <div id="center_center">
        <div class="info">
          <span class="label">帐号:</span>
        </div>

        <div class="info">
          <input class="edit_area" type="text", id="username" onkeydown="prompt_change()" onkeypress='if(event.keyCode==13){username_check()}'>
        </div>

        <div class="info">
          <span class="label">密码:</span>
        </div>

        <div class="info">
          <input class="edit_area" type="password" id="password" onkeydown="prompt_change()" onkeypress='if(event.keyCode==13){password_check()}'>
        </div>

        <div class="info">
          <span class="label">确认:</span>
        </div>

        <div class="info">
          <input class="edit_area" type="password" id="password_confirm" onkeydown="prompt_change()" onkeypress='if(event.keyCode==13){signup()}'>
        </div>

        <div class="info" id="prompt_board">
          <span id="prompt"></span>
        </div>

        <div id="btn_board">
          <button class="btn" id="signup">注册</button>
        </div>

        <div id="copyright"></div>
      </div>

      <script type="text/javascript">
        $("#username").focus();
        $("#signup").click(signup);

        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("注册 -- Debug");
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