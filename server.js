const http = require("http");
const url = require("url");
const fs = require("fs");

const wwwRoot = __dirname + '/www/';
console.log(wwwRoot);

const host = 'localhost';
const port = 8000;

const requestListener = function (req, res) {

    console.log(`url : ${req.url}`);
    const url_parts = url.parse(req.url);

    // map request url to filesystem:
    if (url_parts.pathname === '/' || url_parts.pathname === '/index.html') {
        console.log('www root index');
        fs.readFile(wwwRoot + 'index.html', 'UTF-8', (err, data) => {
            if (err) {
                return error404(res);
            }
            res.writeHead(200);
            res.end(data);
        })
    }

    //  res.end(`url: ${JSON.stringify(url_parts)} `);
};

const error404 = (res) => {
    res.writeHead(404);
    res.end("File not found");
}

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
