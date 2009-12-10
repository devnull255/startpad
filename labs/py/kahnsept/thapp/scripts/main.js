global_namespace.Define('kahnsept.thapp', function(NS) {
	var Timer = NS.Import('startpad.timer');

NS.Extend(NS, {
	sSiteName: "ThApp",
	sCSRF: "",
	apikey: undefined,
	msLoaded: Timer.MSNow(),

Init: function(sCSRF)
	{
	NS.sCSRF = sCSRF;
	}	
});});