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
      <p>使用的单词书: N1.yb</p>
      <p>目前导入进度: 12.32%</p>
      <p>最近导入: 2017-1-19 09:18:45</p>
      <p><a href="javascript:if(confirm('立即导入远端单词本?'))online_import()">立即导入</a></p>

      <br/>
      <h3>功能区:</h3>
      <p><a href="javascript:alert('修改密码功能尚未开放')">修改密码</a></p>

      <div id="copyright"></div>

      <script>
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("个人信息 -- Debug");
        }
      </script>

      <script type="text/javascript">
        copyright.innerHTML = "&copy; 2016-" + (new Date()).getFullYear() + " by <a style='color: black; text-decoration: underline;' target='_blank' href='http://zhanglintc.co'>zhanglintc</a>";
      </script>
    </div>
  </body>
</html>