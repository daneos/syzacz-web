function check()
{
	var liczba = document.getElementById("password").value;
	if(liczba.length > 7)
		document.getElementById("wynik").innerHTML="Mocne";
	else if((liczba.length < 6) && (liczba.length > 4))
		document.getElementById("wynik").innerHTML="Średnie";
	else
		document.getElementById("wynik").innerHTML="Słabe";	 
}

function check2()
{
	var liczba1 = document.getElementById("password").value;
	var liczba2= document.getElementById("password2").value;
	if(liczba1!==liczba2)
		document.getElementById("wynik2").innerHTML="hasło się różnią";
}

function clean()
{
	document.getElementById("wynik2").innerHTML="";
}