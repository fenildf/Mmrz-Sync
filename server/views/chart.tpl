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

    <script type="text/javascript" src="./js/jquery1.8.3.min.js?v=1000"></script>
    <script type="text/javascript" src="./js/jquery1.4.1.cookie.min.js?v=1000"></script>
    <script type="text/javascript" src="./js/chart.min.js?v=1000"></script>
    <script type="text/javascript" src="./js/utils.js?v=1000"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/mmrz.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">背诵时间</h2>
      <div style="width: 300px; margin: auto;">
        <canvas id="weekly_chart"></canvas>
      </div>

      <div id="copyright"></div>

      <script type="text/javascript">
        make_weekly_chart($("#weekly_chart"), get_weekly_mmrz_time(getQueryString("username")))
      </script>
      <script type="text/javascript">
        $("#title").text("背诵时间 -- " + getQueryString("username"));

        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("背诵时间 -- " + getQueryString("username") + " -- Debug");
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


