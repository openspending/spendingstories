angular.module('storiesServices').factory "Filters", ["$location", ($location)->
    @searchParams = $location.search()
    ### 
    Each filter can be described as following :
        @stackable:
            the filter can be added to the "filter bar"
        @type:      
            the type of the filter value
        @value:     
            the current filter value 
        @modes:
            array of supported visualization mode for the filter 
            will hide the filter if it's not supported and remove 
            this parameters from url.
    ### 
    onlySticky:
        stackable: false
        type: 'boolean'
        value: @searchParams.onlySticky
        modes: ['cards']
    country:
        name: 'Country'
        type: 'string'
        stackable: true 
        value: @searchParams.country
        modes: ['cards', 'scale']
    currency:
        name: 'Currency'
        type: 'string'
        stackable: true
        value: @searchParams.currency
        modes: ['cards', 'scale']
    themes:
        type: 'array'
        stackable: false
        value: if @searchParams.themes? then @searchParams.themes.split(',')
        modes: ['cards', 'scale']
    title:
        name: 'Title'
        type: 'string'
        stackable: true
        value: @searchParams.title
        modes: ['cards', 'scale']
    # Not handled for the moment
    # type:
        # name: 'Type'
        # type: 'string'
        # stackable: true 
        # value: if @searchParams.type? then @searchParams.type
        # modes: ['cards', 'scale']
]