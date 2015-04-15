$('#addquestion').on('click', function(){
    $(this).hide();

    $('#newquestionform').appendTo($(this).parent());
    $('#newquestionform').slideDown(100)
});

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
