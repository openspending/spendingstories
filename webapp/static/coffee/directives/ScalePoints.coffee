angular.module('stories')
    .directive "scalePoints", ['Currency', (Currency)->
        # Returned object to that defines the directive
        restrict: "EAC"
        templateUrl: "/partial/scale-points.html"
        replace: true
        scope:
            data           : "="
            current        : "=story"
            click          : "=click"
            rulerValue     : "=ruler"
            rulerCurrency  : "=currency"
            filter         : "&"
            pointGap       : "&"
            pointGapBig    : "&"
            pointWidth     : "&"
            pointHeight    : "&"
            pointWidthBig  : "&"
            pointHeightBig : "&"
            overview       : "&"
        
        link: (scope, element, attrs)->
            # Where we insert the point
            workspace      = d3.select(element[0])
            # Width of the workspace according to its parent
            workspaceWidth = if scope.overview() then element.innerWidth() else 6000
            
            # Get optional visualization opt
            pointWidth  = if scope.overview() then scope.pointWidth()  or 25 else scope.pointWidthBig()  or 200
            pointHeight = if scope.overview() then scope.pointHeight() or 25 else scope.pointHeightBig() or 60
            pointGap    = if scope.overview() then scope.pointGap()    or 7  else scope.pointGapBig()    or 7
            # Scope values to monitor            
            monitored = ["rulerValue", "rulerCurrency"] #, "data"]
            # Watch those values
            scope.$watch monitored.join("||"), ->update()

            addPoint = (point)->
                lines = scope.lines
                lines = scope.lines = scope.lines || []
                lines[point.line] = {} unless lines[point.line]
                lines[point.line][point.id] = point


            # Isolate the scale initialization to allow dynamique updating
            update = (optimized = false)->
                if !optimized
                    scope.lines = []

                # Data must be loaded
                return unless scope.data? and scope.data.length                                 

                # Ruler that "split" the screen
                rulerValue     = 1*scope.rulerValue or -1

                # Static positioning must be change to relative
                if element.css("position") is "static"
                    # Using relative position allow us to position points
                    # accoding the top left corner of the workspace
                    element.css("position", "relative")

                rulerRate = Currency.list[scope.rulerCurrency].rate
                # if rulerRate is defined we set it to the scope otherwise we set it like USD
                scope.rulerRate = if rulerRate? then rulerRate else 1

                dataset = scope.data
                # Filter dataset if we received a filter
                filter  = scope.filter()
                # Filter is a function
                dataset = _.filter(dataset, filter) if typeof filter is "function"                   
                # Filter is an object
                dataset = _.where(dataset, filter) if typeof filter is "object"            
                # Not more data after filtering ?
                return unless dataset.length
                # Order dataset to avoid caothic stacking
                dataset = _.sortBy dataset, "current_value_usd"
                dataset = _.map dataset, (story)->
                    story.converted_current_value = story.current_value_usd / scope.rulerRate
                    return story

                # Put the processed data into a dedicated field
                scope.dataset = dataset
                console.log dataset[0].converted_current_value
                # Bounds values (using sorted list)            
                min = Math.min dataset[0].converted_current_value, rulerValue 
                max = Math.max dataset[dataset.length-1].converted_current_value, rulerValue
                console.log min, max       
                # And extend the scale with the bounds                    
                scale = d3.scale.log()
                          .domain([ min, max ])
                          .rangeRound([pointWidth, workspaceWidth - pointWidth])
                          .nice()

                ticks = scale.ticks()
                ticks = _.filter(ticks, (t, i)-> (i % Math.floor(ticks.length/4) == 0))

                axisLabels = _.map ticks, (t)-> 
                    text: t
                    value: t

                scope.ticks = ticks
                scope.axisLabels = axisLabels
                xAxisHeight = 80

                # these variables help us to know if we have to go to the next line
                lastY = lastX = -(pointWidth+pointGap)

                # Create position functions
                x = (d)-> scale(d.converted_current_value)
                y = (d)-> d.line * (pointHeight +  pointGap)
            
                # Percentage value (to allow resizing)
                xpr = (d)-> x(d)/workspaceWidth*100 + "%"

                scope.harmonizePoints = ()->
                    lines = scope.lines
                    """
                    Reposition all points to avoid overlapping
                    """
                    # this algorithm work on a sorted list (from lower to higher)
                    lines[0] = _.sortBy lines[0], (e)-> e.x
                    harmonize = (line)->
                        """
                        Will loop over a line and remove all overlapping elements
                        @param line - the line to clean up (Object { <id>: element} )
                        @returns the overlapping elements removed from `line` 

                        To do that it work this way:
                          - we set an element of reference (the lowest)

                          - we search the nearest not overlapping element to be the 
                            new reference element

                          - all other elements are deleted from the passed line and
                            return as result 
                        """
                        last_good_point = null # the reference point 
                        bad_points = {}
                        for i,n of line
                            do()->
                                if !last_good_point or Math.abs(n.x - last_good_point.x) >= (pointWidth + pointGap)
                                    # if the current point is the first point or if he's not overlapping
                                    # with the last good point then we set it as the new reference point 
                                    last_good_point = n
                                if last_good_point.id != n.id
                                    n.line += 1
                                    bad_points[i] = n
                                    delete line[i]
                        # we return the sorted remaining overlapping points 
                        _.sortBy bad_points, (e)-> e.x

                    # understand this loop as: while there is overlapping elements on the last
                    # line we have to create a new line with those elements
                    while !_.isEmpty (last_line = harmonize(lines[lines.length - 1]))
                        do()->
                            lines.push(last_line)

                    update(true)

                # Function that return a tick css 
                scope.tickStyle = (t)->
                        position: "absolute"
                        left: xpr(converted_current_value: t)

                # Function that return the point css
                scope.pointStyle = (d)->
                    # if it's not optimized (e.g: if we change the scale it's
                    # not optimized anymore) we have to reinitialize these 
                    # that help us to place the point during optimization
                    if !optimized
                        d.line = 0
                        d.x = x(d)

                    addPoint(d)
                    style = 
                        position: "absolute"
                        top     : y(d)
                        left    : xpr(d)
                        width   : pointWidth
                        height  : pointHeight

                    # we launch the optimization algorithm after each point is 
                    # placed and that update() method wasn't called by our 
                    # harmonization algorithm. 
                    if this.$last && !optimized 
                        this.$parent.harmonizePoints()
                        
                    return style

                # Add the ruler to the workspace
                scope.rulerStyle = ->
                    position: 'absolute'
                    top: 0
                    bottom: 0
                    left: xpr(converted_current_value: rulerValue)

                # Sets a class that determines
                # the direction of the ruler's label (left or right)
                scope.rulerClass = ->
                    xp = x(converted_current_value: rulerValue)
                    # 2 half of the screen?
                    if xp/workspaceWidth > 0.5 then "to-left" else "to-right"

                # Find the maximum Y of this serie
                maxY = Math.max.apply null, _.map(dataset, y)
                pointsHeight = maxY + pointHeight
                # Update workspace height
                element.find('.points').css "height", pointsHeight
                element.css "minWidth", workspaceWidth unless scope.overview()
    ]