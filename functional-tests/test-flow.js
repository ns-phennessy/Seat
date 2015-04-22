casper.test.begin("Teacher can login", 3, function suite(test) {
  casper.start('http://test.patcave.com/login/',function() {
  	test.assertExists('.ui', 'login page loaded');
  	this.fill('form',{
  		'username' : 'cseat',
  		'password' : 'takeaseat!'
  	}, false);
  })
  casper.then(function() {
  	this.click('button')
  })
  casper.then(function() {
	test.assert(this.getCurrentUrl() === 'http://test.patcave.com/dashboard/courses/')
	console.log('on dashboard')
  })
  casper.then(function() {
  	this.click('#addCourseBtn')
  	console.log('add course button clicked')
  })
  casper.then(function() {
  	this.fill('#addCourseModal form',{
  		'course_name': 'test-course-value'
  	}, false );
  	console.log('course name populated')
  	this.click('#addCourseModal .ui.blue.save.button')
  	console.log('submit course clicked')
  })
  casper.then(function() {
  	test.assertSelectorHasText('.menu.blue.vertical a.item:nth-last-child(2)', 'test-course-value')
  })
  casper.run(function() {
  	test.done()
  })

});