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
    let ul = document.querySelector("ul");
    while (ul.firstChild) {
      ul.removeChild(ul.firstChild);
    }

    for (let i = 0; i < data.length; i++) {
      let li = document.querySelector("li.hidden.block");
      let new_li = li.cloneNode(true);

      let a = new_li.querySelector('a');
      a.href = '/static/embedding/' + data[i].name
      a.target = 'blank'
      a.innerHTML = data[i].name.split("/").slice(-1)[0].substring(16);

      let doc_p = new_li.querySelector("p");
      doc_p.innerHTML = doc_p.innerHTML + data[i].summarization;
      doc_p.addEventListener("click", summary_toggle);
      doc_p.nextElementSibling.addEventListener("click", summary_toggle);

      new_li.classList.remove("hidden");
      ul.append(new_li);
    }

    if (data.length == 0) {
      let li = document.querySelector("li.hidden.none");
      let new_li = li.cloneNode(true);
      new_li.classList.remove("hidden");
      ul.append(new_li);
    }
  });
}

function summary_toggle(e) {
  let li = e.target.parentElement;
  let p = li.querySelector("p");
  if (p.classList.contains("summary-p")) {
    p.classList.remove("summary-p");
  } else {
    p.classList.add("summary-p");
  }
  let div = li.querySelector("div.summary-shadow");
  if (div.classList.contains("hidden")) {
    div.classList.remove("hidden");
  } else {
    div.classList.add("hidden");
  }
}

function add_doc_async() {
  let original_pdf = document.querySelector("input[name='file_f']");
  let model = $("select[name='character']");
  let csrf = $("input[name='csrfmiddlewaretoken']");

  const request_data = new FormData();
  request_data.append('model', model.val());
  request_data.append('csrfmiddlewaretoken', csrf.val());
  if (original_pdf.files.length > 0) {
    for (let index = 0; index < original_pdf.files.length; index++) {
      request_data.append('original_pdf_' + index, original_pdf.files[index]);
    }
  }
  fetch("/embedding_add_doc_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    console.log(response);
    fetch_documents();
  });
}

function wuxi_init() {
  let add_doc_button = document.querySelector("button[name='modal_button']");
  add_doc_button.addEventListener("click", function (e) {
    add_doc_async();
  });

  let selecor = document.querySelector("select");
  selecor.addEventListener("change", function (e) {
    fetch_documents();
  });

  fetch_documents();
}

$(document).ready(function () {
  wuxi_init();
})