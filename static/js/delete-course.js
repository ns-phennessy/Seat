function submitDeleteCourse() {
    var middlewareToken = $('#addCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

    $('#main').addClass('loading');

    $.ajax({
       type: "POST",
       url: '/api/course/',
       data: { course_id: $('#course-id').val() },
       beforeSend: function(xhr) {
           xhr.setRequestHeader('X-CSRFToken', middlewareToken );
           xhr.setRequestHeader('X-METHODOVERRIDE', 'DELETE');
       },
       success: function() {
           console.log('success');
           location.reload();
       },
       fail : function() {
       		console.log('failure');
       }
   })
}

$('#delete-course').click(function(e) {
  submitDeleteCourse();
})
