require("http").createServer((req, res) => {
    res.end("Hello from server started by electron app!");
}).listen(9000);


