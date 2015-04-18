(function ($) {
  /* closure - static variables go here */
  var data = {}

  /* begin plugin */
  $.fn.databind = function (options, default_values) {
    var container = this;

    assertOptionsAreValid(options)

    for (key in options.template) {

      container[key] = createGetterSetter(container, key, options);
      if (default_values !== undefined && typeof (options.template[key]) != typeof ({})) // set default value
        container[key](default_values[key]); // rn only support defaults for flats

      container[key].on = container.find(options.template[key]).on; // pass through event registering

    }

    container.extract = function () {
      var fresh_data = {};
      for (key in options.template) {
        var val = container[key]();
        if (typeof (val) !== typeof ('') && val !== null) {
          fresh_data[key] = [];
          val.each(function (i, v) { fresh_data[key].push($(v).val()) })
        } else if (val !== null) {
          fresh_data[key] = val;
        }
      }
      return fresh_data;
    }

    return container;
  }

  /* static "private" helper functions*/

  function createGetterSetter(container, this_key, options) {
    return function (index, value) {// getter/setter function
      if (arguments.length == 1) value = index;
      /* follow convention of getting if value doesn't exist */
      var selector = '';
      if (typeof (options.template[this_key]) === typeof ({})) selector = options.template[this_key]['array'];
      else selector = options.template[this_key];
      var element = $(container.find(selector));
      if (element === null || element.length === 0) { console.log('attempt to get ' + this_key + ' failed, could not find element'); return null; }
      if (arguments.length == 0) {
        if (element.length > 1)
          return element;
        else
          return element.val();
      }
      /* otherwise set the value */
      /* update markup */
      if (element.length == 1) {
        element.val(value);
        element.text(value);
      } else {
        if (arguments.length == 1) {
          element.each(function (i, v) { $(v).val(value); $(v).text(value); });
        } else {
          $(element[index]).val(value);
          $(element[index]).text(value);
        }
      }

      /* update storage if we have an id*/
      const id = container.find(options.key).val().trim()
      if (id !== "" && id !== null && id !== true && id !== false && id !== undefined) {
        if (data[id] === undefined) data[id] = {};
        data[id][this_key] = value;
      } else {
        console.log('id empty, not storing')
      }
      return element;
    }
  }

  function assertOptionsAreValid(options) {
    if (!(options.template && options.key)) {
      console.log('missing options in usage of data binder')
    }
  }
})(jQuery)