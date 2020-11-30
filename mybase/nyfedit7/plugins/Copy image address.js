
//sValidation=nyfjs
//sCaption=Copy image address
//sHint=Copy the image address to system clipboard
//sCategory=Context.ImgUtils
//sPosition=
//sCondition=CURDB; DBRW; CURINFOITEM; FORMATTED; IMAGE;
//sID=p.Image.CopyLink
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

		var sUrl=plugin.getImageUrl(-1);

		var sDataType='', vMimeData=[];
		if(sUrl){

			if(sDataType) sDataType+=',';
			sDataType+='text';
			vMimeData.push(sUrl);

			if(sUrl.search(/data:image\/(png|jpg|jpeg|gif|bmp|tiff);base64,/i)<0){
				if(sUrl.search(/^(file|http|https|ftp|gopher|mailto):\/\/.+/)==0){
					if(sDataType) sDataType+=',';
					sDataType+='urls';
					vMimeData.push([sUrl]);
				}
			}
		}

		if(sDataType && vMimeData.length>0){
			platform.setClipboardData(sDataType, vMimeData);
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}
}catch(e){
	alert(e);
}
