
//sValidation=nyfjs
//sCaption=Copy link address ...
//sHint=Copy link address of the current item
//sCategory=MainMenu.Organize; Context.Outline
//sCondition=CURDB; DBRW; OUTLINE; CURINFOITEM
//sID=p.CopyItemLink
//sAppVerMin=7.0
//sShortcutKey=
//sAuthor=wjjsoft

/////////////////////////////////////////////////////////////////////
// Extension scripts for Mybase Desktop v7.x
// Copyright 2010-2020 Wjj Software. All rights Reserved.
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

		//if(!xNyf.isReadonly())
		{

			if(plugin.getCurNavigationTab()==='Outline'){

				var sCurItem=plugin.getCurInfoItem();
				if(sCurItem){
					if(!xNyf.isReadonly()) xNyf.getItemIDByPath(sCurItem, true);
					var sUrl=xNyf.makeInfoItemLink('', sCurItem, '', xNyf.getFolderHint(sCurItem));
					if(sUrl){
						var vUrls=[], sTxt=sUrl; //2016.5.8 ignore urls, as on pasting it has higher priority than HTML/TEXT;
						vUrls.push(sUrl);

						var sDataType='', vMimeData=[];
						{
//							if(sHtml){
//								if(sDataType) sDataType+=',';
//								sDataType+='html';
//								vMimeData.push(sHtml);
//							}
							if(sTxt){
								if(sDataType) sDataType+=',';
								sDataType+='text';
								vMimeData.push(sTxt);
							}
							if(vUrls.length>0){
								if(sDataType) sDataType+=',';
								sDataType+='urls';
								vMimeData.push(vUrls.join('\n'));
							}
						}

						if(sDataType && vMimeData.length>0){
							platform.setClipboardData(sDataType, vMimeData);
						}else{
							alert('No contents copied to clipboard.');
						}

					}else{
						alert('Failed to make item link.');
					}
				}else{
					alert(_lc('Prompt.Warn.NoInfoItemSelected', 'No info item is currently selected.'));
				}

			}else{
				alert(_lc('Prompt.Warn.OutlineNotSelected', 'The outline tree view is currently not selected.'));
			}

		//}else{
		//	alert(_lc('Prompt.Warn.ReadonlyDb', 'Cannot modify the database opened as Readonly.'));
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}
}catch(e){
	alert(e);
}
