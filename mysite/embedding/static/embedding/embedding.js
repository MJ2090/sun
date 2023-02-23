function confirmSubmit(obj) {
  var s = $("#id_message").val();
  var money = s.length
  if (confirm(`The training text length is ${s.length}')) {
    return true;
  }
  return false;
}