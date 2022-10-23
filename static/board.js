  $(document).ready(function () {
        show_board();
      });

      function show_board() {
        $("#contents-body").empty();

        $.ajax({
          type: "GET",
          url: "/guhaejo",
          data: {},
          success: function (response) {
            let rows = response["board_list"];
            for (i = 0; i < rows.length; i++) {
              let post_num = rows[i]["post_num"];
              let tag = rows[i]["tag"];
              let title = rows[i]["title"];
              let nickname = rows[i]["nickname"];
              let view_count = rows[i]["view-count"];
              let tempHtml = `<tr>
                <td>
                  <span class="list__num"> ${post_num} </span>
                </td>
                <td>
                  <span class="list__type"> ${tag} </span>
                </td>
                <td>
                  <span class="list__title">
                    <a href="/page/${post_num}">${title}</a>
                  </span>
                </td>
                <td>
                  <span class="list__writer"> ${nickname} </span>
                </td>
                <td>
                  <span class="list__view">${view_count}</span>
                </td>
              </tr>`;
              $("#contents-body").append(tempHtml);
            }
          },
        });
      }