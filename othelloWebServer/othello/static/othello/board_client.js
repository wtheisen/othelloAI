var updateURL = "http://localhost:1337/update";

createBoard();

function createBoard()
{
    var gamestate = "";

    var table = document.createElement("table");
    for (let i = 1; i < 9; i++) {
        var tr = document.createElement("tr");
        for (let j = 1; j < 9; j++) {
            var td = document.createElement("td");
            td.id = i.toString() + ":" + j.toString();  // this is how to identify a cell --> row:column

            // assign white and black
            if (i%2 == j%2) {
                td.className = "seagreen";
            } else {
                td.className = "green";
            }

            if ((i == 4 && j == 4) || (i == 5 && j == 5))
            {
                var circle = document.createElement("div");
                circle.className = "blackCircle";

                td.appendChild(circle);

                gamestate += "B";
            }
            else if ((i == 4 && j == 5) || (i == 5 && j == 4))
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

                alert("Row: " + i.toString() + "\nColumn: " + j.toString());

                alert(gamestate);

                var xhttp = new XMLHttpRequest();

                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200)
                    {
                        console.log(this.responseText);
                        let new_gamestate = JSON.parse(this.responseText).gamestate;

                        updateGameState(new_gamestate);
                    }
                };

                xhttp.open("POST", updateURL, true);
                xhttp.send("row=" + i.toString() + "&" + "column=" + j.toString() + 
                            "&" + "gamestate=" + gamestate + "&" + "player=" + "P1");

            };
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    document.body.appendChild(table);
}


function updateGameState(gamestring)
{
    let row;
    let column;

    for (let i = 1; i <= gamestring.length; i++)
    {

        if (i <= 8)
        {
            row = 1;
        }
        else if (i <= 16)
        {
            row = 2;
        }
        else if (i <= 24)
        {
            row = 3;
        }
        else if (i <= 32)
        {
            row = 4;
        }
        else if (i <= 40)
        {
            row = 5;
        }
        else if (i <= 48)
        {
            row = 6;
        }
        else if (i <= 56)
        {
            row = 7;
        }
        else if (i <= 64)
        {
            row = 8;
        }

        column = (i % 8 != 0) ? i % 8 : 8;

        let gamechar = gamestring[i-1];
        let gamecell = document.getElementById(row.toString() + ":" + column.toString());

        if (gamechar == "B" && !gamecell.hasChildNodes())
        {
            let circle = document.createElement("div");
            circle.className = "blackCircle";

            gamecell.appendChild(circle);
        }
        else if (gamechar == "W" && !gamecell.hasChildNodes())
        {
            let circle = document.createElement("div");
            circle.className = "whiteCircle";

            gamecell.appendChild(circle);
        }
    }
}


