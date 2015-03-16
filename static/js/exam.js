$('#addquestion').on('click', function(){
  $(this).hide();

  $('#newquestionform').appendTo($(this).parent());
  $('#newquestionform').slideDown(100)

});
