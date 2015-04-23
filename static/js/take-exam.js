$(document).ready(function() {
	const configuration = {
		'QUEUE_RETRY_PERIOD_IN_MS': 500
	};
	/* classes that indicate actions */
	const master_action_map = {
		'.questionClear' : 'clear', /* question local       |  restores question to blank               */
		'.questionSubmit' : 'submit', /* question local     |  submits question, adds to queue if fails */ 
		'.questionBookmark' : 'bookmark', /* question local |  marks question as bookmarked             */
		'.questionSubmitAll' : 'submitAll' /* global        |  */
	};
	
	/* define the queuing system */
	const queue = new (function() {
		var questionsToBeSubmitted = [];
		var interval = setInterval(function() {
			while (questionsToBeSubmitted.length != 0)
				questionsToBeSubmitted.shift().submit()
		}, configuration['QUEUE_RETRY_PERIOD_IN_MS'])
		this.add = function(question) {
			questionsToBeSubmitted.push(question);
		}
	})();

	/* classes that indicate things */
	const basic_dom_selectors = {
		/* any questions */
		'question' : '.seatQuestion',
		/* other things */
		'toc' : '.seatToC',
		'question-list' : '.question-list',
		/* question that has been bookmarked */
		'bookmark' : '.bookmarked',
		/* toc link that correlates to a question with a bookmark */
		'bookmark-link' : '.bookmark-link'
	}

	/* things with data-x="" style annotations
	the values here are the "" */
	const basic_data_selectors = {
		/* common to all questions */
		'question_id' : 'question_id',
		'submission_id' : 'submission_id',
		'answer_text' : 'answer_text'
	}
	/* classes that represent data */
	const dynamic_data_selectors = {
		'selected_choices' : ':checked',
		'choices' : '.checkable'
	}

	function select(from, where, what) {
		if (!where)
			console.log('where did not exist', where, 'in dom_select');
		if (!basic_dom_selectors[what])
			console.log('basic dom selectors did not contain', what);
		return where.find(from[what]);
	}

	/* dom selects things like -> .essay */
	function dom_select(where, what) { return select(basic_dom_selectors, where, what); }
	/* dynamic selects things like -> :checked */
	function dynamic_data_select(where, what) { return select(dynamic_data_selectors, where, what); }
	/* basic selects things like -> data-x="" */
	function basic_data_select(where, what) { return select(basic_data_selectors, where, "[data='"+what+"']")}

	function ajax_submit(data, success_cb, failure_cb, always_cb) {

	}

	const Question = function(manifestation) {
		var question = this;
		question.manifestation = manifestation;
		var bookmarked = false;
		question.data = {
			'question_id' : '',
			'submission_id' : '',
			'choices' : []
		}; /* updated data */

		question.storage = {
			'question_id' : '',
			'submission_id' : '',
			'choices' : []
		}; /* last saved data */
		

		function ajax_submit_success() {
			console.log('submit success', arguments);
			// TODO: set submission id question.data['submission_id']
			question.storage = JSON.parse(JSON.stringify(question.data));
		}
		function ajax_submit_failure() {
			console.log('submit failure', arguments);
		}
		function ajax_always() {
			console.log('ajax always', arguments)
		}

		question.submit = function() {
			ajax_submit(question.data, ajax_submit_success, ajax_submit_failure, ajax_always)
		}

		/* TODO: pat we may change this,
		the point is that here you do whatever needs
		to be done to the list of bookmarks for 
		this particular question. the links
		in the ToC should be labeled with the
		question ID */
		question.bookmark = function() {
			if (!bookmarked) {
				question.manifestation.addClass('bookmarked');
				$('#question-link-'+question.data['question_id']).addClass('bookmark-link');
			} else {
				question.manifestation.removeClass('bookmarked');
				$('#question-link-'+question.data['question_id']).removeClass('bookmark-link');
			}
			bookmarked = !bookmarked;
		}

		question.clear = function() {
			if (question.storage['question_id'] == '') {
				console.log('no storage available for clear!!!!')
				return;
			}
			var text_answer = basic_data_select(question.manifestation, 'answer_text');
			if (text_answer.length != 0) text_answer.val('');
			else {
				var checkables = dynamic_data_select(question.manifestation, 'checkable');
				checkables.each(function(i,v) {
					$(v).prop('checked', false);
				})
			}
		}

		/* wireup */
		function wire_on_click(what) { 
			question.manifestation.find(what).on('click', function(event) {
				question[what]();
			});
		}

		/* actions */
		for (var selector in master_action_map) {
			question.manifestation.find(selector).on('click', function() { question[selector] });
		}

		/* dynamic data */
		question.data['question_id'] = basic_data_select(question.manifestation, 'question_id');

		/* text types of questions */
		var text_answer = basic_data_select(question.manifestation, 'answer_text');
		/* wire up if exists */
		if (text_answer.length != 0) {
			text_answer.on('change', function() {
				question.data['answers'] = [ text_answer.val() ];
			})
		} else {
			/* checkables, tf, multi */
			var checkables = dynamic_data_select(question.manifestation, 'checkable');
			checkables.on('change', function() {
				var choices = dynamic_data_select(question.manifestation, 'selected_choices');
				var new_choices = [];
				choices.each(function(i,v) {
					new_choices.push($(v).val());
				})
				question.data['choices'] = new_choices;
			})
		}

		question.storage = JSON.parse(JSON.stringify(question.data));
	}

	/* populate page */

})