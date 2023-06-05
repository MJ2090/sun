function fetch_documents() {
  let model = $("select[name='character']");
  let csrf = $("input[name='csrfmiddlewaretoken']");

  const request_data = new FormData();
  request_data.append('model', model.val());
  request_data.append('csrfmiddlewaretoken', csrf.val());
  fetch("/embedding_fetch_model_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    let data = response.result;
    let ol = document.querySelector("ol");
    let li = document.querySelector("li.hidden");
    while (ol.firstChild) {
      ol.removeChild(ol.firstChild);
    }

    for (let i = 0; i < data.length; i++) {
      let new_li = li.cloneNode();
      new_li.classList.remove("hidden");
      new_li.innerHTML = data[i].split("/").slice(-1)[0].substring(16);
      ol.append(new_li);
    }

    console.log(data);
  });
}

$(document).ready(function () {
  fetch_documents();
})