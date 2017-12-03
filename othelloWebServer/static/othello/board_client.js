var updateURL = "http://group02.dhcp.nd.edu:8000/othello/update";
createBoard();
function createBoard()
{
    var gamestate = "";
    var table = document.createElement("table");
    for (let i = 0; i < 8; i++) {
        var tr = document.createElement("tr");
        for (let j = 0; j < 8; j++) {
            var td = document.createElement("td");
            td.id = i.toString() + ":" + j.toString();  // this is how to identify a cell --> row:column
            // assign white and black
            if (i%2 == j%2) {
                td.className = "seagreen";
            } else {
                td.className = "green";
            }
            if ((i == 3 && j == 3) || (i == 4 && j == 4))
            {
                var circle = document.createElement("div");
                circle.className = "blackCircle";
                td.appendChild(circle);
                gamestate += "B";
            }
            else if ((i == 3 && j == 4) || (i == 4 && j == 3))
            {
                var circle = document.createElement("div");
                circle.className = "whiteCircle";
                td.appendChild(circle);
                gamestate += "W";
            }
            else
            {
                gamestate += "G";
            }
            td.onclick = function () {
                //alert("Row: " + i.toString() + "\nColumn: " + j.toString());
                //alert(gamestate);
                // POST
                var xhttp_post = new XMLHttpRequest();
                xhttp_post.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200)
                    {
                        console.log(this.responseText);
                        let new_gamestate = JSON.parse(this.responseText).gamestate;
                        updateGameState(new_gamestate);
                        setTimeout(function() {
                                // GET
                                var xhttp_get = new XMLHttpRequest();
                                xhttp_get.onreadystatechange = function() {
                                    if (this.readyState == 4 && this.status == 200)
                                    {
                                        let new_gamestate = JSON.parse(this.responseText).gamestate;
                                        updateGameState(new_gamestate);
                                    }
                                };
                                xhttp_get.open("GET", updateURL, true);
                                xhttp_get.send();
                        }, 2000);
                    }
                };
                var formData = new FormData();
                formData.append("row", i);
                formData.append("column", j);
                xhttp_post.open("POST", updateURL, true);
                xhttp_post.send(formData);
            };
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    $("#board").html(table);
}
function updateGameState(gamestring)
{
    //console.log("updating gamestring");
                
                let row;
    let column;
    for (let i = 0; i < gamestring.length; i++)
    {
        row = Math.floor(i/8);
        column = i%8;
        let gamechar = gamestring[i];
        let gamecell = document.getElementById(row.toString() + ":" + column.toString());
        let circle = document.createElement("div");
        if (gamechar == "O")
        {
            circle.className = "whiteCircle";
        }
        else if (gamechar == "X")
        {
            circle.className = "blackCircle";        
        }
        if(gamecell.hasChildNodes()) {
            gamecell.removeChild(gamecell.lastChild);
        }
        gamecell.appendChild(circle);
    }
}