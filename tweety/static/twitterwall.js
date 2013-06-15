(function($) {
    $.fn.hasScrollBar = function() {
        return this.get(0).scrollHeight > this.height();
    }
})(jQuery);

$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});

var interval = 1500;
var lastpk = 0;

$(document).ready(function() {
	init();
	setInterval(addItem, interval);
});

function init()
{
	$.ajax({
        url: "/json?limit=40",
		async: false,
		contenttype: 'application/json; charset=utf-8',
		datatype: 'json',
		cache: false,
		success: function(data){
				lastpk = data[data.length - 1].pk;
		}
	});
}

function addItem()
{
	$.ajax({
		url: "/getnext?item="+lastpk,
		async: false,
		contenttype: 'application/json; charset=utf-8',
		datatype: 'json',
		cache: false,
		success: function(data){

			$.each(data, function(i,item){
                                var media_url;

				if(item.pk > lastpk)
					lastpk = item.pk;

                                if ( item.fields.message_media_url != null ) {
                                    media_url = item.fields.message_media_url;
                                } else {
                                    media_url = undefined;
                                }

				if(item.fields.visible)
				{
					var d = new Date(item.fields.message_date);
					createTweet(item.fields.message_origin,
                                            item.fields.message_avatar,
                                            item.fields.message_text,
                                            item.fields.message_date,
                                            media_url );
				}
			});
		}
	});
}

function createTweet(from, avatar, msg, time, picture)
{
	var inner = '<div class="msgcontainer" style="display:none;">';
    inner += '<div class="msgtitle">';
    inner += '<div class="avatar"><img class="avatar" src="'+avatar+'" /></div>';
	inner += '<div class="title">'+from+'</div>';
	inner += '<div class="time"><time class="timeago" datetime="'+time+'">'+time+'</time></div></div>';
	inner += '<div class="msg">'+msg+'</div>';
        if (picture) {
            inner += '<img class="embedded_media" src="'+picture+'" />';
        }
        inner += '</div>';
	var new_div = $(inner).hide();
	$('.msglist').prepend(new_div);
	$(".timeago").timeago();
	new_div.slideDown(800, afterInsert);
}

function afterInsert()
{
	if($(".msglist").hasScrollBar())
	{
		$('.msglist .msgcontainer:last-child').remove();
	}
}
