namespace.lookup('org.startpad.xray.chrome').defineOnce(function (ns) {
    var ELEMENT_NODE = 1;
    var TEXT_NODE = 3;

    var divPath = document.createElement('div');
    divPath.setAttribute('id', '_path');
    divPath.setAttribute('style', "background:black;color:green;font-family:Courier");
    document.body.insertBefore(divPath, document.body.firstChild);

    function SourceLine(sf, node, level, fOpen) {
        if (fOpen) {
            this.line = this.format(node);
        }
        else {
            this.line = '&lt;/' + node.tagName.toLowerCase() + '&gt;';
        }
        this.level = level;
        this.lineNumber = sf.sourceList.length;
        sf.sourceList.push(this);
        sf.nodeIndex[node] = this.lineNumber;
    }

    SourceLine.methods({
        format: function (node) {
            var i;
            var s = "";

            if (node.nodeType == TEXT_NODE) {
                s = node.textContent.substr(0, 30);
                return s;
            }

            s += '&lt;';
            s += node.tagName.toLowerCase();
            for (i = 0; i < node.attributes.length; i++) {
                var attr = node.attributes[i];
                s += ' ' + attr.name + '="' + attr.value + '"';
            }
            s += '&gt;';
            return s;
        },

        closeTag: function (node) {
            var len = this.line.length;
            this.line = this.line.substr(0, len - 1) + "/&gt;";
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
            if (node.nodeType != ELEMENT_NODE &&
                node.nodeType != TEXT_NODE) {
                return;
            }

            var source = new SourceLine(this, node, level, true);
            var lines = this.sourceList.length;

            var children = node.children;
            for (var i = 0; i < children.length; i++) {
                this.walkDOM(children[i], level + 1);
            }

            // Closing tag needed
            // TODO: For small TEXT_NODE's put close on the same line
            if (lines != this.sourceList.length) {
                new SourceLine(this, node, level, false);
            }
            else {
                source.closeTag();
            }

        },

        onMouseMove: function(evt) {
            var node = evt.target;
            var lineNumber = this.nodeIndex[node];
            var minLine = Math.max(lineNumber - 2, 0);
            var maxLine = Math.min(minLine + 5, this.sourceList.length);

            var s = "";
            for (var dispLine = minLine; dispLine < maxLine; dispLine++) {
                var sT = this.sourceList[dispLine].line;
                if (dispLine == lineNumber) {
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