# ──────────────────────────────────────────────────────────────────────────────
# Contribute controller handles contribution form's behavior 
# ──────────────────────────────────────────────────────────────────────────────
class ContributeCtrl

    @$inject: ['$scope', 'Currency','Restangular', 'Page']

    constructor: (@scope, @Currency, @Restangular, @Page)->
        @Page.setTitle('Contribute')
        # ──────────────────────────────────────────────────────────────────────
        # Scope variables binding // AngularJS Models 
        # ──────────────────────────────────────────────────────────────────────  
        # Start from the first step
        @scope.stepCount  = 3
        @scope.step 	  = 0
        @scope.loading    = false
        # Currencies list
        @scope.currencies = Currency.list
        # Countries list
        @scope.countries  = Restangular.all("countries").getList()    
        @scope.themes     = Restangular.all("themes").getList()    
        # The story to build
        @scope.story      = currency: 'USD'

        # ──────────────────────────────────────────────────────────────────────
        # Scope function binding 
        # ──────────────────────────────────────────────────────────────────────
        @scope.getForm       = @getForm 
        @scope.isDone        = @isDone
        @scope.progressStyle = @progressStyle
        @scope.reset         = @resetForm 
        @scope.submit        = @submitForm

    getForm: (step=@scope.step)=> 
        if step >= @scope.stepCount
            title = 'Thanks for contributing'
        else
            title = "Contribute / Step #{step+1}"

        @Page.setTitle(title) 
        @scope["stepForm"+step]

    isDone: => @scope.step == @scope.stepCount
    
    submitForm: =>
        # Send the data to the API
        @scope.loading = true
        # Post the story
        @Restangular.all("stories").post(@scope.story).then => 
            # Disables loading mode
            @scope.loading = false
            # No error to show
            @scope.errors  = []
            # Then go to last-step + 1 where we thank the contributor
            @scope.step    = @scope.stepCount  
        # Handle error
        , (response) => 
            # Disables loading mode
            @scope.loading = false
            # Record response as error
            @scope.errors = response.data


    # Reset the form
    resetForm: =>
        @scope.story = currency: 'USD'
        @scope.step  = 0                  

    # Get the style of the progressbar
    # according the state of the current step's form
    progressStyle: =>
        stepCompleted = @scope.step 
        # Is the current step valid ?
        # stepCompleted++ if @scope.getForm().$valid
        # Style of the progress bar
        width: (stepCompleted/@scope.stepCount)*100 + '%'

angular.module('stories').controller 'contributeCtrl', ContributeCtrl