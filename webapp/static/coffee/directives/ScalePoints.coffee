angular.module('stories')
    .directive "scalePoints", ()->     
        # Returned object to that defines the directive
        restrict: "EAC"
        templateUrl: "/partial/scale-points.html"
        replace: true
        scope:
            data        : "="
            current     : "="
            onClick     : "="
            rulerValue  : "="
            filter      : "&"
            pointGap    : "&"
            pointWidth  : "&"
            pointHeight : "&"
        link: (scope, element, attrs)->                               
            # Data must be loaded
            return unless scope.data? and scope.data.length

            # Get optional visualization opt
            pointWidth     = scope.pointWidth()  or 20
            pointHeight    = scope.pointHeight() or 20
            pointGap       = scope.pointGap()    or 7
            # Ruler that "split" the screen
            rulerValue     = scope.rulerValue or -1
            # Where we insert the point
            workspace      = d3.select(element[0])
            # Width of the workspace according to its parent
            workspaceWidth = element.innerWidth()            

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
            # Order dataset to avoid caothic stacking
            dataset = _.sortBy dataset, "current_value_usd" 
            # Put the processed data into a dedicated field
            scope.dataset = dataset

            # Bounds values (using sorted list)            
            min = dataset[0].current_value_usd 
            max = dataset[dataset.length-1].current_value_usd                
            # And extend the scale with the bounds                    
            scale = d3.scale.log().domain [ min, max ]
            # these variables help us to know if we have to go to the next line
            lastY = lastX = -(pointWidth+pointGap)
            # Create position functions 
            x  = (d)-> scale(d.current_value_usd)*workspaceWidth            
            y  = (d)->                   
                if x(d) - lastX >= pointWidth + pointGap       
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
                width   : pointWidth
                height  : pointHeight

            # Add the ruler to the workspace
            scope.rulerStyle = ->
                position: 'absolute'
                top: 0
                bottom: 0
                left: xpr(current_value_usd: rulerValue)

            # Find the maximum Y of this serie
            maxY = Math.max.apply null, _.map(dataset, y)
            # Update workspace height
            element.css "height", maxY + pointHeight    