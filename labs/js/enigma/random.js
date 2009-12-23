global_namespace.Define('startpad.random.', function(NS) {
/* Random number functions.

   The builtin Math.random does not afford setting an initial seed.  These
   functions provide an alternative random number generation system - and mirror
   the subset of functions builtin to Python (random.py).
   
   Usage:
   
    Random = NS.Import('startpad.random');
    
   	Random.seed([]) - intialize the random generator for a string, number, array, or date (uses current
   		Date() if none is given.
   	Random.randint(min, max) - return a uniform random integer between min and max - inclusive
   	Random.random() - return a random floating point number between 0 and 1 inclusive
   
   2009-12-22 [mck] Created.
*/
	MT = NS.Import('startpad.random.mt');
	Base = NS.Import('startpad.base');
	
NS.Extend(NS, {
seed: function(data)
	{
	if (data == undefined)
		data = new Date();
		
	if (typeof data == 'number')
		data = [data];
		
	if (typeof data == 'string')
		data = Base.map(data.split(''), String.codeFromChar);
	},
	
randint: function(min, max)
	{
	},
	
random: function()
	{
	}
});

// Intiialize the random generatr by the current date, if the user doesn't seed it
NS.seed();

});