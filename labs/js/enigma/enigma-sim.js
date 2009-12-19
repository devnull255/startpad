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
	aInitFields: ['rotors', 'position', 'rings', 'plugs'],

Init: function()
	{
	NS.mParts = DOM.BindIDs();
	NS.mParts.plain.focus();
	
	NS.mState = machine.StateStrings();
	
	DOM.InitValues(NS.aInitFields, NS.mParts, NS.mState);
	
	Event.AddEventFn(NS.mParts.plain, 'change', NS.UpdateDisplay);
	Event.AddEventFn(window, 'keydown', function(){});
	Event.AddEventFn(window, 'keyup', function(evt)
		{
		NS.UpdateDisplay();
		});
	
	NS.UpdateDisplay();
	},
	
UpdateDisplay: function()
	{
	var sPlain = NS.mParts.plain.value;
	
	DOM.ReadValues(NS.aInitFields, NS.mParts, NS.mState);

	machine.Init(Enigma.SettingsFromStrings(NS.mState));
	var sCipher = machine.Encode(sPlain);
	DOM.SetText(NS.mParts.cipher, sCipher);
	
	for (var i = 1; i <= 3; i++)
		DOM.SetText(NS.mParts['rot_'+i], Enigma.ChFromI(machine.position[i-1]));
	}

});
});
