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
    <script type="text/javascript" src="./js/welcome.js?{{static_file_version}}"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css?{{static_file_version}}">
    <link rel="stylesheet" type="text/css" href="./css/welcome.css?{{static_file_version}}">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">Mmrz</h2>

      <div id="center_center">
        <div class="info">
          <p>Memorize, 随时随地记单词 !</p>
          <hr>
          新用户: <a href="./signup">注册</a>
          已有帐号: <a href="./login">登录</a>
        </div>
        <div id="copyright"></div>
      </div>
    </div>

    <script type="text/javascript">
      domain = document.domain;
      if(domain == "localhost" || domain == "127.0.0.1") {
        $("#title").text("Mmrz -- Debug");
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