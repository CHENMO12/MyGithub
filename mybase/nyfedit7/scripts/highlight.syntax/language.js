
/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2017 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

//
//Map of Language ID and suffix name for Syntax highlighting
//

var languageOf = function(sExt, sSrc){
	var sLid;
	if(sExt){
		var m = {
			'html': 'html;htm;xml;qrich'
			, 'cpp': 'c;cc;cpp;cxx;c++;h;hpp;hxx'
			, 'java': 'java'
			, 'cs': 'cs'
			, 'js': 'js;json'
			, 'sql': 'sql'
			, 'php': 'php'
			, 'go': 'go'
			, 'vb': 'vb'
			, 'py': 'py'
			, 'pl': 'pl;cgi'
			, 'as': 'as'
			, 'ruby': 'rb;rbw'
			, 'delphi': 'pas'
			, 'bash': 'sh'
			, 'objc': 'm;mm' //2016.4.20 'm' conflicts with 'mathlib'
			, 'swift': 'swift'
			, 'md': 'md;mark;markdown'
			, 'css': 'css;qss'
			, 'rust': 'rs'
			, 'r': 'r'
		};
		sExt=sExt.toLowerCase();
		for(var sID in m){
			var vExts = m[sID].split(';');
			if(vExts.indexOf(sExt) >= 0){
				sLid = sID;
			}
		}

		if(sSrc && sExt.toLowerCase()=='m'){
			//2016.4.20 to resolve conflicts of .m suffix between Objective-C and MathLib;
			if(sSrc.search(/\n\s*%.+/)>=0 || sSrc.search(/\n*\s*#import\s*<.*?>/)<0 || sSrc.search(/\bNS\w{2,64}\b/)<0 || sSrc.search(/\bmathlib\b/i)>0){
				sLid='mathlib';
			}
		}
	}
	return sLid;
};
