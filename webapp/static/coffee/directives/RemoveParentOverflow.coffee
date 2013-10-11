(angular.module 'stories').directive 'removeparentoverflow', [() ->

    removeparentoverflow =
        restrict : 'A'
        link: (scope, element, attr) ->
            parentSelector = attr.removeparentoverflow
            parent = if parentSelector? then element.parents(parentSelector) else do element.parent
            timer = undefined

            element.on 'focus', () =>
                if timer?
                    clearTimeout timer
                    timer = undefined
                parent.css 'overflow', 'visible'
            element.on 'blur', () =>
                timer = setTimeout () =>
                    timer = undefined
                    parent.css 'overflow', 'hidden'
                , 100

]