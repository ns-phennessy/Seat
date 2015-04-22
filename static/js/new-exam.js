function submitNewExam() {
  var data = $('#newExamModal form').form('get values');

  $('#newExamModal .ui.form').addClass('loading');

  $.ajax({
    type: 'POST',
    url:  '/api/exam',
    data: data,
    success: newExamSuccess,
    error: function(res) {
      newExamFailure({
        message: 'An error occurred while creating the new exam. Please try again.'
      });
    }
  });
}

function newExamSuccess(res) {
  if (res.success) {
    location = res.edit_url
  } else {
    newExamFailure(res);
  }
}

function newExamFailure(res) {
  $('#newExamModal.ui.modal').modal('hide');

  noty({
    text: res.message,
    type: 'error',
    theme: 'relax'
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

$('.new-exam-btn').on('click', function() {
  $('#newExamModal.ui.modal').modal('show');
});
