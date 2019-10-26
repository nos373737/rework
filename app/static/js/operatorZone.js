getLastSymbolUrl = function(){
    var urlString = window.location.href;
    var url = new URL(urlString);
    var id = url.searchParams.get("id");
    return id;
}
var urlId = getLastSymbolUrl();
