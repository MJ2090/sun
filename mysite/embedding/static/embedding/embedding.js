function confirmSubmit(obj) {
  let s = $("#id_message").val();
  let money = s.length / 1000 / 150.0
  if (confirm(`The text length is ${s.length}, which will roughly cost $${money.toFixed(2)}, continue?`)) {
    return true;
  }
  return false;
}