
//sValidation=nyfjs
//sCaption=Edit stylesheet for Markdown ...
//sHint=Edit stylesheet for Markdown document renderer
//sCategory=MainMenu.Tools; Context.Action.Edit.Markdown; Context.HtmlView.Markdown
//sCondition=
//sID=p.MarkdownCss
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

try{	
	var sFnSel='marked.css';
	var xFn=new CLocalFile(plugin.getPathToDomScripts(), sFnSel);
	if(xFn.exists()){
		var sCss=xFn.loadText('auto');
		var sMsg=_lc2('Descr', 'Custom stylesheet for Markdown document renderer.');
		sCss=textbox({
				     sTitle: plugin.getScriptTitle()
				     , sDescr: sMsg
				     , sDefTxt: sCss
				     , bReadonly: false
				     , bWordwrap: false
				     , bFind: true
				     , bFont: true
				     , bRich: false
				     , nWidth: 85
				     , nHeight: 80
				     , sBtnOK: _lc('p.Common.Apply', 'Apply')
			     });

		if(sCss){
			if(xFn.saveUtf8(sCss)>0){
				plugin.refreshDocViews(-1, '');
			}else{
				alert('Failed to save changes to the stylesheet file.' + '\n\n' + xFn.toString());
			}
		}
	}

}catch(e){
	alert(e);
}
