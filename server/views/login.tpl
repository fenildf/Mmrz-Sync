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

    <link rel="stylesheet" type="text/css" href="./css/login.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz 网页版</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">Mmrz 网页版</h2>

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

      <script type="text/javascript">
        $("#username").focus();
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("Mmrz -- Debug");
        }

        prompt_change = function() {
          $("#prompt").text("");
          $("#username").css("background-color", "white");
          $("#password").css("background-color", "white");
        }

        username_check = function() {
          if($("#username").val() == "") {
            $("#prompt").text("不能为空")
            $("#username").css("background-color", "#ffb6c1");
            $("#username").focus();
            return false;
          }
          else {
            $("#prompt").text("")
            $("#password").focus();
            return true;
          }
        }

        login = function() {
          if(!username_check()) {
            return;
          }

          if($("#password").val() == "") {
            $("#prompt").text("不能为空")
            $("#password").css("background-color", "#ffb6c1");
            $("#password").focus();
            return;
          }

          params = {
            username: $("#username").val(),
            password: window.btoa($("#password").val()),
          }

          // post("/log_in", params);
          $.post('/log_in', params, function(rec) {
            rec = JSON.parse(rec);
            if(rec['verified'] == true) {
              location.href="/memorize";
            }
            else {
              $("#prompt").text("帐号或密码不正确");
            }
          });
        }
        submit.onclick = login;
      </script>

      <script type="text/javascript">
        copyright.innerHTML = "&copy; 2016-" + (new Date()).getFullYear() + " by zhanglintc";
      </script>
    </div>
  </body>
</html>