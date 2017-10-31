const http = require('http');
const url = require('url');
var qs = require('querystring');

startServer();

function startServer()
{
	http.createServer(function (req, res) {

		const pathname = url.parse(req.url).pathname;
		const query = url.parse(req.url).query;

		console.log(req.method + " : " + req.url);

		if (req.method == "POST")
		{
			let body = "";

			req.on("data", (data) => {
				body += data;
			});

			req.on("end", () => {
				let post = qs.parse(body);

				if (req.url == "/update")
				{
					let row_index = post.row - 1;
					let column_index = post.column - 1;
					let newGamestate = "";

					for (let i = 0; i < post.gamestate.length; i++)
					{
						if (i == ((8*row_index) + column_index))
						{
							newGamestate += "B";
						}
						else
						{
							newGamestate += post.gamestate[i];
						}
					}

					let new_info = {
						gamestate : newGamestate
					};

					console.log("Row: " + post.row + "\n" +
								"Column: " + post.column + "\n" +
								"Gamestate: " + newGamestate + "\n" +
								"Player: " + post.player);

					res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
					res.writeHead(200, {'Content-Type': 'text/plain'});
					res.write(JSON.stringify(new_info));
					res.end();
				}

			});
		}

		if (req.method == "GET")
		{
			if (req.url == "/")
			{
				res.write('<html>');
				res.write('GET Success!!!');
				res.end('</html>');
			}
		}

	}).listen(1337, '127.0.0.1');
}