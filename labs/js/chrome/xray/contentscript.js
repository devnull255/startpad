var divPath = document.createElement('div');
divPath.setAttribute('id', '_path');
divPath.setAttribute('style', "height: 100px;border:1px solid red;");
document.body.insertBefore(divPath, document.body.firstChild);

var nodeList = [];
var nodeMap = {};

function walkDOM(node, level) {
    if (node.nodeType != 1)
        return;

    nodeList.push({node: node, level: level});
    nodeMap[node] = nodeList.length - 1;

    var children = node.children;
    for (var i = 0; i < children.length; i++) {
        walkDOM(children[i], level + 1);
    }
}

function domPath(elem) {
    s = "";
    while (elem) {
        s = elem.tagName + " - " + s;
        elem = elem.parentElement;
    }
    return s;
}

function onMouseMove(evt) {
    var node = evt.target;
    var line = nodeMap[node];
    var minLine = Math.max(line - 3, 0);
    var maxLine = Math.min(minLine + 5, nodeList.length);

    var s = "";
    for (var dispLine = minLine; dispLine < maxLine; dispLine++) {
        if (dispLine == line) {
            s += '<b>';
        }
        s += formatLine(nodeList[dispLine].node, nodeList[dispLine].level) + '<br\>';
        if (dispLine == line) {
            s += '</b>';
        }
    }

    divPath.innerHTML = s;
}

function formatLine(node, level) {
    var s = "";

    for (var i = 0; i < level; i++) {
        s += "&nbsp;&nbsp;";
    }

    s += node.tagName;
    return s;
}

walkDOM(document.body.parentElement, 0);

document.addEventListener('mousemove', onMouseMove);
