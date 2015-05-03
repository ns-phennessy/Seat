$(document).ready(function() {
  $('#token-input').form({
    token: {
      identifier: 'token',
      rules: [
        {
          type: 'empty',
          prompt: 'Please enter a token'
        },
        {
          type: 'length[7]',
          prompt: 'All tokens are 7 characters'
        }
      ]
    }
  }, {
    'onSuccess': function () {
        $('#custom-errors').text('').hide()
        const token = $('#token-input input[name=token]').val();
        verify_token_and_redirect_to_exam(token)
    },
    'onFailure': function () {
      $('#custom-errors').text('').hide()
    }
  });
});

var duplicate_send_blocker = false;

function verify_token_and_redirect_to_exam(token) {
  if (duplicate_send_blocker === true) return;
  console.log('submitting')
  duplicate_send_blocker = true;

  $.ajax({
    url: '/api/validate_token',
    type: 'POST',
    data: { 'token': token,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
          },
    success: function(data, success) {
      duplicate_send_blocker = false;
      if (!success) {
        $('.ui.error.message.red').text('connection failure')
        return;
      }
      if (data.success === true) {
        console.log('valid token')
        location.href = '/student/take_exam'
      } else {
        $('#custom-errors').text(data.message).show()
      }

    }
  });
}

$('#take-exam').on('click', function() {
  token = $('#token-input input[name=token]').val();
  verify_token_and_redirect_to_exam(token);
});

$('form').on('submit', function(e) {
  e.preventDefault();
});
