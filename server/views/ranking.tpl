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

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/ranking.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">

      <h2 id="title">用户信息汇总</h2>

      <table align="center">
        <tr>
          <th>用户</th>
          <th>最后活跃</th>
          <th>单词</th>
          <th>本周背诵</th>
        </tr>
        %for user in db_info_list:
          <tr>
            <td><a style="color: black;" target="_blank" href="/chart?&username={{user[0]}}">{{user[0]}}</a></td>
            <td>{{user[1]}}</td>
            <td>{{user[2]}}</td>
            <td>{{user[3]}}</td>
          </tr>
        %end
      </table>

      <br/>
      <hr>

      <h3>奋斗日榜(单位: 分钟)</h3>
      <p>{{date}}</p>
      <div style="width: 300px; margin: auto;">
        <canvas id="daily_ranking"></canvas>
      </div>

      <h3>奋斗周榜(单位: 分钟)</h3>
      <p>{{week}}</p>
      <div style="width: 300px; margin: auto;">
        <canvas id="weekly_ranking"></canvas>
      </div>

      <h3>奋斗月榜(单位: 分钟)</h3>
      <p>{{month}}</p>
      <div style="width: 300px; margin: auto;">
        <canvas id="monthly_ranking"></canvas>
      </div>

      <h3>奋斗年榜(单位: 分钟)</h3>
      <p>{{year}}</p>
      <div style="width: 300px; margin: auto;">
        <canvas id="yearly_ranking"></canvas>
      </div>

      <div id="copyright"></div>

      <script>
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("用户信息汇总 -- Debug");
        }

        make_ranking_chart($("#daily_ranking"),   get_ranking_info("day"));
        make_ranking_chart($("#weekly_ranking"),  get_ranking_info("week"));
        make_ranking_chart($("#monthly_ranking"), get_ranking_info("month"));
        make_ranking_chart($("#yearly_ranking"),  get_ranking_info("year"));
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
