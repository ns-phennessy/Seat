$('tr[data-role=exam] div[data-role=delete]').on('click', function(e) {
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

	this.update = function(){
		$.ajax({
			method: "POST",
			url: '/api/token/',
			data: {
				'token' : JSON.stringify({
					'token_id' : 1,
					'open' : true,
					'released' : false
				})
			},
			headers: {
				'X-CSRFToken' : $.cookie('csrftoken'),
				'X-METHODOVERRIDE' : 'PUT'
			}
		},function() {
			console.log(arguments)
		})
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

$('.tokens .ui.dropdown').dropdown({

});