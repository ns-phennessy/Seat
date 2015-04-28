$('#grade-link').on('click', function () {
  var token_id = $('#grade-link').data('token');

  $.ajax({
      type: 'POST',
      url: '/api/grade',
      data: { 'token_id': token_id },
      headers: {
          'X-CSRFToken': $.cookie('csrftoken')
      }
  })
});
