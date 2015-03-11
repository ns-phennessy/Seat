$('[data-content]').popup({
   position:'top center',
   transition:'drop'
});

$('.ui.menu .item').tab();

$('.ui.dropdown').dropdown({});

$('.ui.checkbox').checkbox();

$('.ui.button');

$('#addCourseBtn').on('click', function(){
	$('#addCourseModal.ui.modal').modal('show');
});
