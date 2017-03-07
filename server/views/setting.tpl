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
    <script type="text/javascript" src="./js/setting.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">

      <h2 id="title">个人设定</h2>

      <div align="center" style="margin-bottom: 10px"><b style="font-size:18px;">修改密码</b></div>
      <table border="0" align="center">
        <tbody>
          <tr>
            <td align="right">当前密码:</td>
            <td align="left"><input id="password_current" type="password" style="width: 135px"></td>
          </tr>
          <tr>
            <td align="right">新密码:</td>
            <td align="left"><input id="password_new" type="password" style="width: 135px"></td>
          </tr>
          <tr>
            <td align="right">确认新密码:</td>
            <td align="left"><input id="password_again" type="password" style="width: 135px"></td>
          </tr>

          <tr>
            <td>
              <div id="#prompt"></div>
            </td>
            <td align="right">
              <div>
                <button class="btn" onclick="update_password()" style="margin-top: 5px; font-size: 14px">更改密码</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div id="copyright"></div>

      <script type="text/javascript">
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("个人设定 -- Debug");
        }

        if(getQueryString("username") != $.cookie("username")) {
          location.href = "/";
        }
      </script>

      <script type="text/javascript">
        Copyright();
      </script>
    </div>
  </body>
</html>