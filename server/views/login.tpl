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

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="./js/utils.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/style.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">Mmrz 网页版</h2>

      <div class="info">
        <span>帐号:</span>
        <br>
        <input type="text", id="username" onkeypress='if(event.keyCode==13){$("#password").focus()}'>
        <br>
      </div>

      <div class="info">
        <span>密码:</span>
        <br>
        <input type="password" id="password" onkeypress='if(event.keyCode==13){login()}'>
      </div>

      <div class="btn">
        <button id="submit">登录</button>
        <button id="signup">注册</button>
      </div>

      <div id="copyright"></div>

      <script type="text/javascript">
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("Mmrz 网页版 [debug]");
        }

        login = function() {
          if($("#username").val() == "") {
            alert("请输入账号");
            $("#username").focus();
            return;
          }
          if($("#password").val() == "") {
            alert("请输入密码");
            $("#password").focus();
            return;
          }

          params = {
            username: $("#username").val(),
            password: window.btoa($("#password").val()),
          }

          post("/log_in", params);
        }
        submit.onclick = login;
      </script>

      <script type="text/javascript">
        copyright.innerHTML = "&copy; 2016-" + (new Date()).getFullYear() + " by zhanglintc";
      </script>
    </div>
  </body>
</html>