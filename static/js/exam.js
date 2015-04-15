$('#addquestion').on('click', function(){
    $(this).hide();

    $('#newquestionform').appendTo($(this).parent());
    $('#newquestionform').slideDown(100)
});

$('#question-type-selection').on('change', function () {
  $('#question-specifics-segment').show()
  $('#question-specifics-segment .form').hide()
  $('#question-specifics-segment .form[name=' + $(this).val() + ']').show()
  $('#question-save-bar').show()
})

$('div[data-role=question] div[data-role=delete]').on('click', function() {
    data = { question_id: $(this).data('id') }

    $.ajax({
        type: 'POST',
        url:  '/api/question',
        data: data,
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
          xhr.setRequestHeader('X-METHODOVERRIDE', 'DELETE');
        },
        success: function() {
          location.reload();
        }
    });
});
