$('#addquestion').on('click', function(){
    $(this).hide();
  
    $('#newquestionform').appendTo($(this).parent());
    $('#newquestionform').slideDown(100)
});

$('div[data-role=question] div[data-role=delete]').on('click', function() {
    var question = $(this).closest('div[data-role=question]');
    var questionId = question.data('id');

    $.ajax({
        url: '/dashboard/questions/' + questionId,
        type: 'DELETE',
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
        },
        success: function() {
          question.remove();
        }
    });
});
