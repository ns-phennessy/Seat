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
      $(this).find('input[name=exam-name]').val('');
      $(this).find('input[name=course]').val('');
		},
		onApprove: function(){
			return false;
		}
	}
);

$('#newExamBtn').on('click', function() {
  $('#newExamModal.ui.modal').modal('show');
});
