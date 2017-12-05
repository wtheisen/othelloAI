var updateURL = "http://group02.dhcp.nd.edu:" + location.port + "/othello/update";

var validHumanMoves = [[2, 3], [3,2], [4,5], [5,4]];
var validAIMoves = [];
var humanScore = 2;
var aiScore = 2;
var timer = 500;
var gamestate = "";
var myInterval;
var getMove = true;
var gameStatsPosted = false;

getGlobalStats();

function drawBoard(gamestate, turn)
{
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
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    $("#turn").html(table);

}

createBoard();

function createBoard() {
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

            if ((row == 3 && col == 3) || (row == 4 && col == 4)) {
                var circle = document.createElement("div");
                circle.className = "blackCircle";
                td.appendChild(circle);
                gamestate += "B";
            } else if ((row == 3 && col == 4) || (row == 4 && col == 3)) {
                var circle = document.createElement("div");
                circle.className = "whiteCircle";
                td.appendChild(circle);
                gamestate += "W";
            } else {
                gamestate += "G";
            }

            document.getElementById("hScore").innerHTML = humanScore;
            document.getElementById("aiScore").innerHTML = aiScore;

            td.onclick = function () {

                console.log(validHumanMoves);

                let isValid = false;
                validHumanMoves.forEach((move) => {
                    if (row == move[0] && col == move[1])
                    {
                        isValid = true;
                    }
                });

                if (isValid) { // POST -- Player Move
                    var xhttp_post = new XMLHttpRequest();

                    xhttp_post.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200)
                        {
                            let response = JSON.parse(this.responseText);
                            validHumanMoves = response.validHumanMoves;
                            updateGameState(response.gamestate, "human");
                            if (response.end == "true") {
				                displayWinner();
                            } else {
                                validAIMoves = response.validAIMoves;
                                if(hasValidMoves("AI")) { 
                                    myInterval = setInterval(function() {
                                    	if(getMove == true) {
                                    		getAIMove();
                                    	}
                                    }, timer);

                                    function getAIMove() {
                                    	getMove = false;
                                        var xhttp_get = new XMLHttpRequest();
                                        xhttp_get.onreadystatechange = function() {
                                            if (this.readyState == 4 && this.status == 200) {
                                                let response = JSON.parse(this.responseText);
                                                validHumanMoves = response.validHumanMoves;
                                                updateGameState(response.gamestate, "AI");
                                                getMove = true;
                                                if (response.end == "true") {
                                                    clearInterval(myInterval);
						                            displayWinner();
                                                } else {
                                                    if(validHumanMoves.length > 0) {
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
                                } else {
                                    alert("AI can't move!");
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
    // drawBoard("", 0);
    $("#board").html(table);
}
function updateGameState(gamestring, player)
{
    gamestate = gamestring;
    humanScore = 0;
    aiScore = 0;

    let row;
    let column; 
    for (let i = 0; i < gamestring.length; i++)
    {
        row = Math.floor(i/8);
        column = i%8;
        let gamechar = gamestring[i];
        let gamecell = document.getElementById(row.toString() + ":" + column.toString());
        let circle = document.createElement("div");

        if (row%2 == column%2) {
            gamecell.className = "seagreen";
        } else {
            gamecell.className = "green";
        }

        let checkbox = document.getElementById("myCheckbox");
        if (player == "AI" && checkbox.checked == true)
        {
            validHumanMoves.forEach((move) => {
                if (row == move[0] && column == move[1])
                {
                    gamecell.className = "paleturquoise";
                }
            });
        }

        if (gamechar == "O")
        {
            circle.className = "whiteCircle";
            humanScore++;

        }
        else if (gamechar == "X")
        {
            circle.className = "blackCircle";
            aiScore++;
        }
        if(gamecell.hasChildNodes()) {
            gamecell.removeChild(gamecell.lastChild);
        }
        gamecell.appendChild(circle);
    }

    document.getElementById("hScore").innerHTML = humanScore;
    document.getElementById("aiScore").innerHTML = aiScore;

}

function getGlobalStats() {
	$.ajax({
		type: "GET",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/stats",
		success: function(data){
		    //console.log(data);
		    $("#nGames").text(data["nGames"]);
		    $("#nEntries").text(data["nEntries"]);
		    $("#querySpeedIdx").text(String(data["querySpeedIdx"].toFixed(4)) + " sec");
		    $("#querySpeedNoIdx").text(String(data["querySpeedNoIdx"].toFixed(4)) + " sec");
		}
	});
}

function hasValidMoves(player) {

    if(player == "human") {
        validMoves = validHumanMoves;
    } else {
        validMoves = validAIMoves;
    }

    return validMoves.length > 0;
}

function displayWinner() {

    let x = 0;
    let o = 0;
    for(var i=0; i<gamestate.length; i++) {

        if(gamestate[i] == 'X') {
            x++;
        } else if(gamestate[i] == 'O') {
            o++;
        }
    }

    let winner;

    $(".alert").show();
    if (x>o)
    {
    	winner = "X";
        $("#winnerText").text("The AI has won!")
    }
    else if (o>x)
    {
    	winner = "O";
        $("#winnerText").text("The human has won!")
    }
    else
    {
        winner = "T";
        $("#winnerText").text("It's a tie!")   
    }
    if(!gameStatsPosted) {
    	postGameStats(winner);
    	gameStatsPosted = true;
    }
}

function postGameStats(winner) {
	$.ajax({
		type: "POST",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/winner",
		data: {token: winner},
		success: function(data){
			console.log(data);
		}
	});
}

$("#playAgain").click(function() {
	location.reload();
});

function toggleValidMoves(checkbox)
{
    for (let row = 0; row < 8; row++)
    {
        for (let col = 0; col < 8; col++)
        {
            let cell = document.getElementById(row.toString() + ":" + col.toString());

            if (checkbox.checked == true)
            {
                validHumanMoves.forEach((move) => {
                    if (row == move[0] && col == move[1])
                    {
                        cell.className = "paleturquoise";
                    }
                });
            }
            else
            {
                if (row%2 == col%2) {
                    cell.className = "seagreen";
                } else {
                    cell.className = "green";
                }
            }
        }
    }
}