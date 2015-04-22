$('[data-content]').popup({
	position:'top center',
	transition:'drop'
});
$('.ui.menu .item').tab();
$('.ui.dropdown:not([data-role="questionType"])').dropdown({});
$('.ui.checkbox').checkbox();

$(document).ready(function(e) {
  var refresh = $('#refresh');
  if ( refresh.val() === 'yes' ) {
    location.reload(true);
  } else {
    refresh.val('yes');
  }
});
