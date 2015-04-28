$('.delete-exam').on('click', function(e) {
	var optionDelete = this;

	data = { exam_id: $(this).data('id') };

	$.ajax({
		type: 'POST',
		url:  '/api/exam/',
		data: data,
		beforeSend: function(xhr) {
			xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
			xhr.setRequestHeader('X-METHODOVERRIDE', 'DELETE');
		},
		success: function() {
			location.reload()
		}
	});
});

// Token stuff
var token = new function(){

	this.create = function(exam_id){
		$.ajax({
			method: "POST",
			url: '/api/token/',
			data: {
				'exam_id' : exam_id
			},
			headers: {
				'X-CSRFToken' : $.cookie('csrftoken')
			}
		}).success(function(data, succcess) {

			$('#newTokenModal').find('.tokenText').text(data.token);
			$('#newTokenModal').modal({
				onHide: function(){
					location.reload();
				}
			});

			$('#newTokenModal').modal('show');
		})
		.fail(function() {console.log(arguments) })
		.always(function() {console.log(arguments) })

	};

	this.delete = function(){
		$.ajax({
			method: "POST",
			url: '/api/token/',
			data: {
				'token_id' : 15
			},
			headers: {
				'X-CSRFToken' : $.cookie('csrftoken'),
				'X-METHODOVERRIDE' : 'DELETE'
			}
		}).success(function(data, succcess) {console.log(data.token) })
		.fail(function() {console.log(arguments) })
		.always(function() {console.log(arguments) })
	};

	this.update = function(id, open, released, success){
		$.ajax({
			method: "POST",
			url: '/api/token/',
			data: {
				'token' : JSON.stringify({
					'token_id' : id,
					'open' : open,
					'released' : released
				})
			},
			headers: {
				'X-CSRFToken' : $.cookie('csrftoken'),
				'X-METHODOVERRIDE' : 'PUT'
			}
		})
		.success(success)
	};

}


$('[data-role="new-token"]').on('click', function(){
	var exam_id = $(this).attr('data-id');	
	token.create(exam_id);
});


$('[data-content]').popup({
	variation:'inverted',
	delay:{
		show:500	
	},
	position:'left center'	
});

$('.token .ui.dropdown').dropdown({
	onChange: function(value, text, $choice){
		var tokenContainer = $(this);
		var token_id = $(this).attr('data-tokenid');
        var gradeLink = $(this).find('[data-role="viewTokenGrades"]');
        
		switch(value){
			case 'openToken':
				var success = function(){
					var statusLabel = $(tokenContainer).find('.ui.circular.label');

					statusLabel.removeClass('red');
					statusLabel.removeClass('purple');
					statusLabel.addClass('green');
                    
                    gradeLink.addClass('disabled');
				}


				token.update(token_id, true, false, success);
				break;
			case 'closeToken':
				var success = function(){
					var statusLabel = $(tokenContainer).find('.ui.circular.label');

					statusLabel.removeClass('green');
					statusLabel.removeClass('purple');
					statusLabel.addClass('red');
                    
                    gradeLink.removeClass('disabled');

				}


				token.update(token_id, false, false, success);
				break;
			case 'releaseToken':
				var success = function(){
					var statusLabel = $(tokenContainer).find('.ui.circular.label');

					statusLabel.removeClass('green');
					statusLabel.removeClass('red');
					statusLabel.addClass('purple');
                    
                    gradeLink.removeClass('disabled');

				}


				token.update(token_id, false, true, success);
				break;
		}
	}
});
