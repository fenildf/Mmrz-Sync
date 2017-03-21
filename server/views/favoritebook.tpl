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
    <script type="text/javascript" src="./js/favorite.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/favorite.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">

      <h2 id="title">我的收藏</h2>

      <!-- 小图片进行预加载 -->
      <span class="favourite_outline_btn favourite_christmas_btn" style="display:none"></span>

      <table style="font-size: 12px;" align="center">
        <tr>
          <th width="45px" >编号</th>
          <th width="150px">单词</th>
          <th width="400px" onclick="show_word_meaning('all')">词意<span id="word_meaning_title" style="font-size:8px">※点击显示全部</span></th>
          <th width="45px">收藏</th>
        </tr>

        %idx = 0
        %for row in rows:
          %wordID        = row[0]
          %word          = row[1]
          %pronounce     = row[2]
          %favourite     = row[3]

          %idx += 1
          <tr>
            <td>{{idx}}</td>
            <td class="td_word" onclick="jump_to_hujiang({{idx}})">{{word}}</td>
            <td class="td_favourite" onclick="show_word_meaning({{idx}})">{{pronounce}}</td>
            <td><button class="favourite_christmas_btn" onclick="favourite_action({{idx}}, {{wordID}})"></button></td>
            <input name="favourite" type="hidden" value="{{favourite}}"/>
          </tr>
        %end
      </table>
      <input name="show_word" type="hidden" value="0"/>

      <div id="copyright"></div>

      <script>
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("我的收藏 -- Debug");
        }
      </script>

      <script type="text/javascript">
        Copyright();
      </script>
    </div>
  </body>
</html>