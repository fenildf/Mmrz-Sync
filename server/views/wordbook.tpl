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
    <script type="text/javascript" src="./js/jquery.twbsPagination.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/utils.js?{{static_file_version}}"></script>
    <script type="text/javascript" src="./js/wordbook.js?{{static_file_version}}"></script>

    <link rel="stylesheet" type="text/css" href="./css/common.css?{{static_file_version}}">
    <link rel="stylesheet" type="text/css" href="./css/wordbook.css?{{static_file_version}}">

    <link rel="shortcut icon" href="./fav.ico"/>
    <link rel="bookmark" href="./fav.ico"/>

    <title>Mmrz</title>
  </head>

  <body>
    <div id="center_board">
      <br/>
      <h3 id="title" style="margin:auto;">单词本</h3>
      <br/>

      <div style="margin:auto;">
        <span style="font-size: 13px">当前提取 {{len(rows)}} / {{word_quantity}} 个单词</span>
        <br/>

        <ul id="pagination-demo" class="pagination-sm"></ul>
      </div>

      <table style="font-size: 11px;" align="center">
        <tr>
          <th width="40px">编号</th>
          <th width="130px">时间</th>
          <th width="45px">次数</th>
          <th width="135px">单词</th>
          <th width="300px">词意</th>
        </tr>

        %idx = rows_start
        %for row in rows:
          %word          = row[0]
          %pronounce     = row[1]
          %memTimes      = row[2]
          %remindTime    = row[3]
          %remindTimeStr = row[4]
          %wordID        = row[5]

          %idx += 1
          <tr>
            <td>{{idx}}</td>
            <td>{{remindTimeStr}}</td>
            <td>{{memTimes}}</td>
            <td>{{word}}</td>
            <td style="word-wrap: break-word;">{{pronounce}}</td>
          </tr>
        %end
      </table>

      <div style="margin:auto;">
        <span style="font-size: 13px">当前提取 {{len(rows)}} / {{word_quantity}} 个单词</span>
        <br/>

        <ul id="pagination-demo" class="pagination-sm"></ul>
      </div>

      <div id="copyright"></div>

      <script>
        domain = document.domain;
        if(domain == "localhost" || domain == "127.0.0.1") {
          $("#title").text("单词本 -- Debug");
        }

        page_max = {{page_max}};
        visiblePages = page_max > 5 ? 5 : page_max;

        url_page = Number(getQueryString("page"));
        url_page = url_page <= 1 ? 1 : url_page;

        $('#pagination-demo').twbsPagination({
          totalPages: page_max,
          visiblePages: visiblePages,
          version: '1.1',
          startPage: url_page,
          first: '<<',
          prev: '',
          next: '',
          last: '>>',
          onPageClick: function (event, page) {
            if(url_page != page) {
              location.href = "./wordbook?username=" + $.cookie("username") +"&page=" + page;
            }

            if(url_page <= 1) {
              $('.first').toggleClass('disabled')
              $('.prev').toggleClass('disabled')
            }
            else if (url_page == page_max) {
              $('.next').toggleClass('disabled')
              $('.last').toggleClass('disabled')
            }
          }
        });

        if(url_page <= 1) {
          $('.first').toggleClass('disabled')
          $('.prev').toggleClass('disabled')
        }
        else if (url_page == page_max) {
          $('.next').toggleClass('disabled')
          $('.last').toggleClass('disabled')
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
