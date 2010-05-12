// ==UserScript==
// @name           Blue Dot Dolphin Delta
// @namespace      http://bluedot.us
// @description    Proposed changes for Blue Dot Dolphin Pages
// @include        http://test1/*
// ==/UserScript==

GM_log("Start: " + new Date());
var stGreek = "Aenean adipiscing. Duis ut urna. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras id nisl. Ut quis ante. <br><br>Nullam vel elit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. In sollicitudin sollicitudin magna. Mauris bibendum. Maecenas condimentum leo a erat. Suspendisse molestie, dolor eu porttitor accumsan, nisi velit blandit leo, non scelerisque nibh est id magna. Sed dictum suscipit orci. Mauris imperdiet, sem vel consequat bibendum, enim est vulputate nisl, eget faucibus sapien risus vel dui. Vestibulum faucibus massa ut felis. Sed non magna sed mi venenatis egestas."

function AddGlobalStyle(css) {
    var head, style;
    head = document.getElementsByTagName('head')[0];
    if (!head) { return; }
    style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = css;
    head.appendChild(style);
}

function ChildTagClass(node, tag, class)
{
	var i;
	var nodeChildren;

	if (!node)
		return null;

	nodeChildren = node.getElementsByTagName(tag);
	if (nodeChildren.length == 0)
		return null;
	for (i = 0; i < nodeChildren.length; i++)
		{
		var nodeT = nodeChildren[i];
		if (class == undefined || nodeT.className == class)
			return nodeT;
		}
	return null;
}

String.prototype.StReplace = function(stPat, stRep)
{

	var st = "";

	var ich = 0;
	var ichFind = this.indexOf(stPat, 0);

	while (ichFind >= 0)
		{
		st += this.substring(ich, ichFind) + stRep;
		ich = ichFind + stPat.length;
		ichFind = this.indexOf(stPat, ich);
		}
	st += this.substring(ich);

	return st;
}

AddGlobalStyle('a.frameS { \
	background-position:top center; \
	border-style: none; \
	}');
AddGlobalStyle('a.frameL { \
	background-position:top center; \
	border-style: none; \
	}');
AddGlobalStyle(' #featured a.t { \
	font-weight: bold; \
	}');
AddGlobalStyle('a.small { font-weight: bold; }');

var dotF = document.evaluate("//div[@class='featuredDot']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (dotF)
	{
	var pF = dotF.getElementsByTagName("P")[0];
	pF.textContent = pF.textContent.StReplace("...", stGreek);
	}

GM_log("Do NOT trip featured dot text - would LIKE up to 10 lines of text for balance");

AddGlobalStyle('#adPlacementFeaturedDot {margin-left: 10px !important;}');

var aTags = document.getElementsByTagName("A");
var i;

GM_log("A's: " + aTags.length);
for (i = 0; i < aTags.length; i++)
	{
	if (aTags[i].className == "frameL" || aTags[i].className == "frameS")
		{
		var aImg = aTags[i];
		var img;
		var stImg;

		stImg = aImg.style.backgroundImage + "";
		stImg = stImg.StReplace("url(", "").StReplace(")", "");
		aImg.style.backgroundImage = null;

		img = document.createElement("IMG");
		if (aImg.className =="frameL")
			img.setAttribute("style", "float:left; margin-right: 5px;border:none;");
		else
			{
			img.setAttribute("style", "float:right; margin-left: 5px;border:none;");
			stImg = stImg.StReplace("_1", "_2");
			}

		img.src = stImg;		aImg.appendChild(img);
		aImg.className = null;
		}
	}




