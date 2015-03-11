$('[data-content]').popup({
	position:'top center',
	transition:'drop'
});

$('.ui.menu .item').tab();

$('.ui.dropdown').dropdown({});

$('.ui.checkbox').checkbox();


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
			$(this).find('input').val('');
		},
		onApprove: function(){
			return false;
		}
	}
);

$('#addCourseBtn').on('click', function(){
	$('#addCourseModal.ui.modal').modal('show');
});

