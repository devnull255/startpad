namespace.lookup('org.startpad.xray.chrome').defineOnce(function (ns) {

    var divPath = document.createElement('div');
    divPath.setAttribute('id', '_path');
    divPath.setAttribute('style', "height: 100px;border:1px solid red;");
    document.body.insertBefore(divPath, document.body.firstChild);

    function SourceLine(sf, node, level) {
        this.node = node;
        this.level = level;
        this.lineNumber = sf.sourceList.length;
        this.lineMatch = this.lineNumber;
        sf.sourceList.push(this);
        sf.nodeIndex[node] = this.lineNumber;
    }

    SourceLine.methods({
        endNode: function (sf) {
            if (sf.sourceList.length > this.lineNumber + 1) {
                var closeNode = new SourceLine(sf, null, this.level);
                closeNode.lineMatch = this.lineNumber;
                this.lineMatch = closeNode.lineNumber;
            }
        },

        format: function (sf) {
            var i;
            var s = "";

            for (i = 0; i < this.level; i++) {
                s += "&nbsp;&nbsp;";
            }

            s += '&lt;';
            if (this.lineMatch < this.lineNumber) {
                var sourceOpen = sf.sourceList[this.lineMatch];
                s += '/' + sourceOpen.node.tagName.toLowerCase();
            }
            else {
                s += this.node.tagName.toLowerCase();
                for (i = 0; i < this.node.attributes.length; i++) {
                    var attr = this.node.attributes[i];
                    s += ' ' + attr.name + '="' + attr.value + '"';
                }
            }
            s += '&gt;';
            return s;
        }
    });

    function SourceFile(rootNode) {
        this.rootNode = rootNode;
        this.sourceList = [];
        this.nodeIndex = {};

        this.walkDOM(rootNode, 0);
        document.addEventListener('mousemove',
                                  this.onMouseMove.fnMethod(this));
    }

    SourceFile.methods({
        walkDOM: function(node, level) {
            if (node.nodeType != 1) {
                return;
            }

            var source = new SourceLine(this, node, level);

            var children = node.children;
            for (var i = 0; i < children.length; i++) {
                this.walkDOM(children[i], level + 1);
            }

            source.endNode(this);
        },

        onMouseMove: function(evt) {
            var node = evt.target;
            console.log("mouse move", node.tagName);
            var line = this.nodeIndex[node];
            var minLine = Math.max(line - 2, 0);
            var maxLine = Math.min(minLine + 5, this.sourceList.length);

            var s = "";
            for (var dispLine = minLine; dispLine < maxLine; dispLine++) {
                var sT = this.sourceList[dispLine].format(this);
                if (dispLine == line) {
                    sT = '<b>' + sT + '</b>';
                }
                s += sT + '<br/>';
            }
            console.log(s);
            divPath.innerHTML = s;
        }
    });


    var sf = new SourceFile(document.body.parentElement, 0);
});