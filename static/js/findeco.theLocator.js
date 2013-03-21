/**
 * Created with JetBrains PhpStorm.
 * User: justus
 * Date: 19.03.13
 * Time: 16:01
 * Yes, I'm fucking serious.
 */

function theLocator() {
}

var TheLocator = new theLocator();

theLocator.prototype.getPath = function () {
    // We're going to hell for this. Sorry folks.
    var path = (document.location.hash + '/').match(/([_A-z]+\.\d+(\.(pro|con|neut)\.\d+)?\/)+/g);
    if (path == null || path.length == 0) {
        path = '/';
    } else {
        path = path[0];
    }
    return path;
}

function isNonEmpty(element, index, array) {
    return (element != "");
}

theLocator.prototype.getPathParts = function () {
    var path = this.getPath();
    var pathParts = this.getPath().split("/").filter(isNonEmpty);
    return pathParts;
};

theLocator.prototype.getSanitizedPath = function (target) {

    if (target == undefined) {
        target = '';
    } else {
        target = target.replace(/\//g, '');
    }

    var parts = this.getPathParts();
    var tmp = [];
    for (p in parts) {
        if (parts[p] == "") {
            continue;
        }
        tmp.push(parts[p]);
    }

    var sanePath = this.saneSlashAppending(tmp.join('/')) + target;
    if (sanePath != '/') {
        sanePath = this.removeTrailingSlashes(sanePath);
    }
    return sanePath;
};

theLocator.prototype.getSanitizedArgumentFreePath = function () {
    var tmp = this.getSanitizedPath();
    if ( !this.isArgumentPath(tmp) ) {
        return tmp;
    }
    tmp = tmp.replace(/\.(pro|con|neut)\.\d+$/,'');
    return tmp;
}

theLocator.prototype.removeTrailingSlashes = function (string) {
    if (string.substr(string.length-1) == '/') {
        string = string.substr(0, string.length - 1);
    }
    return string;
};

theLocator.prototype.isArgumentPath = function (path) {
    var pP;
    if ( path == undefined ) {
        pP = this.getSanitizedPath().split(".");
    } else {
        pP = path.split(".");
    }
    var shortTitle = pP[pP.length - 2];
    if ( shortTitle == "pro"
        || shortTitle == "neut"
        || shortTitle == "con" ) {
        return true;
    }
    return false;
}

theLocator.prototype.saneSlashAppending = function (string) {
    if (string.substr(string.length-1) != '/') {
        string += '/';
    }
    return string;
};
