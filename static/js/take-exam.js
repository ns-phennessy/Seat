$(document).ready(function () {
    const configuration = {
        'QUEUE_RETRY_PERIOD_IN_MS': 500
    };
    const api_endpoint_for_submissions = "/api/submissions";
    const exam_id = $('#exam_id').val();
    /* classes that indicate actions */
    const master_action_map = {
        '.questionClear': 'clear', /* question local       |  restores question to blank               */
        '.questionSubmit': 'submit', /* question local     |  submits question, adds to queue if fails */
        '.left.corner': 'bookmark', /* question local |  marks question as bookmarked             */
        '.questionSubmitAll': 'submitAll' /* global        |  */
    };

    /* define the queuing system */
    const queue = new (function () {
        var questionsToBeSubmitted = [];
        var interval = setInterval(function () {
            while (questionsToBeSubmitted.length != 0)
                questionsToBeSubmitted.shift().submit()
        }, configuration['QUEUE_RETRY_PERIOD_IN_MS'])
        this.add = function (question) {
            questionsToBeSubmitted.push(question);
        }
    })();

    /* classes that indicate things */
    const basic_dom_selectors = {
        /* any questions */
        'question': '.question',
        /* other things */
        'toc': '.table-of-contents',
        'question-list': '.question-list',
        /* question that has been bookmarked */
        'bookmark': '.bookmarked',
        /* toc link that correlates to a question with a bookmark */
        'bookmark-link': '.bookmark-link'
    }

    /* things with data-x="" style annotations
	the values here are the "" */
    const basic_data_selectors = {
        /* common to all questions */
        'question_id': 'question_id',
        'answer_text': 'answer_text'
    }
    /* classes that represent data */
    const dynamic_data_selectors = {
        'selected_choices': ':checked',
        'checkable': '.checkable'
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
    function basic_data_select(where, what) { return select(basic_data_selectors, where, "[data-x='" + what + "']") }

    function ajax_submit(data, success_cb, failure_cb, always_cb) {
        $.ajax({
            type: "POST",
            url: api_endpoint_for_submissions,
            data: {
                'submission': JSON.stringify(data)
            },
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            }
        })
		.done(success_cb)
		.fail(failure_cb)
		.always(always_cb)
    }

    const Question = function (manifestation) {
        var question = this;
        question.manifestation = manifestation;
        var bookmarked = false;
        const id = manifestation.find('.question-id').val();
        console.log('question id',id)
        question.data = {
            'question_id': id,
            'choices': []
        }; /* updated data */

        question.storage = {
            'question_id': id,
            'choices': []
        }; /* last saved data */


        function ajax_submit_success() {
            question.manifestation.find('.questionSaved').show()
            console.log('submit success', arguments);
            $('#question-link-' + id).removeClass('blue').addClass('green');
            question.storage = JSON.parse(JSON.stringify(question.data));
        }
        function ajax_submit_failure() {
            console.log('submit failure', arguments);
            queue.add(question)
        }
        function ajax_always() {
            console.log('ajax always', arguments)
        }

        question.submit = function () {
            question.manifestation.find('.questionSaved').hide()
            ajax_submit(question.data, ajax_submit_success, ajax_submit_failure, ajax_always)
        }

        /* TODO: pat we may change this,
		the point is that here you do whatever needs
		to be done to the list of bookmarks for 
		this particular question. the links
		in the ToC should be labeled with the
		question ID */
        question.bookmark = function () {
            if (!bookmarked) {
                question.manifestation.find('.left.corner').addClass('blue');
                $('#question-link-'+id).addClass('blue').addClass('bookmarked');
            } else {
                question.manifestation.find('.left.corner').removeClass('blue');
                $('#question-link-' + id).removeClass('blue').removeClass('bookmarked');
            }
            bookmarked = !bookmarked;
        }

        question.clear = function () {
            if (question.storage['question_id'] == '') {
                console.log('no storage available for clear!!!!')
                return;
            }
            var text_answer = basic_data_select(question.manifestation, 'answer_text');
            if (text_answer.length != 0) text_answer.val('');
            else {
                var checkables = dynamic_data_select(question.manifestation, 'checkable');
                checkables.each(function (i, v) {
                    $(v).prop('checked', false);
                })
            }
        }

        /* wireup */
        function wire_on_click(what) {
            question.manifestation.find(what).on('click', function (event) {
                question[master_action_map[what]]();
            });
        }

        /* actions */
        for (var selector in master_action_map) {
            wire_on_click(selector)
        }

        /* dynamic data */
        question.data['question_id'] = question.manifestation.find('[data-x="question_id"]').val();

        /* text types of questions */
        var text_answer = question.manifestation.find('.answer-text');
        /* wire up if exists */
        if (text_answer.length != 0) {
            text_answer.on('change', function () {
                question.data['choices'] = [text_answer.val()];
                question.submit()
            })
        } else {
            /* checkables, tf, multi */
            var checkables = dynamic_data_select(question.manifestation, 'checkable');
            checkables.on('change', function () {
                var choices = dynamic_data_select(question.manifestation, 'selected_choices');
                var new_choices = [];
                choices.each(function (i, v) {
                    new_choices.push($(v).val());
                })
                question.data['choices'] = new_choices;
                question.submit()
            })
        }

        question.storage = JSON.parse(JSON.stringify(question.data));
    }
    setInterval(function () {
        var percent = (($('.questionSaved:visible').length) / ($('.questionSaved:visible').length + $('.questionSaved:hidden').length))*100;
        $('[data-percent]').progress({percent: percent})
    }, 250)
    /* populate page */
    var question_array = [];
    var questions = dom_select($('body'), 'question');
    var toc = dom_select($('body'), 'toc')
    for (var i = 0; i < questions.length; ++i) {
        /* wireup is internalized */
        var new_question = new Question($(questions[i]));
        var question_id = new_question.data['question_id'];
        question_array.push(new_question);
        console.log('adding one')
        /* add to ToC */
    }
})