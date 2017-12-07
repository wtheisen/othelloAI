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

// global vars for the graph
var humanScoreHistory = [2];
var AIScoreHistory = [2];
var graph, line;

getGlobalStats();

initGraph();

getUserInfo();	

getUserStats();

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
                            refreshGraph("human");
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
                                                refreshGraph("AI");
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
		    console.log(data);
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

function getUserInfo() {
	$.ajax({
		type: "GET",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/getuser",
		success: function(data){
			console.log(data);
		}
	});
}

function getUserStats() {
	$.ajax({
		type: "GET",
		url: "http://group02.dhcp.nd.edu:"  + location.port +  "/othello/userstats",
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

function initGraph() {

 	var m = [40, 80, 80, 80]; // margins
	var w = 500 - m[1] - m[3]; // width
	var h = 400 - m[0] - m[2]; // height

	// X scale will fit all values from data[] within pixels 0-w
	var x = d3.scale.linear().domain([0, 31]).range([0, w]);
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
	graph = d3.select("#graph").append("svg:svg")
	      .attr("width", w + m[1] + m[3])
	      .attr("height", h + m[0] + m[2])
	      .append("svg:g")
	      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

	// create yAxis
	var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
	// Add the x-axis.
	graph.append("svg:g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + h + ")")
	      .call(xAxis);

	// create left yAxis
	var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
	// Add the y-axis to the left
	graph.append("svg:g")
	      .attr("class", "y axis")
	      .attr("transform", "translate(-25,0)")
	      .call(yAxisLeft);	

	graph.append("text")
    .attr("x", w / 2 )
    .attr("y", -10)
    .style("text-anchor", "middle")
    .text("Points vs. Turn");

    //Create X axis label   
    graph.append("text")
    .attr("x", w / 2 )
    .attr("y",  h + m[1] - 30)
    .style("text-anchor", "middle")
    .text("Turn");

    //Create Y axis label
    graph.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0- m[2])
    .attr("x",0 - (h / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Points"); 

}

function refreshGraph(player) {
	if(player == "human") {
		humanScoreHistory.push(humanScore);
	} else {
		AIScoreHistory.push(aiScore);
	}
	d3.selectAll("path.line").remove(); // clear current lines
	graph.append("svg:path").attr("d", line(humanScoreHistory)).attr("data-legend",function(d) { return "test"});
	graph.append("svg:path").attr("d", line(AIScoreHistory)).style("stroke", "red").attr("data-legend",function(d) { return "test2"});
}