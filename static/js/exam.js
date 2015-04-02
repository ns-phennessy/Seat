$('#addquestion').on('click', function(){
    $(this).hide();

    $('#newquestionform').appendTo($(this).parent());
    $('#newquestionform').slideDown(100)
});

$('div[data-role=question] div[data-role=delete]').on('click', function() {
    $.ajax({
        url: $(this).data('action');
        type: 'DELETE',
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
        },
        success: function() {
          location.reload();
        }
    });
});
