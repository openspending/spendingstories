angular.module('stories')
    .directive "scalePoints", ()->     
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
            # Data must be loaded
            return unless scope.data? and scope.data.length

            # Get optional visualization opt
            pointWidth     = scope.pointWidth()     or 25
            pointHeight    = scope.pointHeight()    or 25
            pointWidthBig  = scope.pointWidthBig()  or 200
            pointHeightBig = scope.pointHeightBig() or 60
            pointGap       = scope.pointGap()       or 7
            pointGapBig    = scope.pointGapBig()    or 7
            # Ruler that "split" the screen
            rulerValue     = 1*scope.rulerValue or -1
            # Where we insert the point
            workspace      = d3.select(element[0])
            # Width of the workspace according to its parent
            workspaceWidth = if scope.overview() then element.innerWidth() else 6000

            # Static positioning must be change to relative
            if element.css("position") is "static"
                # Using relative position allow us to position points
                # accoding the top left corner of the workspace
                element.css("position", "relative")

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
            # Put the processed data into a dedicated field
            scope.dataset = dataset

            # Bounds values (using sorted list)            
            min = Math.min dataset[0].current_value_usd, rulerValue 
            max = Math.max dataset[dataset.length-1].current_value_usd, rulerValue          
            # And extend the scale with the bounds                    
            scale = d3.scale.log().domain [ min, max ]
            # these variables help us to know if we have to go to the next line
            lastY = lastX = -(pointWidth+pointGap)
            # Create position functions 
            x  = (d)-> scale(d.current_value_usd)*workspaceWidth            
            y  = (d)->                   
                pointWidth  = if scope.overview() then pointWidth  else pointWidthBig
                pointHeight = if scope.overview() then pointHeight else pointHeightBig
                pointGap    = if scope.overview() then pointGap    else pointGapBig

                if Math.abs(x(d) - lastX) >= pointWidth + pointGap       
                    lastY = 0
                else                    
                    lastY = lastY + pointHeight + pointGap
                # Record the current value as last x
                lastX = x(d)
                lastY
            # Percentage value (to allow resizing)
            xpr = (d)-> x(d)/workspaceWidth*100 + "%"

            # Function that return the point css
            scope.pointStyle = (d)->
                position: "absolute"
                top     : y(d)
                left    : xpr(d)
                width   : if scope.overview() then pointWidth else pointWidthBig
                height  : if scope.overview() then pointHeight else pointHeightBig

            # Add the ruler to the workspace
            scope.rulerStyle = ->
                position: 'absolute'
                top: 0
                bottom: 0
                left: xpr(current_value_usd: rulerValue)

            # Sets a class that determines
            # the direction of the ruler's label (left or right)
            scope.rulerClass = ->
                xp = x(current_value_usd: rulerValue)
                # 2 half of the screen?
                if xp/workspaceWidth > 0.5 then "to-left" else "to-right"


            # Find the maximum Y of this serie
            maxY = Math.max.apply null, _.map(dataset, y)
            # Update workspace height
            element.css "height", maxY + pointHeight    
            element.css "minWidth", workspaceWidth unless scope.overview()