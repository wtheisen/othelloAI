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
var current_turn_num = 0;

// global vars for the graph
var humanScoreHistory = [2];
var AIScoreHistory = [2];
var pointsGraph, line, line2;
var gameScores, gameScoresGraph;

getGlobalStats();
initPointsGraph();
getUserInfo();
getUserStats();
createBoard();

// initializes the board and defines callback functions for each gamecell
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
                            refreshPointsGraph("human");
                            if (response.end == "true") {
				                displayWinner();
                                console.log(this.responseText);
                            } else {
                                validAIMoves = response.validAIMoves;
                                if(hasValidMoves("AI")) {
                                    // set up an interval that repeately gets an AI move every so often unless the human has a valid move
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
                                                refreshPointsGraph("AI");
                                                getMove = true;
                                                if (response.end == "true") {
						                            displayWinner();
                                                    console.log(this.responseText);
                                                    clearInterval(myInterval);
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
    $("#board").html(table);
}

// updates the visual state of the board based on a gamestring and whose turn it is
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

    current_turn_num++;
    updateTurnList(current_turn_num);
}

// makes a GET request to get the global stats, and updates page accordingly
function getGlobalStats() {
	$.ajax({
		type: "GET",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/stats",
		success: function(data){
		    console.log(data);
		    $("#nGames").text(data["nGames"]);
		    $("#nEntries").text(data["nEntries"]);
		    $("#querySpeedIdx").text(String(data["querySpeedIdx"].toFixed(4)) + " sec");
		    $("#querySpeedNoIdx").text(String(data["querySpeedNoIdx"].toFixed(4)) + " sec");
		}
	});
}

// checks if a player has valid moves
function hasValidMoves(player) {

    if(player == "human") {
        validMoves = validHumanMoves;
    } else {
        validMoves = validAIMoves;
    }

    return validMoves.length > 0;
}

// all the functionality to calculate and display the winner when the game is over
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

// record the game result via a post request
function postGameStats(winner) {
	$.ajax({
		type: "POST",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/winner",
		data: {
			token: winner,
			AIScore: aiScore,
			humanScore: humanScore
		},
		success: function(data){
			console.log(data);
		}
	});
}

// get the user info from the server and updates the page
function getUserInfo() {
      $.ajax({
        type: "GET",
        url: "http://group02.dhcp.nd.edu:" + location.port + "/othello/userinfo",
        success: function(data){
          console.log(data);
          if (data['result'] == 'success') {
            $("#username-p").text("Welcome, " + data["username"]);
            if (data["username"] == "Guest") {
              $("#logout-button").hide();
            }
          } else {
            $("username-p").text("failure");
            console.log(data);
          }
        }
      });
}

// gets user specific stats from the server and initializes the user scores graph
function getUserStats() {
	$.ajax({
		type: "GET",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/userstats",
		success: function(data){
			console.log(data);
			gameScores = data["gameScores"];
            if(gameScores.length < 2) {
                $("#gameScoresGraph").text("Once you have finished 2 games, you will see a chart of your score history here.");
            } else {
                initGameScoresGraph();
            }
		}
	});
}

$("#playAgain").click(function() {
	location.reload();
});

// toggles on and off the visual valid moves
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

// initializes the points graph using d3.js
function initPointsGraph() {

 	var m = [40, 80, 80, 80]; // margins
	var w = 500 - m[1] - m[3]; // width
	var h = 400 - m[0] - m[2]; // height

	// X scale will fit all values from data[] within pixels 0-w
	var x = d3.scale.linear().domain([0, 60]).range([0, w]);
	// Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
	var y = d3.scale.linear().domain([0, 64]).range([h, 0]);
	// automatically determining max range can work something like this
	// var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

	// create a line function that can convert data[] into x and y points
	line = d3.svg.line()
		.x(function(d,i) {
			return x(i);
		})
		.y(function(d) {
			return y(d);
		});


	// Add an SVG element with the desired dimensions and margin.
	pointsGraph = d3.select("#pointsGraph").append("svg:svg")
	      .attr("width", w + m[1] + m[3])
	      .attr("height", h + m[0] + m[2])
	      .append("svg:g")
	      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

	// create yAxis
	var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
	// Add the x-axis.
	pointsGraph.append("svg:g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + h + ")")
	      .call(xAxis);

	// create left yAxis
	var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
	// Add the y-axis to the left
	pointsGraph.append("svg:g")
	      .attr("class", "y axis")
	      .attr("transform", "translate(-25,0)")
	      .call(yAxisLeft);

	pointsGraph.append("text")
    .attr("x", w / 2 )
    .attr("y", -10)
    .style("text-anchor", "middle")
    .text("Points vs. Turn");

    //Create X axis label
    pointsGraph.append("text")
    .attr("x", w / 2 )
    .attr("y",  h + m[1] - 30)
    .style("text-anchor", "middle")
    .text("Turn");

    //Create Y axis label
    pointsGraph.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0- m[2])
    .attr("x",0 - (h / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Points");

}

// refreshes the points graphed based on game data
function refreshPointsGraph(player) {
	//if(player == "human") {
		humanScoreHistory.push(humanScore);
	//} else {
		AIScoreHistory.push(aiScore);
	//}
	d3.selectAll("path.line").remove(); // clear current lines
	pointsGraph.append("svg:path").attr("d", line(humanScoreHistory));
	pointsGraph.append("svg:path").attr("d", line(AIScoreHistory)).style("stroke", "red");
}

// init the game scores graph
function initGameScoresGraph() {

 	var m = [40, 80, 80, 80]; // margins
	var w = 500 - m[1] - m[3]; // width
	var h = 400 - m[0] - m[2]; // height

	// X scale will fit all values from data[] within pixels 0-w
	var x = d3.scale.linear().domain([0, gameScores.length-1]).range([0, w]);
	// Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
	var y = d3.scale.linear().domain([0, 64]).range([h, 0]);
	// automatically determining max range can work something like this
	// var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

	line2 = d3.svg.line()
		.x(function(d,i) {
			return x(i);
		})
		.y(function(d) {
			return y(d);
		});

	// Add an SVG element with the desired dimensions and margin.
	gameScoresGraph = d3.select("#gameScoresGraph").append("svg:svg")
	    .attr("width", w + m[1] + m[3])
	    .attr("height", h + m[0] + m[2])
	    .append("svg:g")
	    .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

	// create yAxis
	var xAxis = d3.svg.axis().scale(x).tickSubdivide(false).tickFormat(d3.format("d"));
	// Add the x-axis.
	gameScoresGraph.append("svg:g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + h + ")")
	      .call(xAxis);

	// create left yAxis
	var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
	// Add the y-axis to the left
	gameScoresGraph.append("svg:g")
    .attr("class", "y axis")
    .attr("transform", "translate(-25,0)")
    .call(yAxisLeft);

	gameScoresGraph.append("text")
    .attr("x", w / 2 )
    .attr("y", -10)
    .style("text-anchor", "middle")
    .text("User Score History");

    //Create X axis label
    gameScoresGraph.append("text")
    .attr("x", w / 2 )
    .attr("y",  h + m[1] - 30)
    .style("text-anchor", "middle")
    .text("Game");

    //Create Y axis label
    gameScoresGraph.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0- m[2])
    .attr("x",0 - (h / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Score");

    gameScoresGraph.append("svg:path").attr("d", line2(gameScores));
}

// update the turns list to implement the turn rollback
function updateTurnList(turnNum)
{
    let turnList = document.getElementById("turnList");

    let current_turn = document.createElement("li");
    let a = document.createElement("a");
    a.setAttribute("data-target", "#turn_" + turnNum.toString());
    a.setAttribute("data-toggle", "collapse");
    a.setAttribute("data-parent", "#turnList");
    a.innerHTML = "Turn " + turnNum.toString();

    let turn = document.createElement("ul");
    turn.setAttribute("id", "turn_" + turnNum.toString());
    turn.className = "nav nav-stacked collapse left-submenu";

    let div = document.createElement("div");
    div.setAttribute("id", "turnBoard_" + turnNum.toString());

    let myCurrentTable = document.getElementById("board");
    let myCloneTable = myCurrentTable.cloneNode(true);
    div.appendChild(myCloneTable);

    let li = document.createElement("li");

    let restoreBtn = document.createElement("button");
    restoreBtn.innerHTML = "Meow";

    li.appendChild(div);
    li.appendChild(restoreBtn);

    turn.appendChild(li);

    current_turn.appendChild(a);
    current_turn.appendChild(turn);

    turnList.appendChild(current_turn);
}
