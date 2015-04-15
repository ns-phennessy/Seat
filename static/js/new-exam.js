function submitNewExam() {
  var data = $('#newExamModal form').form('get values');

  $('#newExamModal .ui.form').addClass('loading');

  $.ajax({
    type: 'POST',
    url:  '/api/exam',
    data: data,
    success: function(res) {
      location.reload()
    }
  });
}

$('#newExamModal .ui.save.button').click(function(e) {
  submitNewExam();
});

$('#newExamModal .ui.form').on('submit', function(e){
	e.preventDefault();
	submitNewExam();
});

$('#newExamModal.ui.modal').modal(
	{
		transition:'fly down',
		duration:500,
		closable:false,
		selector:{
			approve:'.actions .save'
		},
		onShow:function(){
			$(this).find('.ui.form').removeClass('loading');
      $(this).find('input[name=name]').val('');
		},
		onApprove: function(){
			return false;
		}
	}
);

$('#newExamBtn').on('click', function() {
  $('#newExamModal.ui.modal').modal('show');
});
