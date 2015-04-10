function submitRenameCourse() {
	var courseName = $('#renameCourseModal .ui.form input[name="course_name"]').val();
	var middlewareToken = $('#renameCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

	$('#renameCourseModal .ui.form').addClass('loading');

	$.ajax({
       type: "POST",
       url: '/api/course/',
       data: { course_id: $('#course-id').val(), name: courseName },
       beforeSend: function(xhr) {
           xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken') );
           xhr.setRequestHeader('X-METHODOVERRIDE', 'PUT');
       },
       success: function() {
           console.log('success');
           location.reload();
       },
       fail : function() {
       		console.log('failure');
       }
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

