/**
 * Created with JetBrains PhpStorm.
 * User: justus
 * Date: 19.03.13
 * Time: 16:01
 * Yes, I'm fucking serious.
 */

function theLocator() {}

var TheLocator = new theLocator();

theLocator.prototype.getPath = function () {
    var path = document.location.hash.match(/([_A-z]+\.\d+(\.(pro|con|neut)\.\d+)?\/?)+/g);
    if (path == null || path.length == 0) {
        path = '/';
    } else {
        path = path[0];
    }
    return path;
}

theLocator.prototype.getPathParts = function () {
    var pathParts = this.getPath().split("/");
    return pathParts;
}