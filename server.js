const http = require("http");
const url = require("url");
const fs = require("fs");

const wwwRoot = __dirname + '/www';

const host = 'localhost';
const port = 8000;

const requestListener = function (req, res) {

    console.log(`url : ${req.url}`);
    const urlParts = url.parse(req.url);

    // some security check
    if (urlParts.pathname.includes('../')) {
        console.log("hacker detected");
        return error404(res);
    }

    // map request url to filesystem:
    const indexRegex = /(.*?\/$)|(.*?\/index.html$)/g;
    if (urlParts.pathname.match(indexRegex)) {
        console.log(`index page for ${urlParts.pathname}`);
        const filepath = urlParts.pathname.endsWith('index.html') ? urlParts.pathname : urlParts.pathname + 'index.html'

        fs.readFile(wwwRoot + filepath, 'UTF-8', (err, data) => {
            if (err) {
                if (err.errno === -2) {
                    let fsPath = err.path
                    console.log(`resolved filepath (not found): ${fsPath}`)
                    // file index.html not found. Check if directory exists and list files instead
                    fsPath = fsPath.substring(0, fsPath.length - 10);  // index.html => 10 chars
                    console.log(fsPath);
                    fs.stat(fsPath, (err, stats) => {
                        if (err) {
                            if (err.errno !== -2) console.log(err);
                            return error404(res);
                        }
                        // at this point it has to be directory (or link?)
                        if (!stats.isDirectory()) {
                            return error404(res);
                        }
                    });
                    return listFiles(res, fsPath);
                }
                // else just return 404
                return error404(res);
            }
            // display index.html file
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.end(data);
        })
    } else {
        // as it's not an index page then it could be folder w/o slash or regular file
        fs.readFile(wwwRoot + urlParts.pathname, 'UTF-8', (err, data) => {
                if (err) {
                    // err read from directory
                    if (err.errno === -21) {
                        res.writeHead(301, {
                            'Location': req.url + '/'
                        });
                        res.end();
                        return;
                    }

                    // err no file (or directory but dir is already resolved)
                    if (err.errno === -2) {
                        return error404(res);
                    }

                    // well at this point lets throw 500 ;)
                    return error500(res);
                }
                res.writeHead(200, {'Content-Type': 'text/plain'});
                res.end('not implemented yet');
            }
        )
    }
}


const listFiles = (res, filepath) => {
    res.writeHead(200);
    res.end(`list file in folder ${filepath}`);
}

const error404 = (res) => {
    return _error(res, 404, "File not found");
}

const error500 = (res) => {
    return _error(res, 500, "Internal Server Error");
}

const _error = (res, code, msg) => {
    res.writeHead(code);
    res.end(msg);
}

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
