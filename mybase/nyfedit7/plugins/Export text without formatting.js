
//sValidation=nyfjs
//sCaption=Export text without formatting ...
//sHint=Export current text contents and save as a plain text file
//sCategory=MainMenu.Share
//sCondition=CURDB; OUTLINE; CURINFOITEM
//sID=p.ExportPlainText
//sAppVerMin=7.0
//sAuthor=wjjsoft

/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2016 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

var _lc=function(sTag, sDef){return plugin.getLocaleMsg(sTag, sDef);};
var _lc2=function(sTag, sDef){return _lc(plugin.getLocaleID()+'.'+sTag, sDef);};

var _trim=function(s){return (s||'').replace(/^\s+|\s+$/g, '');};
var _trim_cr=function(s){return (s||'').replace(/\r+$/g, '');};

var _validate_filename=function(s){
	s=s||'';
	s=s.replace(/[\*\?\.\(\)\[\]\{\}\<\>\\\/\!\$\^\&\+\|,;:\"\'`~@]/g, ' ');
	s=s.replace(/\s{2,}/g, ' ');
	s=_trim(s);
	if(s.length>64) s=s.substr(0, 64);
	s=_trim(s);
	s=s.replace(/\s/g, '_');
	return s;
};

try{

	var xNyf=new CNyfDb(-1);
	if(xNyf.isOpen()){

		var sCurItem=plugin.getCurInfoItem(-1);
		var sItemTitle=xNyf.getFolderHint(sCurItem);

		var sCfgKey='ExportPlainText.sDstFn';

		var xInitFn = new CLocalFile(localStorage.getItem(sCfgKey)||''); xInitFn.append(_validate_filename(sItemTitle)||'untitled' + '.txt');

		var sDstFn=platform.getSaveFileName(
			{ sTitle: plugin.getScriptTitle()
			, sInitDir: xInitFn
			, sFilter: 'Plain text files (*.txt);;All files (*.*)'
			});

		if(sDstFn){

			var xDstFn=new CLocalFile(sDstFn);
			localStorage.setItem(sCfgKey, xDstFn.getParent());

			plugin.initProgressRange(plugin.getScriptTitle(), 0);
			plugin.ctrlProgressBar('Extract plain text', 1, false);

			var sHtml = plugin.getSelectedText(-1, true); if(!sHtml) sHtml = plugin.getTextContent(-1, true);
			var sTxt = platform.extractTextFromHtml(sHtml);

			//2015.9.4 consider CRLF as EOL on Windows
			if(platform.getOsType() == 'Win32'){
				var s = '';
				var vLines = sTxt.split('\n');
				for(var i in vLines){
					if(s) s += '\r\n';
					s += _trim_cr(vLines[i]);
				}
				sTxt = s;
			}

			if(sTxt){

				plugin.ctrlProgressBar('Save text', 1, false);

				if(xDstFn.saveUtf8(sTxt)>0){
					plugin.destroyProgressBar();
					var sMsg=_lc2('Done', 'Successfully exported plain text to the specified file. View it now?');
					if(confirm(sMsg+'\n\n'+xDstFn)){
						xDstFn.launch('');
					}
				}
			}else{
				alert(_lc2('NoTextAvail', 'No plain text available to export.'));
			}
		}
	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
