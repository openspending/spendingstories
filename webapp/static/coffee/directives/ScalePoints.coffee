angular.module('stories')
    .directive "scalePoints", ()->     
        # Constants
        pointWidth   = 20
        pointHeight  = 20
        pointGap     = 5 
        # Returned object to that defines the directive
        restrict: "EAC"
        template: '<div class="one-scale-points"></div>'
        replace: false
        scope:
            data: "="
        link: (scope, element, attrs)->                       
            # Data must be loaded
            return unless scope.data.length
            # Where we insert the point
            workspace      = d3.select(element[0])
            # Width of the workspace according to its parent
            workspaceWidth = element.parent().innerWidth()            
            # Order data to avoid caothic stacking
            data  = _.sortBy scope.data, "current_value_usd"
            # Bounds values (using sorted list)            
            min = data[0].current_value_usd 
            max = data[data.length-1].current_value_usd                
            # And extend the scale with the bounds                    
            scale = d3.scale.linear().domain [ min, max ]
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
            # Pixel value
            ypx = (d)-> y(d) + "px"

            # Select the future points
            workspace.selectAll("div.point")
                .data(data)
                .enter()
                .append("div")
                    .attr("class"    , "point")
                    .style("position", "absolute")
                    .style("top"     , ypx)
                    .style("left"    , xpr)
                    .style("width"   , pointWidth  + "px")
                    .style("height"  , pointHeight + "px")                    