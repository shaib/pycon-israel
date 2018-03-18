/* 
This file is copied from the pinax-blog sources
to work around it not being shipped with pinax-blog as of 7.0.3
See https://github.com/pinax/pinax-blog/issues/112
*/
var djJq = django.jQuery;

djJq(document).ready(function  () {
	djJq("#id_teaser").on("propertychange change keyup paste input", function(){
		djJq("#id_description").val(djJq("#id_teaser").val());
	});
})
