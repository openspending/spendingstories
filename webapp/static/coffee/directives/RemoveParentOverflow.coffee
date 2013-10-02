(angular.module 'stories').directive 'removeparentoverflow', [() ->

    removeparentoverflow =
        restrict : 'A'
        link: (scope, element, attr) ->
            parentSelector = attr.removeparentoverflow
            parent = if parentSelector? then element.parents(parentSelector) else do element.parent

            element.on 'focus', () => parent.css 'overflow', 'visible'
            element.on 'blur', () => parent.css 'overflow', 'hidden'

]