
//sValidation=nyfjs
//sCaption=Export text with delimiter ...
//sHint=Export text contents in current branch with a text seperator and save as a text file
//sCategory=MainMenu.Share
//sCondition=CURDB; CURINFOITEM; OUTLINE
//sID=p.ExportTextByDelimiter
//sAppVerMin=7.0
//sAuthor=wjjsoft

/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2018 Wjj Software. All rights Reserved.
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

		if(plugin.isContentEditable()) plugin.commitCurrentChanges();

		var sCurItem=plugin.getCurInfoItem(-1)||plugin.getDefRootContainer();
		var sItemTitle=xNyf.getFolderHint(sCurItem);

		var sCfgKey1='ExportTextByDelimiter.sDir', sCfgKey2='ExportTextByDelimiter.sDelimiter';
		var vFields = [
			{sField: "savefile", sLabel: _lc2('DstFn', 'Save as text file'), sTitle: plugin.getScriptTitle(), sFilter: 'Text files (*.txt);;All files (*.*)', sInit: localStorage.getItem(sCfgKey1)||_validate_filename(sItemTitle)||'untitled'}
			, {sField: "lineedit", sLabel: _lc2('Delimiter', 'Delimiter to separate text content'), sInit: localStorage.getItem(sCfgKey2)||'----------------------------------------'}
		];

		var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 500, vMargins: [2, 0, 50, 0], bVert: true});
		if(vRes && vRes.length==2){

			var sDstFn=vRes[0], sDelimiter=vRes[1];
			if(sDstFn && sDelimiter){

				localStorage.setItem(sCfgKey1, sDstFn);
				localStorage.setItem(sCfgKey2, sDelimiter);

				var sRes='', sDefNoteFn=plugin.getDefNoteFn(), nDone=0;
				var _act_on_treeitem=function(sSsgPath, iLevel){

					var sTitle=xNyf.getFolderHint(sSsgPath); if(!sTitle) sTitle='== Untitled ==';

					var sPreferred=xNyf.detectPreferredFile(sSsgPath, "html;qrich;txt;md;rtf>htm;ini;log");
					if(sPreferred){
						var xSsgFn=new CLocalFile(sSsgPath); xSsgFn.append(sPreferred);
						var sExt=xSsgFn.getSuffix(false)||'';

						var s=xNyf.loadText(xSsgFn, 'auto');

						if(sExt.search(/^(html|htm|qrich)$/i)==0) s=platform.extractTextFromHtml(s);
						else if(sExt.search(/^rtf$/i)==0) s=platform.extractTextFromRtf(s);

						s=_trim(s);
						{
							//eliminates extra blank lines;
							s=s.replace(/\r\n/g, '\n');
							s=s.replace(/\r/g, '\n');
							s=s.replace(/\n{3,}/g, '\n\n');
							s=s.replace(/\n/g, '\r\n');
						}
						if(s){
							if(sRes){
								sRes+='\r\n\r\n\r\n'+sDelimiter+'\r\n\r\n\r\n';
							}
							sRes+=''+(nDone+1)+') ';
							sRes+=sTitle;
							sRes+='\r\n\r\n';
							sRes+=s;
							nDone++;
						}
					}
				};

				xNyf.traverseOutline(sCurItem, true, _act_on_treeitem);

				var nBytes=-1;
				if(sRes){
					nBytes=new CLocalFile(sDstFn).saveUtf8(sRes);
				}
				if(nBytes<=0){
					alert('Failed to export text content to the file.\n\n'+sDstFn);
				}else{
					sMsg=_lc2('Done', 'Total %nDone% info items successfully exported to the file. View it now?');
					sMsg=sMsg.replace('%nDone%', nDone)+'\n\n'+sDstFn;
					if(confirm(sMsg)){
						new CLocalFile(sDstFn).exec();
					}
				}
			}
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
