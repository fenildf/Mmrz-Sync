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
    <script type="text/javascript" src="./js/utils.js?v=1000"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css">
    <link rel="stylesheet" type="text/css" href="./css/edit.css">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <div id="center_center">
        <div class="info">
          <span class="label">单词:</span>
        </div>

        <div class="info">
          <textarea class="edit_area" wrap="physical" id="word"></textarea>
        </div>

        <div class="info">
          <span class="label">发音:</span>
        </div>

        <div class="info">
          <textarea class="edit_area" wrap="physical" id="pronounce"></textarea>
        </div>

        <div class="info">
          <span class="label">解释:</span>
        </div>

        <div class="info">
          <textarea class="edit_area_big" id="meaning"></textarea>
        </div>

        <div id="btn_board">
          <button class="btn" id="confirm" onclick="update_word_info()">修改</button>
          <button class="btn" id="cancel" onclick="parent.layer.close(parent.layer.index)">取消</button>
        </div>

        <div id="copyright"></div>
      </div>

      <script type="text/javascript">
        function update_word_info() {
          word = $("#word").val();
          pronounce = $("#pronounce").val();
          meaning = $("#meaning").val();
          combine = pronounce + " -- " + meaning;

          word_from_db = parent.window.rows_from_DB[parent.window.cursor_of_rows][0];
          combine_from_db = parent.window.rows_from_DB[parent.window.cursor_of_rows][1];

          modified = false;
          if(word != word_from_db) modified = true;
          if(combine != combine_from_db) modified = true;

          if(modified) {
            parent.window.rows_from_DB[parent.window.cursor_of_rows][0] = word;
            parent.window.rows_from_DB[parent.window.cursor_of_rows][1] = combine;
            parent.update_row(parent.window.rows_from_DB[parent.window.cursor_of_rows], true);
            parent.show_word();
            parent.show_secret();
            parent.layer.close(parent.layer.index);
            parent.layer.msg("修改单词信息成功!");
          }
          else {
            parent.layer.close(parent.layer.index);
            parent.layer.msg("未修改任何内容!");
          }
        }
      </script>

      <script type="text/javascript">
        word = parent.window.rows_from_DB[parent.window.cursor_of_rows][0];
        combine = parent.window.rows_from_DB[parent.window.cursor_of_rows][1];
        if(combine.search("--") > 0) {
          combine = combine.split("--");
          pronounce = combine[0].replace(" ", "");
          meaning = combine[1].replace(" ", "");
        }
        else {
          pronounce = "";
          meaning = combine;
        }

        $("#word").val(word);
        $("#pronounce").val(pronounce);
        $("#meaning").val(meaning);
      </script>

      <div style="display: none;">
        <script src="https://s11.cnzz.com/z_stat.php?id=1261540749&web_id=1261540749" language="JavaScript"></script>
      </div>
    </div>
  </body>
</html>