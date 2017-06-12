
function check() {

    var liczba = document.getElementById("haslo1").value;

    if (liczba.length > 7) {

        document.getElementById("wynik").innerHTML = "Mocne";
    }
    else if ((liczba.length < 6) && (liczba.length > 4)) {
        document.getElementById("wynik").innerHTML = "Średnie";
    }
    else document.getElementById("wynik").innerHTML = "Słabe";

}
function check2() {
    var liczba1 = document.getElementById("haslo1").value;
    var liczba2 = document.getElementById("haslo2").value;


    if (liczba1 === liczba2) { }
    else document.getElementById("wynik2").innerHTML = "hasło się różnią";
}
function clean() {
    document.getElementById("wynik2").innerHTML = "";

}