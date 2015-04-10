function submitRenameCourse() {
	var courseName = $('#addCourseModal .ui.form input[name="course_name"]').val();
	var middlewareToken = $('#addCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

	$('#addCourseModal .ui.form').addClass('loading');

	$.post('/api/course', {
		name : courseName,
		csrfmiddlewaretoken : middlewareToken
	}, function() {
		$('#renameCourseModal.ui.modal').modal('hide');
		location.reload();

	}).fail(function() {
		console.log(arguments);
	})
}

$('#renameCourseModal .ui.save.button').click(function(e) {
	submitRenameCourse();
});

$('#renameCourseModal.ui.modal').modal(
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

$('.ui.button[data-role="renameCourse"]').on('click', function(){
	$('#renameCourseModal.ui.modal').modal('show');
});

$('input[name=course_name]').keypress(function(e) {
	if (e.keyCode == 13) {
		e.preventDefault();
		submitAddCourse();
	}
});
