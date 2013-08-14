angular.module('stories')
    .directive "stickToTop", ->     
        link: (scope, element, attrs)->    
            # Record element's initial top
            elementTop = 1*element.css("top").replace("px", "")
            element.data("initial-top", elementTop) 
            # Record last scroll position for later
            lastScrollTop = $(window).scrollTop()
            # Watch window scroll
            $(window).on "scroll", ->
                # Get the current window scroll top position to calculate the delta
                currentScrollTop = $(window).scrollTop()
                # Delta reprensentes the distance since the last scroll
                delta = currentScrollTop -  lastScrollTop
                # Records the current scroll as last top for next events
                lastScrollTop = currentScrollTop

                elementHeight     = element.outerHeight()
                elementTop        = 1*element.css("top").replace("px", "")
                elementInitialTop = element.data("initial-top") or 0                
                # We go down
                if delta > 0
                    # Moves the element to the top bu not top high !
                    offset = 
                        if currentScrollTop < elementHeight + elementInitialTop
                            -currentScrollTop + elementInitialTop
                        else
                            Math.max -elementHeight, elementTop - delta
                # We go up
                else
                    # Moves the element to the bottom but not under its initial top
                    offset = Math.min elementInitialTop, elementTop - delta

                element.css "top", offset

