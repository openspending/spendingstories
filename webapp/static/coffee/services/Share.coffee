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

    getEmbedUrl : () =>
        currentUrl = (do @location.absUrl).split '?'
        vars = _.filter (currentUrl[1].split '&'), (elem) =>
            (not elem.match /^title=/) and (not elem.match /^visualization=/)
        vars.push "visualization=cards"
        vars = vars.join '&'
        url = "#{do @location.protocol}://#{do @location.host}"
        url += ":#{do @location.port}" if (do @location.port) isnt 80
        url += "/embed?#{vars}"

angular.module('storiesServices').service "shareService", ShareService