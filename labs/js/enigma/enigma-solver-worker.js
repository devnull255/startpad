importScripts('namespace.js', 'base.js', 'enigma.js');
global_namespace.Define('startpad.enigma.solver.worker', function(NS)
{
	postMessage("this is a test");
	
	onmessage = function(event)
		{
		postMessage("from worker - " + event.data);
		};
});

