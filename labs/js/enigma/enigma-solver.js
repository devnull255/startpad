global_namespace.Define('startpad.enigma.solver', function (NS)
{
	Enigma = NS.Import('startpad.enigma');
	
NS.Extend(NS, {
Init: function()
	{
		NS.worker = new Worker('enigma-solver-worker.js');
		NS.worker.onmessage = NS.OnMessage;
		NS.worker.onerror = NS.OnError;
	},

Solve: function()
	{
	},
	
OnMessage: function(event)
	{
	alert(event.data);
	},
	
OnError: function(event)
	{
	alert("Worker error - " + event.message + " (" + event.filename + ": line #" + event.lineno + ")");
	}
});
});
