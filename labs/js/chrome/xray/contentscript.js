namespace.lookup('org.startpad.xray.chrome').defineOnce(function (ns) {
    var ELEMENT_NODE = 1;
    var TEXT_NODE = 3;

    var divPath = document.createElement('div');
    divPath.setAttribute('id', '_xray');
    divPath.setAttribute('style',
                         "position:absolute;top:0;left:0;" +
                         "transparency
                         "background:black;color:green;" +
                         "font-family:Courier;font-size:12px;" +
                         "margin:0;padding:0;");
    document.body.appendChild(divPath);

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
            this.line = this.line.substr(0, len - 4) + "/&gt;";
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

        dumpLines: function() {
            var s = "";
            for (var i = 0; i < this.sourceList.length; i++) {
                s += '<p id="_xray_' + i + '" ' +
                    'style="margin:0;padding:0;"' +
                    '>' + this.sourceList[i].line + '</p>';
            }
            return s;
        },

        onMouseMove: function(evt) {
            var node = evt.target;
            var lineNumber = this.nodeIndex[node];
            var textLine = document.getElementById("_xray_" + lineNumber);
            textLine.style.fontStyle = 'bold';
        }
    });


    var sf = new SourceFile(document.body.parentElement, 0);
    divPath.innerHTML = sf.dumpLines();
});