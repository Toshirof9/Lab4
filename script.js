function displayReserves(data) {
    var reservesList = document.getElementById("reserves-list");
    reservesList.innerHTML = "";

    for (var i = 0; i < data.length; i++) {
        var reserve = data[i];
        var li = document.createElement("li");
        li.textContent = reserve.dt + " - " + reserve.txt + ": " + reserve.value;
        reservesList.appendChild(li);
    }
}

function fetchReserves(year, month) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://bank.gov.ua/NBUStatService/v1/statdirectory/res?date=" + year + (month < 10 ? "0" + month : month), true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var xmlData = xhr.responseText;
                var parser = new DOMParser();
                var xmlDoc = parser.parseFromString(xmlData, "text/xml");

                var reserves = xmlDoc.getElementsByTagName("res");
                var data = [];

                for (var i = 0; i < reserves.length; i++) {
                    var reserve = reserves[i];
                    var dt = reserve.getElementsByTagName("dt")[0].textContent;
                    var txt = reserve.getElementsByTagName("txt")[0].textContent;
                    var value = reserve.getElementsByTagName("value")[0].textContent;

                    data.push({ dt: dt, txt: txt, value: value });
                }

                displayReserves(data);
            } else {
                displayError("Помилка підключення. Спробуйте знову.");
            }
        }
    };
    xhr.send();
}

function displayError(message) {
    var errorMessage = document.getElementById("error-message");
    errorMessage.textContent = message;
}

var form = document.getElementById("input-form");
form.addEventListener("submit", function(event) {
    event.preventDefault();
    var year = document.getElementById("year").value;
    var month = document.getElementById("month").value;
    fetchReserves(year, month);
});