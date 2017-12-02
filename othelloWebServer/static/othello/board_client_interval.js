var updateURL = "http://group02.dhcp.nd.edu:8080/othello/update";

var validMoves = [[2, 3], [3,2], [4,5], [5,4]];

createBoard();
function createBoard()
{
    var gamestate = "";
    var table = document.createElement("table");
    for (let row = 0; row < 8; row++) {
        var tr = document.createElement("tr");
        for (let col = 0; col < 8; col++) {
            var td = document.createElement("td");
            td.id = row.toString() + ":" + row.toString();  // this is how to identify a cell --> row:column
            // assign white and black
            if (row%2 == col%2) {
                td.className = "seagreen";
            } else {
                td.className = "green";
            }
            if ((row == 3 && col == 3) || (row == 4 && col == 4))
            {
                var circle = document.createElement("div");
                circle.className = "blackCircle";
                td.appendChild(circle);
                gamestate += "B";
            }
            else if ((row == 3 && col == 4) || (row == 4 && col == 3))
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

                // check if row/column is invalid move -- iterate over list ??

                let isValid = false;
                validMoves.forEach((move) => {
                    if (row == move[0] && col == move[1])
                    {
                        isValid = true;
                    }
                });

                if (!isValid)
                {
                    alert("Invalid Move! Please pick a valid move.");
                }
                else
                {
                    // POST -- Player Move
                    var xhttp_post = new XMLHttpRequest();

                    xhttp_post.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200)
                        {
                            let new_gamestate = JSON.parse(this.responseText).gamestate;
                            updateGameState(new_gamestate);

                            if (response.end == "true")
                            {
                                alert(JSON.parse(this.responseText).winner + " wins!")
                            }

                            else
                            {
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
                                                let response = JSON.parse(this.responseText);

                                                if (response.end == "true")
                                                {
                                                    alert(JSON.parse(this.responseText).winner + " wins!")
                                                }
                                                else
                                                {
                                                    let new_gamestate = JSON.parse(this.responseText).gamestate;
                                                    updateGameState(new_gamestate);
                                                    if (checkIfValidMoves("human"))
                                                    {
                                                        clearInterval(myInterval)
                                                    }
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
                        }
                    };

                    var formData = new FormData();
                    formData.append("row", row);
                    formData.append("column", col);
                    xhttp_post.open("POST", updateURL, true);
                    xhttp_post.send(formData);
                }
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
