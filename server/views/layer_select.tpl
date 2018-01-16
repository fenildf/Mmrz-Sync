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

    <link rel="stylesheet" type="text/css" href="./css/common.css?{{static_file_version}}">
    <link rel="stylesheet" type="text/css" href="./css/layer_select.css?{{static_file_version}}">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <div id="center_center">
        <div class="info">
          <span class="label">预置词典:</span>
        </div>

        <div class="info">
          <select id="lexicon_list" onchange="change_line_displayer()" style="width: 100%; height: 30px; font: 18px">
            %for lexicon_id, lexicon in lexicon_dict.items():
              <option value="{{lexicon_id}}" lines="{{lexicon[1]}}">{{lexicon[0]}}</option>
            %end
          </select>
        </div>

        <div style="margin-top: 10px">
          <span id="line_displayer" style="font-size: 12px">共计 {{lexicon_dict['lexicon_0'][1]}} 个单词</span>
        </div>

        <div id="btn_board">
          <button class="btn" id="confirm" onclick="if(confirm('确认要使用该词典替换当前词典吗?')){parent.select_lexicon($('#lexicon_list').find('option:selected').val(), $('#lexicon_list').find('option:selected').text());parent.layer.close(parent.layer.index)}">确定</button>
          <button class="btn" id="cancel" onclick="parent.layer.close(parent.layer.index)">取消</button>
        </div>

        <div id="copyright"></div>
      </div>

      <script type="text/javascript">
        function change_line_displayer() {
          $('#line_displayer').text("共计 " + $('#lexicon_list').find('option:selected').attr("lines") + " 个单词");
        }
      </script>

      <div style="display: none;">
        <script src="https://s11.cnzz.com/z_stat.php?id=1261540749&web_id=1261540749" language="JavaScript"></script>
      </div>
    </div>
  </body>
</html>


