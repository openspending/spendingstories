class ShareService

    @$inject : ['$location']

    constructor : (@location) ->

    getBaseUrl : () =>
        url = "#{do @location.protocol}://#{do @location.host}"
        url += ":#{do @location.port}" if (do @location.port) isnt 80
        url

    getBaseSearch : () =>
        search = do @location.search
        "q=#{search.q}&c=#{search.c}"

    getSharingAddress : (title, viz='scale') =>
        (do @getBaseUrl) + "/#/search/?#{do @getBaseSearch}&visualization=#{viz}&title=#{title}"

    getEmbedFrame : (title) =>
        url = do @getBaseUrl
        url += "/embed?#{do @getBaseSearch}&title=#{title}"
        '<iframe src="' + url + '" width="244" height="242" frameborder="0"></iframe>'

angular.module('storiesServices').service "shareService", ShareService