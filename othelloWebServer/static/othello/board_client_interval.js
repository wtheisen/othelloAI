var updateURL = "http://group02.dhcp.nd.edu:8080/othello/update";

// creates HTML board and puts pieces on it
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

                // check if row/column is invalid move -- iterate over list ??
                    // alert("Invalid Move! Please pick a valid move.");

                // else
                    // POST -- Player Move
                    var xhttp_post = new XMLHttpRequest();

                    xhttp_post.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200)
                        {
                            let new_gamestate = JSON.parse(this.responseText).gamestate;
                            updateGameState(new_gamestate);

                            // if game ends -- if JSON.parse(this.responseText).end == "true" ??
                                // alert(JSON.parse(this.responseText).winner + " wins!");

                            // else
                                if (checkIfValidMoves("AI"))
                                {
                                    var myInterval = setInterval(function() {getAIMove()}, 2000);

                                    function getAIMove()
                                    {
                                         // GET -- AI Move
                                        var xhttp_get = new XMLHttpRequest();

                                        xhttp_get.onreadystatechange = function() {
                                            if (this.readyState == 4 && this.status == 200)
                                            {
                                                // if game ends -- if JSON.parse(this.responseText).end == "true" ??
                                                    // alert(JSON.parse(this.responseText).winner + " wins!");

                                                // else
                                                let new_gamestate = JSON.parse(this.responseText).gamestate;
                                                updateGameState(new_gamestate);
                                                if (checkIfValidMoves("human"))
                                                {
                                                    clearInterval(myInterval)
                                                }
                                            }
                                        };

                                        xhttp_get.open("GET", updateURL, true);
                                        xhttp_get.send();                                       
                                    }

                                    setTimeout(function() {

                                    }, 2000);
                                }
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

// loops through board and updates it to match a gamestring
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

// calls an API to check if a player can make any valid moves
function checkIfValidMoves(player)
{
    var checkURL = "http://group02.dhcp.nd.edu:8080/othello/check";
    var xhttp_get_check_move = new XMLHttpRequest();

    xhttp_get_check_move.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
        {
            return JSON.parse(this.responseText).result;
        }
    };

    if (player == "AI")
    {
        xhttp_get_check_move.open("POST", checkURL + "?player=AI", true);    
    }
    else
    {
        xhttp_get_check_move.open("POST", checkURL + "?player=human", true);
    }

    xhttp_get_check_move.send();
}
