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

    <link rel="stylesheet" type="text/css" href="./css/style.css">

    <script type="text/javascript" src="./js/utils.js"></script>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">Mmrz 网页版</h2>

      <div class="info">
        <span>帐号:</span>
        <br>
        <input type="text", id="username">
        <br>
      </div>

      <div class="info">
        <span>密码:</span>
        <br>
        <input type="password" id="password">
      </div>

      <div class="btn">
        <button id="submit">登录</button>
        <button id="signup">注册</button>
      </div>

      <div id="copyright"></div>

      <script type="text/javascript">
        submit.onclick = function() {
          params = {
            username: document.getElementById("username").value,
            password: window.btoa(document.getElementById("password").value),
          }

          post("/log_in", params);
        }
      </script>

      <script type="text/javascript">
        copyright.innerHTML = "&copy; 2016-" + (new Date()).getFullYear() + " by zhanglintc";
      </script>
    </div>
  </body>
</html>