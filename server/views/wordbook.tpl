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
    <script type="text/javascript" src="./js/wordbook.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/wordbook.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">

      <h2 id="title">单词本</h2>

      <h3>库中共计 {{word_quantity}} 个单词</h3>
      <h3>当前提取 {{len(rows)}} 个单词</h3>
      <a href="javascript:location.href='/wordbook?username=' + $.cookie('username') + '&show_all=yes'">点击提取全部单词</a>

      %for row in rows:
        %word          = row[0]
        %pronounce     = row[1]
        %memTimes      = row[2]
        %remindTime    = row[3]
        %remindTimeStr = row[4]
        %wordID        = row[5]

        <p>{{wordID}} => next: {{remindTimeStr}}, {{memTimes}} times, {{word}}, {{pronounce}}</p>
      %end

      <div id="copyright"></div>

      <script>
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("单词本 -- Debug");
        }
      </script>

      <script type="text/javascript">
        Copyright();
      </script>
    </div>
  </body>
</html>