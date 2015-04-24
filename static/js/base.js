$('[data-content]').popup({
	position:'top center',
	transition:'drop'
});

$('.ui.checkbox').checkbox();
$('.ui.menu .item').tab();
$('.ui.dropdown:not([data-role="questionType"])').dropdown({});

$(document).ready(function(e) {
  var refresh = $('#refresh');
  if ( refresh.val() === 'yes' ) {
    location.reload(true);
  } else {
    refresh.val('yes');
  }
});

function showErrorMessage(message) {
  noty({
    text:  message,
    type:  'error',
    theme: 'relax',
    killer: true
  });
}
