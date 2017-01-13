var gamelistvalue = new Array();
var gamelistunit = new Array();
var modgamelistvalue = new Array();
var pricetotal,
    total,
    hdunit,
    how_long;

function lightscreen(){
    document.getElementById('lightscreen').style.display = 'block';
    document.getElementById('lightscreenform').style.display = 'block';
}
function typecheck(select_type){
    if(select_type === 'All'){
        for (i=0; i<document.getElementsByName('includegame').length; i++){
            document.getElementsByName('includegame')[i].checked=true;
        }
    }
    else if(select_type === 'None'){
        for (i=0; i<document.getElementsByName('includegame').length; i++){
            document.getElementsByName('includegame')[i].checked=false;
        }
    }
    else if(select_type === 'Game'){
        $.each($('.type_col'), function(index){
            if($('.type_col')[index].innerHTML === 'Game'){
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'DLC'){
        $.each($('.type_col'), function(index){
            if($('.type_col')[index].innerHTML === 'DLC'){
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'App'){
        $.each($('.type_col'), function(index){
            if($('.type_col')[index].innerHTML === 'App'){
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'Movie'){
        $.each($('.type_col'), function(index){
            if($('.type_col')[index].innerHTML === 'Movie'){
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.type_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'Mac'){
        $.each($('.os_col'), function(index){
            if($(this).hasClass('mac_os')){
                $('.os_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.os_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'Linux'){
        $.each($('.os_col'), function(index){
            if($(this).hasClass('linux_os')){
                $('.os_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.os_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'Multiplayer'){
        $.each($('.multiplay_col'), function(index){
            if($(this).text() === 'Yes'){
                $('.multiplay_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.multiplay_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else if(select_type === 'Controller'){
        $.each($('.contoller_col'), function(index){
            if(($(this).text() === 'partial') || ($(this).text() === 'full')){
                $('.contoller_col')[index].parentNode.firstChild.firstChild.checked=true;
            }
            else{
                $('.contoller_col')[index].parentNode.firstChild.firstChild.checked=false;
            }
        });
    }
    else{
    }
    update_count();
}
function checkall(x){
    if(x.checked){
        for (i=0; i<document.getElementsByName('includegame').length; i++){
            document.getElementsByName('includegame')[i].checked=true;
        }
    }
    else{
        for (i=0; i<document.getElementsByName('includegame').length; i++){
            document.getElementsByName('includegame')[i].checked=false;
        }
    }
    update_count();
}
function checkgame(x){
    x.parentNode.firstChild.firstChild.click();
    update_count();
    // if(x.checked){
        // x.parentNode.parentNode.style.background='black'
    // }
}
function update_unit(){
    if(document.getElementById('unit_GB').checked){
        $.each($('.size_col'), function(index, value){
            if($('.unit_col')[index].innerHTML == 'MB'){
                value.innerHTML /= 1000;
                $('.unit_col')[index].innerHTML = 'GB';
            }
        });
    }
    if(document.getElementById('unit_MB').checked){
        $.each($('.size_col'), function(index, value){
            if($('.unit_col')[index].innerHTML == 'GB'){
                value.innerHTML *= 1000;
                $('.unit_col')[index].innerHTML = 'MB';
            }
        });
    }
    $('#gamelist').trigger('update')
}
function update_count(){
    gamelistplayed=[]
    gamelistprice=[]
    gamelistvalue=[];
    gamelistunit=[];
    modgamelistvalue=[];

    $('.checkbox_col input:checked').each(function() {
        gamelistplayed.push($(this).parent().nextAll('.playtime_col').text());
    });
    playtimetotal = 0;
    for (var i = 0; i < gamelistplayed.length; i++) {
        playtimetotal += parseFloat(gamelistplayed[i]);
    }
    playtimetotal = Math.round(playtimetotal*100)/100;
    $('.checkbox_col input:checked').each(function(){
        if (isNaN($(this).parent().nextAll('.value_col').text())){
            gamelistprice.push(0);
        }
        else{
            gamelistprice.push(parseFloat($(this).parent().nextAll('.value_col').text()));
        }
    });
    pricetotal = 0;
    for (var i = 0; i < gamelistprice.length; i++) {
        pricetotal += parseFloat(gamelistprice[i]);
    }
    pricetotal = Math.round(pricetotal*100)/100;
    $('.checkbox_col input:checked').each(function() {
        gamelistvalue.push($(this).parent().nextAll('.size_col').text());
    });
    $('.checkbox_col input:checked').each(function() {
        gamelistunit.push($(this).parent().nextAll('.unit_col').text());
    });
    $.each(gamelistunit, function(index, value){
        if(value == 'MB'){
            modgamelistvalue.push((gamelistvalue[index]));
        }
        else if(value == 'GB'){
            modgamelistvalue.push((gamelistvalue[index]*1000));
        }
        else if(value == 'TB'){
            modgamelistvalue.push((gamelistvalue[index]*1000000));
        }
        else if(value == '-'){
            modgamelistvalue.push(0);
        }
        else{
            modgamelistvalue.push(0);
        }
    });
    total = 0;
    for (var i = 0; i < modgamelistvalue.length; i++) {
        total += parseInt(modgamelistvalue[i]);
    }
    if (year_diff > 1){
        how_long = 'Over the last '+year_diff+' years, ';
    }
    else{
        how_long = 'Over the last '+year_diff+' year, ';
    }
    if (total > 1000){
        total /= 1000;
        total = Math.round(total*100)/100;
        $('#size_footer').text(total);
        $('#unit_footer').text('GB');
        hdunit = 'GB'
        $('.top-summary').text(how_long+'you\'ve spent '+playtimetotal+' hours playing this selection, which includes '+modgamelistvalue.length+' items, is valued at $'+pricetotal+', and requires '+total+' '+hdunit);
        update_bar(total, hdunit);
    }
    else{
        total = Math.round(total*100)/100;
        $('#size_footer').text(total);
        $('#unit_footer').text('MB');
        $('.top-summary').text(how_long+'you\'ve spent '+playtimetotal+' hours playing this selection, which includes '+modgamelistvalue.length+' items, is valued at $'+pricetotal+', and requires '+total+' '+hdunit);
        hdunit = 'MB'
        update_bar(total, hdunit);
    }
    /* Update game count */
    $('#gamename_footer').text(gamelistprice.length+' items');
    $('#playtime_footer').text(playtimetotal+' hours');
    $('#value_footer').text('$'+pricetotal);
    $('#gamelist').trigger('update');
}
/* Get total game size */
function update_bar(select_val, select_unit){
    gamelistvalue=[];
    gamelistunit=[];
    modgamelistvalue=[];
    $('.size_col').each(function() {
        gamelistvalue.push($(this).text());
    });
    $('.unit_col').each(function() {
        gamelistunit.push($(this).text());
    });
    $.each(gamelistunit, function(index, value){
        if(value == 'MB'){
            modgamelistvalue.push((gamelistvalue[index]));
        }
        else if(value == 'GB'){
            modgamelistvalue.push((gamelistvalue[index]*1000));
        }
        else if(value == 'TB'){
            modgamelistvalue.push((gamelistvalue[index]*1000000));
        }
        else if(value == '-'){
            modgamelistvalue.push(0);
        }
        else{
            modgamelistvalue.push(0);
        }
    });
    var total = 0;
    for (var i = 0; i < modgamelistvalue.length; i++) {
        total += parseInt(modgamelistvalue[i]);
    }
    if(select_unit == 'GB'){
        total /= 1000;
    }
    document.getElementById('game_selection_bar').style.width=Math.round((select_val/total)*100)+'%';
    // $('#game_total_bar').text('');
    // $('#game_selection_bar').text('');
}
function missingno(){
    $('.flag').remove();
    $('.gamename_col').each(function()
    {
        // if(this.innerHTML === "-"){
            // var newdiv = document.createElement('div');
            // newdiv.innerHTML = '<i style="padding:0px 10px;" class="icon-remove" onclick="$(this).parent().prev().remove();$(\'#gamelist\').trigger(\'update\');"></i>&nbsp;<i class="icon-flag"></i>';
            // newdiv.setAttribute('class', 'flag');
            // $(newdiv).insertAfter(this.parentNode)
        // }
        var newdiv = document.createElement('div');
        newdiv.innerHTML = '<i class="icon-remove" onclick="delrow($(this).parent());"></i>';
        newdiv.setAttribute('class', 'flag');
        $(newdiv).insertAfter(this.parentNode)
    });
}
function delrow(marked_row){
    marked_row.prev().find('.includegame').click();
    marked_row.prev().remove();
    update_count();
    marked_row.remove();
}
function create_social(){
    var twitter = '<a style="color:#0094C2;" class="custom-share" href="https://twitter.com/share?url='+document.URL+'&text=My%20%23Steam%20account%20has%20'+modgamelistvalue.length+'%20items%20valued%20at%20%24'+pricetotal+'%20and%20requires%20'+total+' '+hdunit+'%20of%20disk%20space%3A" onclick="javascript:window.open(this.href,\'\', \'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=275,width=500\');return false;"><i class="icon-twitter-sign"></i></a>';
    var googleplus = '<a style="color:#d94f30;" class="custom-share" href="https://plus.google.com/share?url='+document.URL+'" onclick="javascript:window.open(this.href,\'\', \'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=275,width=500\');return false;"><i class="icon-google-plus-sign"></i></a>';
    var facebook = '<a style="color:#3b5998;" class="custom-share" href="https://www.facebook.com/sharer/sharer.php?u='+document.URL+'" onclick="javascript:window.open(this.href,\'\', \'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=275,width=500\');return false;"><i class="icon-facebook-sign"></i></a>';
    var soc = document.createElement('div');
    soc.innerHTML = 'Share:'+twitter+' '+googleplus+' '+facebook;
    soc.setAttribute('id', 'socialdiv');
    $(soc).insertAfter($('#dl_link'));
}
// $(document).ready(function(){
        // $.tablesorter.addParser({
            // id: 'input'
            // is: function(s) {
                // return false;
            // },
            // format: function(s, t, node) {
                // return $('input[type=checkbox]', node).is(':checked') ? 1 : 0;
            // },
            // type: 'numeric'
        // });
        // $('#gamelist').tablesorter({headers:{0:{sorter:'input'}}});
        // $("#gamelist").tablesorter({headers:{0:{sorter:false}}});
        // $("#gamelist").bind("sortEnd",function(){
            // $('.flag').remove();
            // missingno();
        // });
    // }
// );
// window.onload = function(){
    // $('.win_os').append('<i class="icon-windows"></i>');
    // $('.mac_os').append('<i class="icon-apple"></i>');
    // $('.linux_os').append('<i class="icon-tux"></i>');
    // update_count();
    // create_social();
    // if ($('.gamerow')[0].firstChild.innerHTML === ''){
        // $('#dl_link').remove();
        // $('#socialdiv').remove();
        // $('#useravatar').remove();
    // }
    // $('#unit_MB').click();
    // update_unit();
// }
