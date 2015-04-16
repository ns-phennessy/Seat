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
  }).submit(function (e) {
    e.preventDefault()
    const token = $('#token-input input[name=token]').val();
    /*loading*/
    verify_token_and_redirect_to_exam(token)
  })

  function verify_token_and_redirect_to_exam(token) {
    $.post('/api/validate_token'
      ,{
        'token': token,
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
      }, function () {
        console.log(arguments)
      });
  }

})