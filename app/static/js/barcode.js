// var priceEls = document.getElementsByClassName("alert alert-info");
// for (var i = 0; i < priceEls.length; i++) {
// var price = priceEls[i].innerText;
// var result = price.slice(2)
// }

getReworkId = function(){
    var url = window.location.pathname;
    var id = url.substring(url.lastIndexOf('/') + 1);
    return id;
}       
var my_id = getReworkId();
var stroka = '';
var len_id = my_id.length;
var const_len = 9;
while(len_id < const_len){
    stroka = stroka + "0";
    len_id++;
    }
var result = stroka.concat(my_id);
// getBarcodeNum = function(){
//     var res = '';
//     var len_id = my_id.length;
//     var const_len = 9;
//     while(len_id < const_len){
//         stroka = stroka + "0";
//         len_id++;
//     }
//     return res = stroka.concat(my_id);
// }
// var result = getBarcodeNum();

 
