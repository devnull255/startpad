/* Enigma.js

   Enigma machine simulation.
   
   Copyright (c) 2009, Mike Koss
   
   See Paper Enigma at:
   	http://mckoss.com/Crypto/Enigma.htm
   	
   Usage:
   
      var enigma = global_namespace.Import('startpad.enigma');
      var machine = new enigma.Enigma();
      var cipher = machine.Encode("plain text");
      machine.Init();
      var plain = machine.Encode(cipher);  -> "PLAIN TEXT"
   
   Rotor settings from:
   	http://homepages.tesco.net/~andycarlson/enigma/simulating_enigma.html
   
   TODO
   	- Ring Settings - notch moves relative to wires
   	- Plugboard
*/
global_namespace.Define('startpad.enigma', function (NS)
{
	var Base = NS.Import('startpad.base');

NS.Extend(NS, {
	mRotors: {
		I: {wires: "EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch: 'Q'},
		II: {wires: "AJDKSIRUXBLHWTMCQGZNPYFVOE", notch: 'E'},
		III: {wires: "BDFHJLCPRTXVZNYEIWGAKMUSQO", notch: 'V'},
		IV: {wires: "ESOVPZJAYQUIRHXLNFTGKDCMWB", notch: 'J'},
		V: {wires: "VZBRGITYUPSDNHLXAWMJQOFECK", notch: 'Z'}
		},

	mReflectors: {
	B: {wires: "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
	C: {wires: "FVPJIAOYEDRZXWGCTKUQSBNMHL"}
	},

	fnTrace: undefined,
	codeA: 'A'.charCodeAt(0),
	
MapRotor: function(rotor)
	{
	// Determine the relative offset (mod 26) of encoding and decoding each letter
	// (wire position)
	rotor.map = {};
	rotor.mapRev = {};
	for (var iFrom = 0; iFrom < 26; iFrom++)
		{
		var iTo = NS.IFromCh(rotor.wires.charAt(iFrom));
		rotor.map[iFrom] = (26 + iTo - iFrom) % 26;
		rotor.mapRev[iTo] = (26 + iFrom - iTo) % 26;
		}
	},
	
IFromCh: function(ch)
	{
	ch = ch.toUpperCase();
	return ch.charCodeAt(0) - NS.codeA;
	},

ChFromI: function(i)
	{
	return String.fromCharCode(i + NS.codeA);
	}
});

// Compute forward and reverse mappings for rotors and reflectors
for (var sRotor in NS.mRotors)
	NS.MapRotor(NS.mRotors[sRotor]);
	
for (var sReflector in NS.mReflectors)
	NS.MapRotor(NS.mReflectors[sReflector]);

NS.Enigma = function(settings)
{
	this.fnTrace = NS.fnTrace;
	this.settings = {
		rotors: ['I', 'II', 'III'],
		reflector: 'B',
		position: ['M', 'C', 'K'],
		rings: ['A', 'A', 'A'],
		plugs: ""
		};
	NS.Extend(this.settings, settings);
	this.Init();
};

NS.Extend(NS.Enigma.prototype, {
Init: function(settings)
	{
	NS.Extend(this.settings, settings);
	
	this.rotors = [];
	for (var i in this.settings.rotors)
			this.rotors[i] = NS.mRotors[this.settings.rotors[i]];

	this.reflector = NS.mReflectors[this.settings.reflector];

	// Position is for the position of the out Rings (i.e. the visible
	// marking on the code wheel.
	this.position = [];
	for (var i in this.settings.rotors)
		{
		this.position[i] = (NS.IFromCh(this.settings.position[i]));
		}
	
	this.rings = [];
	for (var i in this.settings.rings)
		{
		this.rings[i] = NS.IFromCh(this.settings.rings[i]);
		}
	
	this.settings.plugs = this.settings.plugs.toUpperCase();
	this.settings.plugs = this.settings.plugs.replace(/[^A-Z]/g, '');
	
	if (this.settings.plugs.length % 2 == 1)
		console.warn("Invalid plugboard settings - must have an even number of characters.");
	
	this.mPlugs = {};
	for (var i = 0; i < 26; i++)
		this.mPlugs[i] = i;

	for (var i = 0; i < this.settings.plugs.length; i += 2)
		{
		var iFrom = NS.IFromCh(this.settings.plugs[i]);
		var iTo = NS.IFromCh(this.settings.plugs[i+1]);
	
		if (this.mPlugs[iFrom] != iFrom)
			console.warn("Redefinition of plug setting for " + NS.ChFromI(iFrom));
		if (this.mPlugs[iTo] != iTo)
			console.warn("Redefinition of plug setting for " + NS.ChFromI(iTo));
			
		this.mPlugs[iFrom] = iTo;
		this.mPlugs[iTo] = iFrom;
		}
	
	if (this.fnTrace)
		this.fnTrace("Init: " + this.toString())
	},

/* Return machine state	as a string
 * 
 * Format: "Enigma Rotors: I-II-III Position: ABC <Rings:AAA> <Plugboard: AB CD>"
 * 
 * Rings settings of AAA not displayed.
 * Null plugboard not displayed.
 */
toString: function()
	{
	var s = "";
	var mState = this.StateStrings();
	
	s += "Enigma Rotors: " + mState.rotors;
	s += " Position: " + mState.position;

	if (mState.rings != "AAA")
		s += " Rings: " + mState.rings;

	if (mState.plugs != "")
		s += " Plugboard: " + mState.plugs;

	return s;
	},
	
StateStrings: function()
	{
	var mState = {};

	mState.rotors = this.settings.rotors.join('-');
	mState.position = Base.Map(this.position, NS.ChFromI).join('')
	mState.rings = Base.Map(this.rings, NS.ChFromI).join('')
	
	mState.plugs = "";
	var chSep = "";
	for (var i = 0; i < 26; i++)
		{
		if (i < this.mPlugs[i])
			{
			mState.plugs += chSep + NS.ChFromI(i) + NS.ChFromI(this.mPlugs[i]);
			chSep = " ";
			}
		}

	return mState;
	},
	
PositionString: function()
	{
	var s = "";
	for (var i in this.position)
		s += NS.ChFromI(this.position[i]);
	return s;
	},
	
IncrementRotors: function()
	{
	/* Note that notches are components of the outer rings.  So wheel
	 * motion is tied to the visible rotor position (letter or number)
	 * NOT the wiring position - which is dictated by the rings settings
	 * (or offset from the 'A' position).
	 */
	
	// Middle notch - all rotors rotate
	if (this.position[1] == NS.IFromCh(this.rotors[1].notch))
		{
		this.position[0] += 1;
		this.position[1] += 1;
		}
	// Right notch - right two rotors rotate
	else if (this.position[2] == NS.IFromCh(this.rotors[2].notch))
		this.position[1] += 1;
		
	this.position[2] += 1;
	
	for (var i in this.rotors)
		this.position[i] = this.position[i] % 26; 
	},
	
EncodeCh: function(ch)
	{
	var aTrace = [];
	var i;
	
	ch = ch.toUpperCase();
	
	// Short circuit non alphabetics
	if (ch < 'A' || ch > 'Z')
		return ch;
		
	this.IncrementRotors();
	
	i = NS.IFromCh(ch);
	aTrace.push(i);
	i = this.mPlugs[i];
	aTrace.push(i);

	for (var r = 2; r >= 0; r--)
		{
		var d = this.rotors[r].map[(26 + i + this.position[r] - this.rings[r]) % 26];
		i = (i + d) % 26;
		aTrace.push(i);
		}
		
	i = (i + this.reflector.map[i]) % 26;
	aTrace.push(i);
	
	for (var r = 0; r < 3; r++)
		{
		var d = this.rotors[r].mapRev[(26 + i + this.position[r] - this.rings[r]) % 26];
		i = (i + d) % 26;
		aTrace.push(i);
		}
		
	i = this.mPlugs[i];
	aTrace.push(i);

	var chOut = NS.ChFromI(i);
	
	if (this.fnTrace)
		{
		var s = "";
		var chSep = "";
		for (var i in aTrace)
			{
			s += chSep + NS.ChFromI(aTrace[i]);
			chSep = "->";
			}
		this.fnTrace(s + " " + this.toString());
		}

	return chOut;
	},
	
Encode: function(s)
	{
	var sOut = "";
	for (var i = 0; i < s.length; i++)
		sOut += this.EncodeCh(s[i]);
	return sOut;
	}
});

}); // startpad.enigma