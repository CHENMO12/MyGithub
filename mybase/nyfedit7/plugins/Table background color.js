
//sValidation=nyfjs
//sCaption=Background color ...
//sHint=Set background color of the selected cells in the table
//sCategory=MainMenu.Table
//sPosition=TBL-03-ATTR-02
//sCondition=CURDB; DBRW; CURINFOITEM; FORMATTED; EDITING; TABLE
//sID=p.Table.BackColor
//sAppVerMin=7.0
//sShortcutKey=
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

try{
	var xNyf=new CNyfDb(-1);

	if(xNyf.isOpen()){

		if(!xNyf.isReadonly()){

			if(plugin.isContentEditable()){

				var sCfgKey1='TableBackColor.Color';

//				var sCode, sOld;
//				if(!sOld){
//					sCode='cellCssUtil("background-color");';
//					sOld=plugin.runDomScript(-1, sCode); if(sOld=='undefined') sOld='';
//				}
//				if(!sOld){
//					sCode='tableCssUtil("background-color");';
//					sOld=plugin.runDomScript(-1, sCode); if(sOld=='undefined') sOld='';
//				}

				var sOld=plugin.getCellBackColor(-1);

				var vFields = [
					{sField:  "colorpicker", sLabel: _lc2('Descr', 'Background color'), sInit: sOld||localStorage.getItem(sCfgKey1)||''}
				];

				var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 400, vMargins: [10, 0, 30, 0]});
				if(vRes.length>0){

					var sColor=vRes[0]||'';
					
					if(sColor.toLowerCase()=='transparent') sColor='';

					localStorage.setItem(sCfgKey1, sColor);

					//sCode='\n'+'cellCssUtil("background-color", "%COLOR%");'.replace(/%COLOR%/g, sColor);
					//if(plugin.runDomScript(-1, sCode)){
					//}

					plugin.setCellBackColor(-1, sColor);
				}

			}else{
				alert(_lc('Prompt.Warn.ReadonlyContent', 'Cannot modify the content opened as Readonly.'));
			}

		}else{
			alert(_lc('Prompt.Warn.ReadonlyDb', 'Cannot modify the database opened as Readonly.'));
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}
}catch(e){
	alert(e);
}
