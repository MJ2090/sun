function confirmSubmit(obj) {
  let s = $("#id_message").val();
  let money = s.length / 1000 / 100.0
  if (confirm(`The text length is ${s.length}, which will roughly cost $${money}, continue?`)) {
    return true;
  }
  return false;
}