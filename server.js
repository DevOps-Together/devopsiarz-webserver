const http = require("http");
const url = require("url");
const fs = require("fs");
const path = require("path");

const wwwRoot = __dirname + '/www';

const host = 'localhost';
const port = 8000;

const extList = ['txt', 'html'];

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
        const fPath = wwwRoot + urlParts.pathname;
        fs.readFile(fPath, 'UTF-8', (err, data) => {
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

                //display file if extension is supported:
                const extension = getExtension(fPath)
                if (extList.includes(extension)) {
                    const mimeType = getMimeType(extension);
                    res.writeHead(200, {'Content-Type': mimeType});
                    res.end(data);
                    return;
                }
                // else
                res.writeHead(200, {'Content-Type': 'text/plain'});
                res.end('not implemented yet');
            }
        )
    }
}

const getExtension = (filepath) => path.extname(filepath).replace('.', '').toLowerCase();

const getMimeType = function (extension) {
    if (extension === 'txt') return 'text/plain'
    if (extension === 'html') return 'text/html'
    // return sth
    return "text/plain"
}

const listFiles = (res, filepath) => {
    const buffer = fs.readFileSync(__dirname + '/templates/listing.html');
    let template = buffer.toString();
    let urlPath = filepath.replace(wwwRoot, '');
    fs.readdir(filepath, (err, files) => {
        //add link to parent dir if not www root
        let fileList = ''
        if (wwwRoot + '/' !== filepath) {
            fileList += `<li><a href="${path.dirname(urlPath)}">. .</a></li>`
        }

        files.forEach(file => {
            const ext = getExtension(file);
            fileList += extList.includes(ext) ? `<li><a href="${urlPath + file}">${file}</a></li>` : `<li>${file}</li>`
        });

        template = template.replace('[files]', fileList);
        template = template.replace(/\[path\]/g, urlPath);

        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end(template);
    });
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
