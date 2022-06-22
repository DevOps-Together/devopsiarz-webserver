const http = require("http");
const url = require("url");
const fs = require("fs");

const wwwRoot = __dirname + '/www';
console.log(wwwRoot);

const host = 'localhost';
const port = 8000;

const requestListener = function (req, res) {

    console.log(`url : ${req.url}`);
    const urlParts = url.parse(req.url);

    // map request url to filesystem:
    const indexRegex = /(.*?\/$)|(.*?\/index.html$)/g;
    if (urlParts.pathname.match(indexRegex)) {
        console.log(`index page for ${urlParts.pathname}`);
        const filepath = urlParts.pathname.endsWith('index.html') ? urlParts.pathname : urlParts.pathname + 'index.html'

        // some security check
        if (filepath.includes('../')) {
            console.log("hacker detected");
            return error404(res);
        }

        fs.readFile(wwwRoot + filepath, 'UTF-8', (err, data) => {
            if (err) {
                console.log(err);
                if (err.errno === -2) {
                    let fsPath = err.path
                    console.log(`resolved filepath (not found): ${fsPath}`)
                    // file index.html not found. Check if directory exists and list files instead
                    fsPath = fsPath.substring(0, fsPath.length - 10);  // index.html => 10 chars
                    fs.lstat(fsPath, (err, stats) => {
                        if (err) {
                            if (err.errno !== -2) console.log(err);
                            return error404(res);
                        }
                        // at this point it has to be directory (or link?)
                        if (!stats.isDirectory()) {
                            return error404(res);
                        }
                    });
                    return listFiles(res, filepath);
                }
                // else just return 404
                return error404(res);
            }
            // display index.html file
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.end(data);
        })
    } else {
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end('not implemented yet');
    }

    //  res.end(`url: ${JSON.stringify(urlParts)} `);
};

const listFiles = (res, filepath) => {
    res.writeHead(200);
    res.end(`list file in folder ${filepath}`);
}

const error404 = (res) => {
    res.writeHead(404);
    res.end("File not found");
}

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
