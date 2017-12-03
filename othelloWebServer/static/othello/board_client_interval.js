var updateURL = "http://group02.dhcp.nd.edu:8080/othello/update";

var validMoves = [[2, 3], [3,2], [4,5], [5,4]];
var timer = 500;

getGlobalStats();

function findWinner(gamestate) {
	let x = 0;
	let o = 0;
	for (let row=0; row<8; row++) {
		for (let col=0; col<8; col++) {
			if (gamestate[row][col] = 'X') x++;
			else o++;
		}
	}
	if (x>o) return "The AI";
	else return "You";
}

createBoard();
function createBoard()
{
    var gamestate = "";
    var table = document.createElement("table");
    for (let row = 0; row < 8; row++) {
        var tr = document.createElement("tr");
        for (let col = 0; col < 8; col++) {
            var td = document.createElement("td");
            td.id = row.toString() + ":" + col.toString();  // this is how to identify a cell --> row:column
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

                console.log(validMoves);

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
                    //alert("Invalid Move! Please pick a valid move.");
                }
                else
                {
                    // POST -- Player Move
                    var xhttp_post = new XMLHttpRequest();

                    xhttp_post.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200)
                        {
                            let response = JSON.parse(this.responseText);
                            let new_gamestate = response.gamestate;
                            updateGameState(new_gamestate);

                            if (response.end == "true")
                            {
                                //alert(JSON.parse(this.responseText).winner + " wins!")
				alert(findWinner(new_gamestate) + " wins!");
                            }

                            else
                            {
                                checkIfValidMoves("AI").then((result) => {

                                    if (result == true)
                                    {
                                        var myInterval = setInterval(function() {getAIMove()}, timer);

                                        function getAIMove()
                                        {
                                             // GET -- AI Move
                                            var xhttp_get = new XMLHttpRequest();

                                            xhttp_get.onreadystatechange = function() {
                                                if (this.readyState == 4 && this.status == 200)
                                                {
                                                    let response = JSON.parse(this.responseText);
                                                    
                                                    updateGameState(response.gamestate);

                                                    if (response.end == "true")
                                                    {
                                                        clearInterval(myInterval);
                                                        //alert(response.winner + " wins!")
							alert(findWinner(new_gamestate) + " wins!");
                                                    }
                                                    else
                                                    {
                                                        validMoves = response.validHumanMoves;
                                                        if(validMoves.length > 0) {
                                                            clearInterval(myInterval);
                                                        } else {
                                                            alert("You can't make a move.");
                                                        }
                                                    }
                                                }
                                            };

                                            xhttp_get.open("GET", updateURL, true);
                                            xhttp_get.send();
                                        }

                                        setTimeout(function() {

                                        }, timer);
                                    }
                                    else
                                    {
                                        alert("AI can't move!");
                                    }
                                });
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
    return new Promise((resolve, reject) => {
        
        url = "http://group02.dhcp.nd.edu:8080/othello/check";

        if(player == "AI") {
        	url += "?player=AI"
        } else {
        	url += "?player=human"
        }

        $.ajax({
			type: "GET",
			url: url,
			success: function(data){
			    resolve(data.result);
			}
		});
    });
}

function getGlobalStats() {
	$.ajax({
		type: "GET",
		url: "http://group02.dhcp.nd.edu:8080/othello/stats",
		success: function(data){
		    console.log(data);
		    $("#nGames").text(data["nGames"]);
		    $("#nEntries").text(data["nEntries"]);
		    $("#querySpeedIdx").text(String(data["querySpeedIdx"].toFixed(4)) + " sec");
		    $("#querySpeedNoIdx").text(String(data["querySpeedNoIdx"].toFixed(4)) + " sec");
		}
	});
}
