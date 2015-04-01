$('.exam .menu div[data-role=delete]').on('click', function(e) {
  var optionDelete = this;

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
