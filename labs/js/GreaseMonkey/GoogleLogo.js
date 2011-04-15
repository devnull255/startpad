// ==UserScript==
// @name           Google Logo Replacement
// @namespace      http://bluedot.us
// @description    Replaces the google logo with one of our choosing
// @include        http://www.google.com/*
// @include        http://google.com/*
// ==/UserScript==

var stLogo = "http://www.google.com/logos/velasquez.gif";

function FindGoogleLogo()
{
	var images = document.getElementsByTagName("img");
	for (var i = 0; i < images.length; i++)
		{
		if (/\/logos\//.test(images[i].src))
			return images[i];
		}
	return null;
}

var imgLogo = FindGoogleLogo();
if (imgLogo)
	{
	imgLogo.src = stLogo;
	imgLogo.title = imgLogo.alt = "Hi, Dana!";
	}
