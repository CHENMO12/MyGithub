
//sValidation=nyfjs
//sCaption=Diagnose file parser ...
//sHint=Diagnose file parser with current document or selected attachments
//sCategory=MainMenu.Tools; Context.Attachments
//sCondition=CURDB; CURINFOITEM
//sID=p.DiagnoseParser
//sAppVerMin=7.0
//sShortcutKey=
//sAuthor=wjjsoft

/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////


var _lc=function(sTag, sDef){return plugin.getLocaleMsg(sTag, sDef);};
var _lc2=function(sTag, sDef){return _lc(plugin.getLocaleID()+'.'+sTag, sDef);};

var _trim=function(s){return (s||'').replace(/^\s+|\s+$/g, '');};
var _trim_r=function(s){return (s||'').replace(/\s+$/g, '');};
var _trim_cr=function(s){return (s||'').replace(/\r+$/g, '');};

var _trim_blanklines=function(sLines){
	var v=sLines.split('\n'), r='';
	for(var i in v){
		var s=_trim_r(v[i]);
		if(s){
			if(r) r+='\n';
			r+=s;
		}
	}
	return r;
};

try{

	var xNyf=new CNyfDb(-1);
	if(xNyf.isOpen()){

		/*var vFiles=[];
		var sRes=plugin.getSelectedAttachments('\t')||'';
		if(sRes){
			var vLines=sRes.split('\n');
			for(var i in vLines){
				var s=vLines[i]||'';
				var v=s.split('\t');
				var sDbPath=v[0], sSsgPath=v[1], sSsgName=v[2];
				var xFn=new CLocalFile(sSsgPath); xFn.append(sSsgName);
				vFiles.push(xFn.toString());
			}
		}else{
			var sCurFn=plugin.getCurDocFile();
			if(sCurFn) vFiles.push(sCurFn);
		}*/

		var bFullPath=true;
		var vFiles=plugin.getSelectedAttachments(-1, bFullPath);
		if(!vFiles || vFiles.length<=0){
			var sCurFn=plugin.getCurDocFile();
			if(sCurFn) vFiles.push(sCurFn);
		}

		var sRes='';
		for(var i in vFiles){

			var xSsgFn=new CLocalFile(vFiles[i]), sSrcFn='', sTxt='';

			if(xNyf.isShortcut(xSsgFn)){
				sSrcFn=xNyf.getShortcutFile(xSsgFn, true);
			}

			if(sRes) sRes+='\n\n\n';

			if(sSrcFn){
				sRes+='########## %sSsgFn% --> %sShortcut% ##########\n\n'.replace(/%sSsgFn%/g, xSsgFn.getLeafName()).replace(/%sShortcut%/g, sSrcFn);
			}else{
				sRes+='########## %sSsgFn% ##########\n\n'.replace(/%sSsgFn%/g, xSsgFn.getLeafName());
			}

			sTxt=xNyf.parseFile(xSsgFn.getDirectory(), xSsgFn.getLeafName(), false);

			sRes+=_trim_blanklines(sTxt);
		}

		if(sRes){

			textbox({
				sTitle: plugin.getScriptTitle()
				, sDescr: _lc2('Descr', 'Reports on diagnosing file parsers with the documents; The following contents are searchable.')
				, sDefTxt: sRes
				, bReadonly: true
				, bWordwrap: true
				, nWidth: 70
				, nHeight: 60
			});
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
