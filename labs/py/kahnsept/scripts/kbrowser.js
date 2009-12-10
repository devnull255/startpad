global_namespace.Define('kahnsept.browser', function(NS) {
	var K = NS.Import("kahnsept");
	var DOM = NS.Import("startpad.DOM");
	var Event = NS.Import('startpad.events');
	
NS.aBrowsers = [];

NS.Browser = function(parts)
{
	this.parts = parts;
	NS.aBrowsers.push(this);
	this.iBrowser = NS.aBrowsers.length-1;
	this.mode = 'read';
	
	Event.AddEventFn(this.parts['save'], 'click', this.Save.FnMethod(this));
};

NS.Extend(NS.Browser.prototype, {

SGlobalName: function(s)
	{
	return NS.SGlobalName("aBrowsers[" + this.iBrowser + "]." + s);
	},

Navigate: function(k)
	{
	if (k != undefined)
		this.k = k;
	
	var btn = this.parts['toggle-mode'];
	switch (this.mode)
		{
	case 'read':
		btn.value = "Edit";
		Event.AddEventFn(btn, 'click', this.EditMode.FnMethod(this));
		this.parts['save'].style.visibility = 'hidden';
		break;
	case 'write':
		btn.value = "Cancel";
		Event.AddEventFn(btn, 'click', this.ReadOnlyMode.FnMethod(this));
		this.parts['save'].style.visibility = 'visible';
		break;
		}


	DOM.SetText(this.parts['name'], this.k._id + ". " + this.k.SName());
	
	DOM.EmptyNode(this.parts['parents']);
	this.parts['parents'].appendChild(this.LinkK("_parents", this.k.Parents()));
	
	DOM.EmptyNode(this.parts['konexions']);
	var tbl = document.createElement('table');
	var aNames = this.k.GetXNames();
	for (var i = 0; i < aNames.length; i++)
		{
		var sName = aNames[i];
		var tr = document.createElement('tr');
		var thName = document.createElement('th');
		DOM.SetText(thName, aNames[i]);
		var tdValue = document.createElement('td');
		tdValue.appendChild(this.LinkK(sName, this.k.GetX(aNames[i])));
		tr.appendChild(thName);
		tr.appendChild(tdValue);
		tbl.appendChild(tr);
		}
	this.parts['konexions'].appendChild(tbl);
	
	DOM.EmptyNode(this.parts['children']);
	var btn = document.createElement('input');
	btn.type = "button";
	btn.value = "New Child";
	btn.setAttribute("onclick", this.SGlobalName("MakeChild") + '(' + this.k._id + ');');
	this.parts['children'].appendChild(btn);
	
	var aChildren = this.k.GetChildren();
	for (var i = 0; i < aChildren.length; i++)
		{
		var k = aChildren[i];
		var div = document.createElement('div');
		var link = this.LinkK("_children", k);
		div.appendChild(link);
		this.parts['children'].appendChild(div);
		}
	},
	
EditMode: function()
	{
	this.mode = 'write';
	this.mControls = {};
	this.Navigate();
	},

ReadOnlyMode: function()
	{
	this.mode = 'read';
	this.mControls = undefined;
	this.Navigate();
	},
	
Save: function()
	{
	for (var id in this.mControls)
		{
		if (!this.mControls.hasOwnProperty(id))
			continue;

		var k = K.Get(id);		
		var mControl = this.mControls[id];

		var sOld = K.ToString(k);
		var sNew = mControl.inp.value;
		
		// Don't do anything if no edits were made
		if (sOld != sNew)
			{
			// If this property is not "local" - then copy it for the change
			if (!mControl.fOwn)
				{
				this.k.RemoveX(mControl.sName, k);
				var kT = K.Clone(k);
				this.k.X(mControl.sName, kT);
				}
			
			// Set the value in the old or new Kahnsept
			if (k.IsA(K.kNumber))
				{
				var nNew = parseInt(sNew);
				if (typeof nNew == 'number')
					k._value = nNew;
				}
			else if (k.IsA(K.kString))
				{
				k._value = sNew;
				}
			}
		}
	this.ReadOnlyMode();
	},
	
NavigateId: function(id) {this.Navigate(K.Get(id));},

LinkK: function(sName, k)
	{
	if (k instanceof Array)
		{
		var span = document.createElement('span');
		for (var i = 0; i < k.length; i++)
			{
			if (i > 0)
				span.appendChild(document.createTextNode(", "));
			span.appendChild(this.LinkK(sName, k[i]));
			}
		return span;
		}

	// Don't link to BuiltIn elements with values - just display
	if (k.IsA(K.kBuiltin) && k._value != undefined)
		{
		if (this.mode == 'read')
			{
			var span = document.createElement('span');
			DOM.SetText(span, K.ToString(k));
			return span;
			}
		var inp = document.createElement('input');
		inp.type = "text";
		inp.value = K.ToString(k);
		this.mControls[k._id] = {'sName': sName, 'inp': inp,  'fOwn': this.k.IsOwn(sName, k)};
		return inp;
		}

	var link = document.createElement('a');
	link.href = "#";
	link.setAttribute("onclick", this.SGlobalName("NavigateId") + "(" + k._id + ");return false;");
	if (k.IsA(K.kBuiltin) && k._value)
		DOM.SetText(link, '"' + k._value.toString() + '" (' + k._id + ". " + k.SName() + ")");
	else
		DOM.SetText(link, k._id + ". " + k.SName());
	return link;
	},
	
MakeChild: function(id)
	{
	var k = K.New(K.Get(id));
	this.Navigate(k);
	},

}); // NS

}); // kahnsept.browser Namespace