$(document).ready(function () {
  console.log('hello')
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
        /*TODO: loading*/
        verify_token_and_redirect_to_exam(token)
    },
    'onFailure': function () {
      $('#custom-errors').text('').hide()
    }
  })
  var duplicate_send_blocker = false;
  function verify_token_and_redirect_to_exam(token) {
    if (duplicate_send_blocker === true) return;
    console.log('submitting')
    duplicate_send_blocker = true;
    $.post('/api/validate_token'
      ,{
        'token': token,
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
      }, function (data, success) {
        duplicate_send_blocker = false;
        if (!success) {
          /* TODO: handle no internet */
          $('.ui.error.message.red').text('connection failure')
          return;
        }
        if (data.success === true) {
          console.log('valid token')
          location.href = '/student/take_exam.html'
        } else {
          $('#custom-errors').text(data.message).show()
        }
      });
  }

})