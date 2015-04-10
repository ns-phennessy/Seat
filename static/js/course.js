$('tr[data-role=exam] div[data-role=delete]').on('click', function(e) {
  var optionDelete = this;
  console.log('fuck these guys')
  $.ajax({
    url: $(this).data('action'),
    type: 'DELETE',
    beforeSend: function(xhr) {
      xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
    },
    success: function() {
      $(optionDelete).closest('tr').remove();
    }
  });
});
