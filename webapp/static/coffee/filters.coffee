angular
    .module('storiesFilters', [])
    .filter("nl2br", ->
        return (str='')-> (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')
    )
    .filter("thousandRound", ->
        return (n)-> Math.round(n/1000)*1000
    )
    .filter("thousandSeparator", ->
        return (nStr, sep=",")->
            nStr = "" + (nStr or "")
            x = nStr.split(".")
            x1 = x[0]
            x2 = (if x.length > 1 then "." + x[1] else "")
            rgx = /(\d+)(\d{3})/
            x1 = x1.replace(rgx, "$1" + sep + "$2") while rgx.test(x1)
            x1 + x2
    ).filter("simpleMillion", ->
        return (n)-> Math.round(n/Math.pow(10, 5))/10
    ).filter("decimalSeparator", ->
        return (n, dec=".")-> (n+"").replace /\./, dec
    )