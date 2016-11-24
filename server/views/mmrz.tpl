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
    <script type="text/javascript" src="http://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
    <script type="text/javascript" src="./js/utils.js"></script>
    <script type="text/javascript" src="./js/mmrz.js"></script>

    <link rel="stylesheet" type="text/css" href="./css/mmrz.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz 网页版</title>
  </head>

  <body>
    <div id="center_board">
      <h2 id="title">背诵模式</h2>

      <div class="info">
        <span class="label" id="label_word">味わう</span>
      </div>

      <div class="info" id="view_board">
        <div>
          <button class="btn" id="btn_view">查看</button>
        </div>
        <div>
          <span class="label" id="label_meaning"></span>
        </div>
      </div>

      <div id="btn_board">
        <button class="btn" id="btn_yes">记得住</button>
        <button class="btn" id="btn_no">记不住</button>
      </div>

      <div id="uinfo_board">
        <span id="user_info"></span>
        <a href="javascript:if(confirm('确认退出帐号 ' + $.cookie('username') + ' ?'))logout()">注销</a>
      </div>

      <div id="copyright"></div>

      <script type="text/javascript">
        $("#btn_yes").css("display", "none");
        $("#btn_no").css("display", "none");

        $("#btn_view").click(
          function () {
            $("#btn_view").css("display", "none");
            $("#btn_yes").css("display", "");
            $("#btn_no").css("display", "");
            $("#label_meaning").text("あじわう -- 品尝")
          }
        );

        $("#btn_yes").click(
          function () {
            $("#btn_view").css("display", "");
            $("#btn_yes").css("display", "none");
            $("#btn_no").css("display", "none");
            $("#label_meaning").text("")
          }
        );

        $("#btn_no").click(
          function () {
            $("#btn_view").css("display", "");
            $("#btn_yes").css("display", "none");
            $("#btn_no").css("display", "none");
            $("#label_meaning").text("")
          }
        );
      </script>

      <script>
        $("#user_info").text($.cookie('username'));
      </script>

      <script type="text/javascript">
        copyright.innerHTML = "&copy; 2016-" + (new Date()).getFullYear() + " by zhanglintc";
      </script>
    </div>
  </body>
</html>