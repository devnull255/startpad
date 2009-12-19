/*
	Web UI for the Enigma machine simulator.
	
	Copyright (c) 2009, Mike Koss - mckoss@startpad.org
*/
global_namespace.Define('startpad.enigma.sim', function (NS) {
	var Enigma = NS.Import('startpad.enigma');
	var machine = new Enigma.Enigma();
	var DOM = NS.Import('startpad.DOM');
	var Event = NS.Import('startpad.events');
	
Enigma.fnTrace = function(s) {console.log(s);}

NS.Extend(NS, {
Init: function()
	{
	NS.mParts = DOM.BindIDs();
	NS.mParts.plain.focus();
	
	var mState = machine.StateStrings();
	
	NS.mParts.init_rotors.value = mState.rotors;
	NS.mParts.init_position.value = mState.position;
	NS.mParts.init_rings.value = mState.rings;
	NS.mParts.init_plugs.value = mState.plugs;
	
	Event.AddEventFn(NS.mParts.plain, 'change', NS.UpdateDisplay);
	Event.AddEventFn(NS.mParts.plain, 'keydown', function(){});
	Event.AddEventFn(NS.mParts.plain, 'keyup', function(evt)
		{
		NS.UpdateDisplay();
		});
	
	NS.UpdateDisplay();
	},
	
UpdateDisplay: function()
	{
	var sPlain = NS.mParts.plain.value;
	machine.Init();
	var sCipher = machine.Encode(sPlain);
	DOM.SetText(NS.mParts.cipher, sCipher);
	
	for (var i = 1; i <= 3; i++)
		DOM.SetText(NS.mParts['rot_'+i], Enigma.ChFromI(machine.position[i-1]));
	}

});
});
