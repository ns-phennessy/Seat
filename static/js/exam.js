$('div[data-role=question] div[data-role=delete]').on('click', function() {
    data = { question_id: $(this).data('id') }

    $.ajax({
        type: 'POST',
        url:  $(this).data('action'),
        data: data,
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
          xhr.setRequestHeader('X-METHODOVERRIDE', 'DELETE');
        },
        success: function() {
          location.reload();
        }
    });
});

$('.ui.menu .item').tab();
$('.ui.checkbox').checkbox();

var questionDataTemplate = {
	question_id:'',
	prompt:'',
	type:'',
	options:{},
	clone:function(){
		return $.extend(true, {}, this)
	}
};

(function ($) {
	$.fn.questionForm = function(options){
		//Globals
		var form = this;
		var items = $('[data-tab="tab_edit"]').find('.items');

		//Settings
		var settings = $.extend({
			newQuestionButton: 		".ui.button[data-role='newQuestion']",
			editQuestionButton: 	".ui.button[data-role='edit']",
			deleteQuestionButton: 	".ui.button[data-role='delete']",
			saveButton:				".ui.button[data-role='save']",
			closeButton:			"[data-role='close']",
			questionTypeSelector:	"select[data-role='questionType']",
			deleteOptionSelector:	".ui.button[data-role='deleteOption']"
		}, options );

		form.init = function(){
			$('[data-content]').popup({
				position:'top center',
				transition:'drop'
			});

			$('#newquestionform .dimmer').dimmer({
				duration:{
					show:500, 
					hide:0
				}
			});

			$(settings.editQuestionButton).on('click', function(){
				var questionSummary = this.closest('.item');
				var dataHolder = $(questionSummary).find('input[type="hidden"]');

				var questionData = JSON.parse(dataHolder.val());	

				form.clear();

				form.setValue('prompt', questionData.prompt);
				form.setValue('questionType', questionData.type);

				//Load question option data!
				switch(questionData.type){
					case 'multichoice':

						var inputs = $('.multichoice.options input[type="text"]');
						
						$(inputs[0]).val(questionData.options.answer);

						$.each(questionData.options.choices, function(index, value){

							if(index == 0){
								$(inputs[1]).val(value);		
							}
							else{
						
								var place = $('.ui.button[data-role="add-multichoice-choice"]');
								var template = $('.multichoiceTemplate').clone();

								template.removeClass('multichoiceTemplate');

								template.insertBefore(place);
								template.find('input[type="text"]').val(value);
								$('.ui.checkbox').checkbox();

								template.show();

								$(settings.deleteOptionSelector).on('click', function(){				
									$(place).closest('div.three.fields').remove();
								});


							}
						});


						break;
					case 'truefalse':
						if( questionData.options.answer == true)
							$('.truefalse.options .ui.checkbox').checkbox('check');
						else
							$('.truefalse.options .ui.checkbox').checkbox('uncheck');
						break;
				}

				form.move(questionSummary);
				$(questionSummary).children('.content').hide();
			});

			$(settings.deleteQuestionButton).on('click', function(){
				var questionSummary = this.closest('.item');
				//TODO remove this when doing ajax
				$(this).popup('hide');

				$(questionSummary).remove();

				var ajaxData;
				var token;

				//TODO Hookup to deletion endpoint
				$.ajax({
					url: '/api/question',
					type: 'POST',
					data: ajaxData,
					beforeSend: function(xhr) {
						xhr.setRequestHeader('X-CSRFToken', token);
					},
					success: function() {
						$(questionSummary).remove();
					}
				});
			});
		};
		form.init();


		//Aux functions
		form.clear = function(){
			form.removeClass('loading');
			form.find('.dimmer').dimmer('hide');

			var multichoiceForm = form.find('form[name=multichoice]');

			multichoiceForm.find('.three.fields').each(function(index, value){
				if(index < 2){
					$(this).find('input').val('');
				}
				else{
					$(this).remove();
				}
			});

			var truefalse = form.find('.truefalse.options .ui.checkbox').checkbox('uncheck');

		};

		form.setValue = function(item, value){
			switch(item){
				case 'header':
					form.find('h3.header').text(value);	
					break;

				case 'prompt':
					form.find('input[name="prompt"]').val(value);
					break;

				case 'questionType':
					form.find('div.ui.dropdown.selection').dropdown('set selected', value);
					break;
			}
		};

		form.setLoading = function(){
			form.addClass('loading');
		};

		form.move = function(location){
			form.close();
			form.appendTo(location);
			form.show();
		};

		form.close = function(){
			form.hide();
			$(settings.newQuestionButton).show();
			items.find('.item .content').show();
		};

		form.multiChoiceData = function() {

			question = form.form('get values');
			question.options = {}

			var multiform = form.find('form[name=multichoice]');
			var choices = multiform.find('input[name=choice]');

			choices = choices.map(function() {
				return $(this).val();
			}).get();

			var selectedRadio = multiform.find('input:radio[checked=checked]');
			var selectedInput = selectedRadio.closest('.fields').find('input:text');

			var answer = selectedInput.val();
			var answerIndex = choices.indexOf(answer);

			choices.splice(answerIndex, 1);

			question.options.choices = choices;
			question.options.answer = answer;

			return question;
		};

		//Event listeners
		$(settings.newQuestionButton).on('click', function(){
			form.clear();

			form.setValue('header', 'New Question');
			form.setValue('prompt', '');
			form.move( $('.ui.segment[data-tab="tab_edit"]') );
			$(this).hide();
		});

		$('.truefalse.options [data-role="setTrue"]').on('click', function(){
			$('.truefalse.options .ui.checkbox').checkbox('check');
		});

		$('.truefalse.options [data-role="setFalse"]').on('click', function(){
			$('.truefalse.options .ui.checkbox').checkbox('uncheck');
		});

		form.find(settings.closeButton).on('click', function(){
			form.close();
		});

		$("select[data-role='questionType']").dropdown({
			onChange: function(value, text, $choice){	

				form.find('.options').each(function(){
					$(this).addClass('hidden')
				});

				switch(value){
					case 'multichoice':
						form.find('.multichoice.options').removeClass('hidden');
						break;	
					case 'truefalse':
						form.find('.truefalse.options').removeClass('hidden');
						break;	
					case 'shortanswer':
						form.find('.shortanswer.options').removeClass('hidden');
						break;	
					case 'essay':
						form.find('.essay.options').removeClass('hidden');
						break;	 
				}
			}
		});

		form.find(settings.saveButton).on('click', function () {
			form.setLoading();
			var questionSummary = this.closest('.item');

			//Get form data
			var questionData = questionDataTemplate.clone();
			var formData = form.form('get values');

			questionData.prompt = formData.prompt;
			questionData.type = formData.type;

			//Check if question is new or exists
			if(questionSummary == null){
				questionSummary = $(".item.questionSummary").clone();

				questionSummary.removeClass('questionSummary');
				questionSummary.appendTo(items);
			}

			//Get elements to load data into
			var prompt = $(questionSummary).find('span.prompt');
			var type = $(questionSummary).find('span.type');
			var options = $(questionSummary).find('span.options');
			var dataHolder = $(questionSummary).find('input[type="hidden"]');

			//Set values
			prompt.text(questionData.prompt);

			switch(questionData.type){
				case 'multichoice':
					type.text("Multiple Choice");
					options.text('5 Options');
					questionData.options = form.multiChoiceData().options;
					options.text( (Object.keys(questionData.options.choices).length + 1) + " Options");

					break;	
				case 'truefalse':
					type.text("True / False");
					options.text('True');

					var answerOption = $('.truefalse.options .ui.checkbox').checkbox('is checked');

					questionData.options = {
						answer: answerOption
					};

					options.text(answerOption);

					break;	
				case 'shortanswer':
					type.text('Short Answer');
					break;	
				case 'essay':
					type.text('Essay');
					break;	
			}

			const token = form.find('input[name=csrfmiddlewaretoken]').val();
			const exam_id = $('input[name=exam_id]').val();

			$.ajax({
				url: '/api/question',
				type: 'POST',
				data: {
				  'question': JSON.stringify({
				    'type': questionData.type,
				    'prompt': questionData.prompt,
				    'choices': questionData.choices | [],
            'options' : questionData.options
				  }),
          'exam_id' : exam_id
				},
				beforeSend: function(xhr) {
					xhr.setRequestHeader('X-CSRFToken', token);
				},
				success: function (success, data) {

				  if (success !== true) {
            /* TODO: UI display failure */
				  }

				  if (data.success !== true) {
            /* TODO: UI display failure */
				  }

					$('#newquestionform .dimmer').dimmer('show');
					form.close();
					$(questionSummary).show();

				  // update id
          questionData.question_id = data.id

          // save state
					dataHolder.val(JSON.stringify(questionData));
				},
				fail: function () {
          /* TODO: UI display failure */
				}
			});

		  //Update event listeners?
			form.init();
		});

		$('.ui.button[data-role="add-multichoice-choice"]').on('click', function(){
			var template = $('.multichoiceTemplate').clone();

			template.removeClass('multichoiceTemplate');

			template.insertBefore(this);
			$('.ui.checkbox').checkbox();

			template.show();

			$(settings.deleteOptionSelector).on('click', function(){				
				$(this).closest('div.three.fields').remove();
			});
		});

	};
}(jQuery));

$('#newquestionform').questionForm();

