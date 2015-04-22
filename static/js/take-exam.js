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
		})
		this.add = function(question) {
			questionsToBeSubmitted.push(question);
		}
	})();

	/* classes that indicate things */
	const basic_dom_selectors = {
		/* any questions */
		'question' : '.seatQuestion',
		/* types of questions */
		'multichoice' : '.multi',
		'truefalse' : '.truefalse',
		'essay' : '.essay',
		'shortanswer' : '.shortanswer',
		/* table of contents and outside elements */
		'toc' : '.seatToC'
	}

	/* things with data-x="" style annotations
	the values here are the "" */
	const basic_data_selectors = {
		/* common to all questions */
		'question_id' : 'question_id',
		'answer_text' : 'answer_text'
	}
	/* pseudoclasses that represent data */
	const dynamic_data_selectors = {
		'selected_choices' : ':checked'
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


	const Question = function(manifestation) {
		var question = this;
		question.manifestation = manifestation;
		question.data = {}; /* updated data */
		question.storage = {}; /* last saved data */
		
		question.submit = function() {

		}

		question.bookmark = function() {

		}

		question.clear = function() {

		}

		/* wireup */
		function wire_on_click(what) { 
			question.manifestation.find(what).on('click', function(event) {
				question[what]();
			});
		}
		for (var selector in master_action_map) {
			question.manifestation.find(selector).on('click', function() { question[selector] })
		}

	}

	const MultiQuestion = function() {
		var question = this;
		this.type = 'multichoice';
		this._data = {}
	}
	const ShortAnswer = function() {
		var question = this;
		this.type = 'shortanswer';
	}
	const Essay = function() {
		var question = this;
		this.type = 'essay';
	}
	const TrueFalse = function() {
		var question = this;
		this.type = 'truefalse';
	}
})