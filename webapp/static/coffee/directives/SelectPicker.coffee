angular.module('stories').directive 'selectpicker', ['$timeout', ($timeout) ->
  
  # This is stolen from Angular...
  NG_OPTIONS_REGEXP = /^\s*(.*?)(?:\s+as\s+(.*?))?(?:\s+group\s+by\s+(.*))?\s+for\s+(?:([\$\w][\$\w\d]*)|(?:\(\s*([\$\w][\$\w\d]*)\s*,\s*([\$\w][\$\w\d]*)\s*\)))\s+in\s+(.*)$/

  snakeCase = (input) -> input.replace /[A-Z]/g, ($1) -> "_#{$1.toLowerCase()}"
  isEmpty = (value) ->
    if angular.isArray(value)
      return value.length is 0
    else if angular.isObject(value)
      return false for key in value when value.hasOwnProperty(key)
    true

  selectpicker =
    restrict: 'A'
    link: (scope, element, attr) ->
      # Take a hash of options from the selectpicker directive
      options = scope.$eval(attr.selectpicker) or {}

      startLoading = -> element.addClass('loading disabled').attr('disabled', true)
      stopLoading  = -> element.removeClass('loading disabled').attr('disabled', false)

      # Init selectpicker on the next loop so ng-options can populate the select
      $timeout -> element.selectpicker options

      # Watch the collection in ngOptions and update selectpicker when it changes.  This works with promises!
      if attr.ngOptions
        match = attr.ngOptions.match(NG_OPTIONS_REGEXP)
        valuesExpr = match[7]
        # There's no way to tell if the collection is a promise since $parse hides this from us, so just
        # assume it is a promise if undefined, and show the loader
        startLoading() if angular.isUndefined(scope.$eval(valuesExpr))
        scope.$watch(valuesExpr, (newVal, oldVal) -> 
          stopLoading()
          element.selectpicker "refresh"
        , true)

      if attr.ngModel
        scope.$watch("#{attr.ngModel}", (newVal, oldVal)->
          element.selectpicker "refresh",
          true
        )


]
