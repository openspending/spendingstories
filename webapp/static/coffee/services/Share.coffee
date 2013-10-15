class ShareService

    @$inject : ['$location']

    constructor : (@location) ->

    getSharingUrl : (visualization="scale") =>
        currentUrl = (do @location.absUrl).split '?'
        vars = _.filter (currentUrl[1].split '&'), (elem) =>
            (not elem.match /^title=/) and (not elem.match /^visualization=/)
        vars.push "visualization=#{visualization}"
        currentUrl[1] = vars.join '&'
        currentUrl.join '?'


angular.module('storiesServices').service "shareService", ShareService