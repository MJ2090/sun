function confirmSubmit(obj) {
  let s = $("#id_message").val();
  let money = s.length
  if (confirm(`The training text length is ${s.length}`)) {
    return true;
  }
  return false;
}