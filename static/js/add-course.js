function submitAddCourse() {
  var courseName = $('#addCourseModal .ui.form input[name="course_name"]').val();
  var middlewareToken = $('#addCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

  $('#addCourseModal .ui.form').addClass('loading');

  $.ajax({
    type: 'POST',
    url:  '/api/course',
    data: {
      name: courseName,
      csrfmiddlewaretoken: middlewareToken
    },
    success: newCourseSuccess,
    error: function(res) {
      $('#addCourseModal.ui.modal').modal('hide');
      showErrorMessage('An error occurred while creating the new course. Please try again.');
    }
  })
}

function newCourseSuccess(res) {
  $('#addCourseModal.ui.modal').modal('hide');

  if (res.success) {
    location.reload();
  } else {
    showErrorMessage(res.message);
  }
}

$('#addCourseModal .ui.save.button').click(function(e) {
  submitAddCourse();
});

$('#addCourseModal .ui.form').on('submit', function(e){
	e.preventDefault();
	submitAddCourse();
});

$('#addCourseModal.ui.modal').modal(
	{
		transition:'fly down',
		duration:500,
		closable:false,
		selector:{
			approve:'.actions .save'
		},
		onShow:function(){
			$(this).find('.ui.form').removeClass('loading');
      $(this).find('input[name=course_name]').val('');
		},
		onApprove: function(){
			return false;
		}
	}
);

$('#addCourseBtn').on('click', function(){
	$('#addCourseModal.ui.modal').modal('show');
});
