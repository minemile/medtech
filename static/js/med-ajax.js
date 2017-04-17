$('#likes').click(function () {
  var docid;
  catid = $(this).attr("data-catid");
  $.get('/med/like_doc/', {doctor_id: catid}, function(data){
    $('#like_count').html(data);
    $('#likes').hide();
  });
});

$('#suggestion').keyup(function () {
  var query;
  query = $(this).val();
  $.get('/med/suggest_disease/', {suggestion: query}, function (data) {
    $('#dises').html(data);
  });
});
