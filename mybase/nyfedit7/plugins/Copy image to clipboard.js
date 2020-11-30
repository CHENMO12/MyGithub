
//sValidation=nyfjs
//sCaption=Copy image
//sHint=Copy the image in context to clipboard
//sCategory=Context.ImgUtils
//sPosition=
//sCondition=CURDB; DBRW; CURINFOITEM; FORMATTED; IMAGE;
//sID=p.Image.Copy
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

try{
	var xNyf=new CNyfDb(-1);

	if(xNyf.isOpen()){

		var sSrc=plugin.getDataImageBase64(-1)||'';
		if(sSrc){
			var re=new RegExp('data:image\\/(png|jpg|jpeg|gif|bmp|tiff);base64,(.+)$', 'i');
			var m=re.exec(sSrc);
			if(m && m.length>2){
				sSrc=m[2];
				if(sSrc){
					platform.setClipboardData('base64img', [sSrc]);
				}
			}

		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}
}catch(e){
	alert(e);
}
