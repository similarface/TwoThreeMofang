var dialogFirst=true;
function dialog(title,content,width,height,cssName){
if(dialogFirst==true){
  var temp_float=new String;
  temp_float="<div id=\"FloatBg\"  style=\"height:"+$(document).height()+"px;width:"+$(document).width()+"px;filter:alpha(opacity=0);opacity:0;\"></div>";
  temp_float+="<div id=\"FloatBoxBg\" ></div>";
  temp_float+="<div id=\"FloatBox\">";
  temp_float+="<div class=\"title\"><h4></h4><span class=\"DialogClose\" title=\"关闭\"></span></div>";
  temp_float+="<div class=\"content link_lan\"></div>";
  temp_float+="</div>";
  $("body").append(temp_float);
  dialogFirst=false;
}

function DialogClose()
{
	$("#FloatBg").hide();
	$("#FloatBoxBg").hide();
	$("#FloatBox").hide();
}
function SetBoxBg()
{
	var FloatBoxWidth=$("#FloatBox").width();
	var FloatBoxHeight=$("#FloatBox").height();
	var FloatBoxLeft=$("#FloatBox").offset().left;
	var FloatBoxTop=$("#FloatBox").offset().top;
	$("#FloatBoxBg").css({display:"block",width:(FloatBoxWidth+12)+"px",height:(FloatBoxHeight+12)+"px"});
	$("#FloatBoxBg").css({left:(FloatBoxLeft-5)+"px",top:(FloatBoxTop-5)+"px"});
}
$(".DialogClose").click(function(){DialogClose();});
$("#FloatBox .title h4").html(title);
contentType=content.substring(0,content.indexOf(":"));
content=content.substring(content.indexOf(":")+1,content.length);
switch(contentType){
  case "url":
  var content_array=content.split("?");
  $.ajax({
    type:content_array[0],
    url:content_array[1],
    data:content_array[2],
	error:function(){
	  $("#FloatBox .content").html("error...");
	  SetBoxBg();
	},
    success:function(html){
		//alert(html);
      $("#FloatBox .content").html(html);
	  SetBoxBg();
    }
  });
  break;
  case "text":
  $("#FloatBox .content").html(content);
  SetBoxBg();
  break;
  case "id":
  $("#FloatBox .content").html($("#"+content+"").html());
  SetBoxBg();
  break;
  case "iframe":
  $("#FloatBox .content").html("<iframe src=\""+content+"\" width=\"100%\" height=\""+(parseInt(height)-30)+"px"+"\" scrolling=\"auto\" frameborder=\"0\" marginheight=\"0\" marginwidth=\"0\"></iframe>");
  SetBoxBg();
}

$("#FloatBg").show();
$("#FloatBg").css("opacity", 0);
$("#FloatBoxBg").css("opacity", 0.2);
$("#FloatBox").attr("class",cssName);
$("#FloatBox").css({display:"block",left:(($(document).width())/2-(parseInt(width)/2))+"px",top:($(document).scrollTop()+120)+"px",width:width,height:height});
SetBoxBg();
$("#FloatBox .DialogClose").hover(function(){$(this).addClass("spanhover")},function(){$(this).removeClass("spanhover")});
}