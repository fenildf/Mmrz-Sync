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
      <p>使用的单词书: {{book_name}}</p>
      更换单词书: <button onclick="alert('上传功能尚未开放')">上传</button>
      <P>剩余单词数: {{remained_words}} / {{total_lines}}</P>
      <p>目前导入进度: {{import_rate}}%</p>
      <p>离上次导入已有: {{time_elapsed}}</p>
      导入数量(1-200): <input id="quantity" type="tel" onafterpaste="limit_import_number(this)" onkeyup="limit_import_number(this)" value="100" style="width: 30px">
      <p><a href="javascript:show_wordbook()">查看单词本</a> / <a href="javascript:if(confirm('立即从远端单词本中导入' + $('#quantity').val() + '个单词?'))online_import()">立即导入</a></p>

      <br/>
      <h3>修改密码:</h3>
      <table border="0" align="center">
        <tbody>
          <tr>
            <td align="right">当前密码:</td>
            <td align="left"><input id="password_current" type="password" style="width:135px"></td>
          </tr>
          <tr>
            <td align="right">新密码:</td>
            <td align="left"><input id="password_new" type="password" style="width:135px"></td>
          </tr>
          <tr>
            <td align="right">确认新密码:</td>
            <td align="left"><input id="password_again" type="password" style="width:135px"></td>
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