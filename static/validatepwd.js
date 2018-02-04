$( document ).ready(function() {

	var newpass = $('#newpassword');
	var newpassTooltip = $('#wynik');

	var verifypass = $('#verifypassword');
	var verifypassTooltip = $('#wynik2');

	var submitbutton = $('#submitbutton');

	function check()
	{
		if(newpass.val().length > 7){
			newpassTooltip.css('color','green');
			newpassTooltip.html("Mocne");
		}
		else if((newpass.val().length < 6) && (newpass.val().length > 4)){
			newpassTooltip.css('color','orange');
			newpassTooltip.html("Średnie");
		}
		else {
			newpassTooltip.css('color','red');
			newpassTooltip.html("Słabe");
		}

		if(newpass.val() !== verifypass.val()){
			verifypassTooltip.css('color','red');
			verifypassTooltip.html("Hasła się różnią");
			submitbutton.attr( "disabled", true );

		}
		else {
			if(newpass.val() !== '' && verifypass.val() !== ''){
				verifypassTooltip.html("Hasła są takie same");
				verifypassTooltip.css('color','green');
				submitbutton.attr( "disabled", false );
			}
			else {
				newpassTooltip.html('');
				verifypassTooltip.html('');
				submitbutton.attr( "disabled", true );
			}
		}
	}

newpass.change(function(){
	check();
});

verifypass.change(function(){
	check();
});

});
