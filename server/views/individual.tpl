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
    <script type="text/javascript" src="./js/chart.min.js"></script>
    <script type="text/javascript" src="./js/utils.js"></script>
    <script type="text/javascript" src="./js/individual.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/individual.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">

      <h2 id="title">个人信息</h2>

      <h3>单词导入区:</h3>
      <p id="lexicon_in_use">使用中的词典: {{book_name}}</p>
      上传并更换词典: <button onclick="if(confirm('上传词典将删除当前使用中词典, 请谨慎操作.\n\n注意: 请务必上传 utf-8 格式的词典.\n\n确认继续上传?'))upload_file()">点击上传</button>
      <form id="file_upload_form" action="/upload_file_for_import" method="post" style="display: none" enctype="multipart/form-data">
        <input id="username" type="text" name="username">
        <input id="password" type="password" name="password">
        <input id="file_input" type="file" name="wordfile">
        <input id="submit" type="submit">
      </form>
      <P>剩余单词数: {{remained_words}} / {{total_lines}}</P>
      <p>目前导入进度: {{import_rate}}%</p>
      <p>离上次导入已有: {{time_elapsed}}</p>
      导入数量(1-200): <input id="quantity" type="tel" onafterpaste="limit_import_number(this)" onkeyup="limit_import_number(this)" value="100" style="width: 30px">
      <p><a href="javascript:if(confirm('立即从远端单词本中导入' + $('#quantity').val() + '个单词?'))online_import()">立即导入</a></p>
      
      <hr>

      <h3>本周背诵统计:</h3>
      <div style="width: 300px; margin: auto;">
        <canvas id="weekly_chart"></canvas>
      </div>

      <button id="show_setting_btn" onclick="show_setting()"></button>
      <button id="show_favourite_btn" onclick="show_favoritebook()"></button>
      <button id="show_wordbook_btn" onclick="show_wordbook()"></button>

      <div id="copyright"></div>

      <script type="text/javascript">
        make_weekly_chart($("#weekly_chart"), get_weekly_mmrz_time($.cookie('username')));

        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("个人信息 -- Debug");
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