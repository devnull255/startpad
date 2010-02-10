global_namespace.Define('startpad.base', function(NS) {

NS.Extend(NS, {
Browser:
	{
	version: parseInt(window.navigator.appVersion),
	fIE: window.navigator.appName.indexOf("Microsoft") !== -1
	},

// Javascript Enumeration
// Build an object whose properties are mapped to successive integers
// Also allow setting specific values by passing integers instead of strings.
// e.g. new NS.Enum("a", "b", "c", 5, "d") -> {a:0, b:1, c:2, d:5}
Enum: function(aEnum)
	{
	if (!aEnum)
		return;

	var j = 0;
	for (var i = 0; i < aEnum.length; i++)
		{
		if (typeof aEnum[i] == "string")
			this[aEnum[i]] = j++;
		else
			j = aEnum[i];
		}
	}

});

//--------------------------------------------------------------------------
// Fast string concatenation buffer
//--------------------------------------------------------------------------
NS.StBuf = function()
{
	this.rgst = [];
	this.Append.apply(this, arguments);
	this.sListSep = ", ";
};

NS.StBuf.prototype = {
		constructor: NS.StBuf,

Append: function()
	{
	for (var ist = 0; ist < arguments.length; ist++)
		this.rgst.push(arguments[ist].toString());
	return this;
	},
	
Clear: function ()
	{
	this.rgst = [];
	},

toString: function()
	{
	return this.rgst.join("");
	},

// Build a comma separated list - ignoring undefined, null, empty strings
AppendList: function()
	{
	var sSep = "";
	for (var ist = 0; ist < arguments.length; ist++)
		{
		var sT = arguments[ist];
		if (sT)
			{
			this.Append(sSep + sT);
			sSep = this.sListSep;
			}
		}
	return this;
	}
}; // NS.StBuf

//--------------------------------------------------------------------------
// Some extensions to built-in JavaScript objects (sorry!)
//--------------------------------------------------------------------------

// Wrap a method call in a function
NS.Extend(Function.prototype, {
FnMethod: function(obj)
	{
	var _fn = this;
	return function () { return _fn.apply(obj, arguments); };
	},

// Append additional arguments to a function
FnArgs: function()
	{
	var _fn = this;
	var _args = [];
	for (var i = 0; i < arguments.length; i++)
		{
		_args.push(arguments[i]);
		}

	return function ()
		{
		var args = [];
		// In case this is a method call, preserve the "this" variable
		var self = this;

		// "Natural" arguments come first
		for (i = 0; i < arguments.length; i++)
			{
			args.push(arguments[i]);
			}
		
		// Addtional arguments appended
		for (i = 0; i < _args.length; i++)
			{
			args.push(_args[i]);
			}

		return _fn.apply(self, args);
		};	
	}
}); // Function extensions

NS.Extend(Array.prototype, {
Contains: function(obj)
	{
	return this.IFind(obj) != -1;
	},

IFind: function(obj)
	{
	for (var i = 0; i < this.length; i++)
		if (obj === this[i])
			return i;
	return -1;
	},

PushUnique: function()
	{
	for (var i = 0; i < arguments.length; i++)
		{
		var elt = arguments[i];
		if (!this.Contains(elt))
			this.push(elt);
		}
	},
	
ConcatUnique: function(a)
	{
	for (var i = 0; i < a.length; i++)
		this.PushUnique(a[i]);
	}
}); // Array extensions

}); // startpad.base