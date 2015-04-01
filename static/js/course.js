$('.delete-exam').on('click', function(e) {
  e.preventDefault();

  var _this = this;

  $.ajax({
    url: $(this).attr('href'),
    type: 'DELETE',
    beforeSend: function(xhr) {
      xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
    },
    success: function() {
      $(_this).closest('tr').remove();
    }
  });
});
