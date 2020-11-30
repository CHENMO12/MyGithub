
//sValidation=nyfjs
//sCaption=Export image file ...
//sHint=Export current content as an image file
////sCategory=MainMenu.Share; Context.HtmlEdit; Context.HtmlView; Context.RichEdit; Context.RichView; Context.TextEdit; Context.TextView; Context.Hyperlink
//sCategory=MainMenu.Share;
//sCondition=CURDB; OUTLINE; CURINFOITEM; CURDOC;
//sID=p.ExportPageAsImage
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
	s=s.replace(/[\*\?\.\(\)\[\]\{\}\<\>\\\/\!\$\^\&\+\|,;:\"\'`~@]+/g, ' ');
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

		var sCurDocFn=plugin.getCurDocFile(), sCurDocPath=plugin.getCurDocPath();
		var sExt=new CLocalFile(sCurDocFn).getSuffix(false).toLowerCase();
		var sItemTitle=xNyf.getFolderHint(sCurDocPath);

		var sName;
		if(!xNyf.folderExists(sCurDocFn)){ //consider of non-file contents e.g. image-gallery;

			var xDocFn=new CLocalFile(sCurDocFn);

			sName=xDocFn.getLeafName();
			if(plugin.isReservedNoteFn(sName)){
				sName=(_validate_filename(sItemTitle)||'untitled') + '.jpg';
			}else{
				var sExt=xDocFn.getSuffix(false).toLowerCase();
				if(sExt!='html'){
					sName+='.jpg'; //consider of non-html contents, forcedly turn into .jpg;
				}
			}
		}

		var sCfgKey='ExportPageAsImage.sDstFn';

		var xInitFn = new CLocalFile(localStorage.getItem(sCfgKey)||platform.getHomePath()||'', sName);

		var sDstFn=platform.getSaveFileName(
					{ sTitle: plugin.getScriptTitle()
						, sInitDir: xInitFn
						, sFilter: 'Images (*.jpg;*.jpeg;*.png;*.bmp);;All files (*.*)'
					});

		if(sDstFn){
			var xDstFn=new CLocalFile(sDstFn);
			localStorage.setItem(sCfgKey, xDstFn.getParent());

			var c=new CCanvas();
			var sHtml = plugin.getTextContent(-1, true);
			var sUrl = plugin.getCurUrl(-1);

			c.renderHtml(sHtml, sUrl, true);

			var nJpegQuality=99;
			if(c.saveAs(xDstFn, xDstFn.getSuffix(false), nJpegQuality)){
				var sMsg=_lc2('Done', 'Successfully exported the page to the image file. View it now?');
				if(confirm(sMsg+'\n\n'+xDstFn)){
					xDstFn.launch('open');
				}
			}else{
				alert(_lc2('Fail.Save', 'Failed to export the page as image.'));
			}
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
