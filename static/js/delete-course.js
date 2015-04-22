function submitDeleteCourse() {
  var middlewareToken = $('#addCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

  $('#main').addClass('loading');

  $.ajax({
    type: "POST",
    url: '/api/course/',
    data: { course_id: $('#course-id').val() },
    beforeSend: function(xhr) {
        xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken') );
        xhr.setRequestHeader('X-METHODOVERRIDE', 'DELETE');
    },
    success: deleteCourseSuccess,
    error: function() {
      showErrorMessage('An error occurred while deleting the course. Please try again.');
    }
  });
}

function deleteCourseSuccess(res) {
  if (res.success) {
    location.reload();
  } else {
    showErrorMessage(res.message);
  }
}

$('#delete-course').click(function(e) {
  submitDeleteCourse();
})
