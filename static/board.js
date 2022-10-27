$(document).ready(function () {
        show_board();
 });

function show_board() {
  $("#contents-body").empty();
}
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
      let view_count = rows[i]["view_count"];
      let content = rows[i]["content"];
      let tempHtml = `<tr>
        <td>
          <span class="list__num"> ${post_num} </span>
        </td>
        <td>
          <span class="list__type"> ${tag} </span>
        </td>
        <td onclick="show_content('${tag}','${title}','${nickname}','${content}')">
          <span class="list__title">
            ${title}
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
  },}
);

function hidden_article(){
$("#main-screen__contents-list__table")[0].style.display="flex";
$("#main-screen__contents-list__acticle")[0].style.display="none";
}

function show_content(tag,title,nickname,content) {
$("#main-screen__contents-list__table")[0].style.display="none";
$("#main-screen__contents-list__acticle")[0].style.display="flex";
$("#main-screen__contents-list__acticle").empty();
let tempHtml = `<div id="main-screen__contents-list__acticle__exit" onclick="hidden_article()"><i class="fa-solid fa-xmark"></i></div>
              <div id="main-screen__contents-list__acticle__title">[${tag}]${title}</div>
              <div id="main-screen__contents-list__acticle__headline">${nickname} | <i class="fa-solid fa-comment"></i>5 <i class="fa-regular fa-eye"></i>110</div>
              <div id="main-screen__contents-list__acticle__content">${content}</div>`

$("#main-screen__contents-list__acticle").append(tempHtml);

}