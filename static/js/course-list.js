document.addEventListener("DOMContentLoaded", function(event) {
  $('#addCourseModal .ui.save.button').click(function(e) {

    var courseName = $('#addCourseModal .ui.form input[name="course_name"]').val();
    var middlewareToken = $('#addCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

    $('#addCourseModal .ui.form').addClass('loading');

    $.post('/dashboard/courses/new', {
      name : courseName,
      csrfmiddlewaretoken : middlewareToken
    }, function() {
      $('#addCourseModal.ui.modal').modal('hide');
        location.reload();

    }).fail(function() {
      console.log(arguments);
    })
  })
});
