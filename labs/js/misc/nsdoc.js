/*
 Create documentation from a JavaScript namespace.
 */
 namespace.lookup('org.startpad.nsdoc').defineOnce(function(ns)
{
    var base = namespace.lookup('org.startpad.base');
    
    function namespaceMarkdown(ns) {
        var s = new base.StBuf();
        
        for (var name in ns) {
            if (ns.hasOwnProperty(name)) {
                var func = ns[name];
                if (typeof func != 'function') {
                    continue;
                }
                
                s.append(functionMarkdown(name, func));
            }
        }
        return s.toString();
    }
    
    function functionMarkdown(name, func) {
        var s = new base.StBuf();
        
        s.append(name + '\n' + '---\n')
        
        for (var methodName in func.prototype) {
            if (typeof func.prototype[methodName] == 'function') {
                method = func.prototype[methodName];
                s.append('*' + methodName + '*\n');
            }
            
        }
        return s.toString();
    }
    
    ns.extend({
        'namespaceMarkdown': namespaceMarkdown,
        'functionMarkdown': functionMarkdown
    });
    
});