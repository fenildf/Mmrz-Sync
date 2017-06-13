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
    <script type="text/javascript" src="./js/login.js?{{static_file_version}}"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css?{{static_file_version}}">
    <link rel="stylesheet" type="text/css" href="./css/login.css?{{static_file_version}}">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">登录</h2>

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
          <input class="edit_area" type="password" id="password" onkeydown="prompt_change()" onkeypress='if(event.keyCode==13){login()}'>
        </div>

        <div class="info" id="prompt_board">
          <span id="prompt"></span>
        </div>

        <div id="btn_board">
          <button class="btn" id="submit">登录</button>
          <button class="btn" id="signup">注册</button>
        </div>

        <div id="copyright"></div>
      </div>
    </div>

    <script type="text/javascript">
      $("#username").focus();
      $("#submit").click(login);
      $("#signup").click(function(){window.open("/signup")});

      domain = document.domain;
      if(domain == "localhost" || domain == "127.0.0.1") {
        $("#title").text("登录 -- Debug");
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