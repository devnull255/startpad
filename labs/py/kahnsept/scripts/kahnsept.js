global_namespace.Define('kahnsept', function(K) {

/* kahnsept namespace

   Kahnsept is an object-oriented database, based on a extended prototype-based
   object heirarchy.  The basic objects in the system are called "Kahnsepts".
   Kahnsepts are related to each other via named "Konexions".

   Kahnsepts can inherit Konexions from their parent Kahnsepts (each Kansept, except
   for the Root Kahnsept has one (or more) parents).

   Namespace Variables and Functions:

   kRoot - the root of the Kahnsept database
   Init() - call once to initialize the Kahnsept database
   Get(id) - given a unique id, return the Kahnsept having that id.
   New(kParent, kwargs) - create a new con
*/

K.Extend(K, {
	idMax: 0,
	aKahnsepts: [],

// Create the World
Init: function()
	{
	// Careful bootstrapping to not require forward references to undefined properties
	// Note we pass in null (rather than undefined) to make a Root object
	K.kRoot = new K.Kahnsept(null);
	K.kBuiltin = new K.Kahnsept(K.kRoot);
	K.kString = new K.Kahnsept(K.kBuiltin);
	K.mBuiltinTypes = {'string': K.kString};
	K.kRoot.X("name", "Kahnsept");
	K.kBuiltin.X("name", "builtin");
	K.kString.X("name", "string");

	K.kNumber = new K.Kahnsept(K.kBuiltin, {name:"number"});
	K.kBoolean = new K.Kahnsept(K.kBuiltin, {name:"boolean"});
	K.kDate = new K.Kahnsept(K.kBuiltin, {name:"date"});
	K.kUndefined = new K.Kahnsept(K.kBuiltin, {name:"undefined"});

	K.mBuiltinTypes = {'number': K.kNumber, 'string': K.kString, 'boolean': K.kBoolean, 'undefined': K.kUndefined};
	K.aBuiltinClasses = [{fnConstructor: Date, k:K.kDate}];
	},
	
// Return a Kahnsept from it's id
Get: function(id)
	{
	return K.aKahnsepts[id];
	},
	
New: function(kParent, kwargs)
	{
	return new K.Kahnsept(kParent, kwargs);
	},
	
Kahnvert: function(obj)
	{
	if (typeof obj == 'object' && obj instanceof K.Kahnsept)
		return obj;
	
	// Convert builtin types to a Kahnsept's
	var kType = K.mBuiltinTypes[typeof obj];
	if (kType != undefined)
		{
		var k = K.New(kType);
		k._value = obj;
		return k;
		}
		
	if (typeof obj == 'object')
		{
		for (var i = 0; i < K.aBuiltinClasses.length; i++)
			{
			var m = K.aBuiltinClasses[i];
			if (obj instanceof m.fnConstructor)
				{
				var k = K.New(m.k);
				k._value = obj;
				return k;
				}
			}
		}
	
	throw new Error("Can't convert unknown object type to a Kahnsept (" + obj.toString + ")");
	},

// Copy the Kahnsept - but without any back-references	
Clone: function(k)
	{
	var kClone = new K.Kahnsept(k._parents);
	if (k.IsA(K.kBuiltin))
		{
		kClone._value = k._value;
		return;
		}

	for (var prop in this)
		{
		if (!this.hasOwnProperty(prop) || prop[0] == '_')
			continue;
		var v = this[prop];
		// Don't copy function objects
		if (typeof v != 'object')
			continue;
		kClone.X(v);
		}
	},
	
ToString: function(ak, chSep)
	{
	if (!(ak instanceof Array))
		{
		if (ak.IsA(K.kBuiltin))
			{
			if (ak._value === undefined)
				return ak.SName();
			return ak._value.toString();
			}
		return K.ToString(ak.GetX("name"));
		}

	if (chSep === undefined)
		chSep = ", ";
	var chSepT = "";
	var s = "";
	for (var i = 0; i < ak.length; i++)
		{
		s += chSepT + K.ToString(ak[i]);
		chSepT = chSep;
		}
	return s;
	},
	
X: function(sName, kSource, kDest)
	{
	kSource = K.Kahnvert(kSource);
	kDest = K.Kahnvert(kDest);
	
	if (kSource[sName] === undefined)
		kSource[sName] = [];
	if (kDest["~"+sName] === undefined)
		kDest["~"+sName] = [];
	if (!kSource[sName].Contains(kDest))
		{
		kSource[sName].push(kDest);
		kDest["~"+sName].push(kSource);
		}
	},
	
RemoveX: function(sName, kSource, kDest)
	{
	if (kSource[sName] === undefined)
		return;
		
	// Remove ALL values of Konexions with a given name
	if (kDest === undefined)
		{
		while (kSource[sName] !== undefined)
			this.RemoveX(sName, kSource, kSource[sName][0]);
		return;
		}
		
	// Remove a specific value of Konexion
	var i = kSource[sName].IFind(kDest);
	if (i == -1)
		return;
	kSource[sName].splice(i,1);
	if (kSource[sName].length == 0)
		delete kSource[sName];
	var i = kDest["~"+sName].IFind(kSource);
	kDest["~"+sName].splice(i,1);
	if (kDest["~"+sName].length == 0)
		delete kDest["~"+sName];
}
});

/* Kahnsept - Base object type

   Private members:
   _id - unique identifier
   _aParents - parent Kahnsepts (or empty for root object)
   _AddChild(k) - Add Kahnsept to list of children
   
   Public members:
   new Kahnsept(kParent, kwargs) - create a new Kahnsept based on a parent,
       and with optional Konexions
   name - (by convention) the user visible name for the Kahnsept
   X(s, k) - Add Konexion named s with value k
   IsA(k) - Return true if k is an (extended) parent of this
   GetX(s) - Return the Konexion named s
   GetXIs(s) - Return the conversion Konexion named s
   RemoveX(s, kValue) - Remove a (single or all) Konexions of a given name, s
   Dump() - Return string representation on Kahnsept - for debugging

   Methods:
   AddChild
*/

K.Kahnsept = function(kParent, kwargs)
{
	this._id = K.idMax++;
	K.aKahnsepts[this._id] = this;
	this._aParents = [];
	
	if (kParent == undefined)
		kParent = K.kRoot;
	
	this.AddParent(kParent);

	if (kwargs !== undefined)
		{
		for (var prop in kwargs)
			{
			if (!kwargs.hasOwnProperty(prop))
				continue;
			this.X(prop, kwargs[prop]);
			}
		}
};

K.Extend(K.Kahnsept.prototype, {
AddParent: function(kParent)
	{
	if (!kParent)
		return;

	if (kParent instanceof Array)
		{
		for (var i = 0; i < kParent.length; i++)
			this.AddParent(kParent[i]);
		return;
		}

	if (this._aParents.Contains(kParent))
		return;

	this._aParents.push(kParent);
	kParent._AddChild(this);
	},
	
SName: function()
	{
	return K.ToString(this.GetX("name"));
	},

_AddChild: function(kChild)
	{
	if (this._children == undefined)
		this._children = [];
	this._children.push(kChild);
	},

// Immediate children only	
GetChildren: function()
	{
	return this._children || [];
	},

// Set Konexion	
X: function(sName, kOther)
	{
	K.X(sName, this, kOther);
	},

// Return true iff kParent is one of this's parents	
IsA: function(kParent)
	{
	if (kParent == K.kRoot || kParent == this)
		return true;
	if (this == K.kRoot)
		return false;
	for (var i = 0; i < this._aParents.length; i++)
		{
		var kT = this._aParents[i];
		if (kT.IsA(kParent))
			return true;
		}
	return false;
	},

// Get array of all parents of the this	
Parents: function()
	{
	if (this == K.kRoot)
		return [];
	var ak = [K.kRoot];
	for (var i = 0; i < this._aParents.length; i++)
		{
		var kP = this._aParents[i];
		ak.PushUnique(kP);
		ak.ConcatUnique(kP.Parents());
		}
	return ak;
	},

// Get a Konexion, by name	
GetX: function(sName)
	{
	var x = this[sName];
	if (x != undefined)
		return x;
		
	// If Konexion is not stored locally, then merge the values of all
	// the parents that have this Konexion.
	x = [];
	for (var i = 0; i < this._aParents.length; i++)
		{
		x = x.concat(this._aParents[i].GetX(sName));
		}
	return x;
	},

// Get a "converse" connection - no inheritance!??	
GetXIs: function(sName)
	{
	var x= this["~"+sName];
	return x === undefined ? [] : x;
	},
	
RemoveX: function(sName, kDest)
	{
	K.RemoveX(sName, this, kDest);
	},

// Return an array of all available Konexion names
// (array of strings)
GetXNames: function()
	{
	var aNames = ["name"];
	
	for (var prop in this)
		{
		if (!this.hasOwnProperty(prop) || prop[0] == '_')
			continue;
		var v = this[prop];
		// Don't include function objects
		if (typeof v != 'object')
			continue;
		aNames.PushUnique(prop);
		}
	
	var aParents = this.Parents();
	for (var i = 0; i < aParents.length; i++)
		{
		aNames.ConcatUnique(aParents[i].GetXNames());
		}
	return aNames;
	},
	
IsOwn: function(sName, kValue)
	{
	if (this[sName] == undefined)
		return false;
	
	return this[sName].Contains(kValue);
	},

// Return a string representation of the Kahnsept (for debugging)	
Dump: function()
	{
	var s = this._id + ". " + '"' + this.name + '" (Parents: ';
	var chSep = "";
	for (var i = 0; i < this._aParents.length; i++)
		{
		s += chSep + this._aParents[i].name;
		chSep = ", ";
		}
	for (prop in this)
		{
		}
	s += ")";
	return s;
	}
});


});