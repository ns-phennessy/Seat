$('tr[data-role=exam] div[data-role=delete]').on('click', function(e) {
  var optionDelete = this;

  data = { exam_id: $(this).data('id') };

  $.ajax({
    type: 'POST',
    url:  '/api/exam/',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
      xhr.setRequestHeader('X-METHODOVERRIDE', 'DELETE');
    },
    success: function() {
      location.reload()
    }
  });
});

$('.ui.accordion')
  .accordion()
;