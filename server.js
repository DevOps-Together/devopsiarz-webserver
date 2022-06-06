const http = require("http");
const url = require("url");

const host = 'localhost';
const port = 8000;

const requestListener = function (req, res) {

    console.log(`url : ${req.url}`);
    const url_parts = url.parse(req.url);

    // map request url to filesystem:
    if (url_parts.pathname === '/' || url_parts.pathname === '/index.html') {
        console.log('www root index');
    }

    res.writeHead(200);
    res.end(`url: ${JSON.stringify(url_parts)} `);
};

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
