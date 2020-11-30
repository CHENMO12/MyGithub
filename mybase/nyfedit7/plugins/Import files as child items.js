
//sValidation=nyfjs
//sCaption=Import files as child items ...
//sHint=Import local files as child items, with text files saved as default contents, else as attachments
//sCategory=MainMenu.Capture
//sCondition=CURDB; DBRW; OUTLINE; CURINFOITEM
//sID=p.ImportFilesAsChild
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

var xNyf=new CNyfDb(-1);

if(xNyf.isOpen()){

	if(!xNyf.isReadonly(-1)){

		var sCfgKey1='ImportFilesAsChild.sDir';
		var vFiles=platform.getOpenFileNames({
			sTitle: plugin.getScriptTitle()
			, sInitDir: localStorage.getItem(sCfgKey1)||''
			, sFilter: 'All files (*.*);;HTML documents (*.htm;*.html);;Text file (*.rtf;*.txt);;Images (*.png;*.jpg;*.gif;*.bmp)'
		});

		if(vFiles && vFiles.length>0){

			localStorage.setItem(sCfgKey1, new CLocalFile(vFiles[0]).getDirectory(false));

			plugin.initProgressRange(plugin.getScriptTitle(), vFiles.length);

			var sCurItem=plugin.getCurInfoItem(-1), nDone=0;

			if(!sCurItem) sCurItem=plugin.getDefRootContainer();

			{
				//2016.4.14 invoke the common functions predefined for plugins;
				var xFn=new CLocalFile(new CLocalFile(plugin.getScriptFile()).getDirectory(false), 'comutils.js');
				var sCode=xFn.loadText('auto');
				if(sCode){
					eval.call(null, sCode);
				}
			}

			var _get_unique_child_id=function(sSsgPath){
				return xNyf.getChildEntry(sSsgPath, 0);
			};

			var _is_htm_utf8=function(s){
				return (s||'').match(/content=\"text\/html;\s+charset=utf-8\"/i)!=null;
			};

			var sTmpDir=platform.getTempFolder(), sTmpName='__nyf7_import_files_as_child_items';
			var xTmpFn=new CLocalFile(sTmpDir, sTmpName+'.html'); if(plugin.deferDeleteFile) plugin.deferDeleteFile(xTmpFn); else platform.deferDeleteFile(xTmpFn);

			for(var i in vFiles){
				var xFn=new CLocalFile(vFiles[i]);
				var sExt=xFn.getSuffix(false)||'', sFileName=xFn.getFileName()||'', sTitle=xFn.getTitle()||'', sDir=xFn.getDirectory()||'';
				var tMod=xFn.getModifyTime();

				var bContinue=plugin.ctrlProgressBar(sFileName, 1, true);
				if(!bContinue) break;

				{
					//2018.1.8 consider of the rich-text file ever exported by v7.0-b27+ with an extension name '.qrich.html';
					var sSuffix=xFn.getCompleteSuffix(false);
					if(sSuffix=='qrich.html'){
						sExt='qrich';
						sFileName=sFileName.replace(/qrich.html$/i, sExt);
					}
				}

				{
					//2018.1.8 consider of the file originated (exported) from info item's default contents;
					if(sFileName.search(/^[_]*(defcontent|defnote|itemcontent|index|default|def|home)\.(html|htm|qrich|qrich\.html|txt|md|rtf)$/i)==0){
						sFileName=plugin.getDefNoteFn(sExt); //set it as the default content of the new info item;
						sTitle=new CLocalFile(sDir).getLeafName(); //use the parent folder's name as the new info item's title;
					}
				}

				var xChild=new CLocalFile(sCurItem); xChild.append(_get_unique_child_id(sCurItem));
				if(sExt.search(/^(html|htm|qrich)$/i)==0){

					var sHtml=xFn.loadText('auto'); //'html' for detection of charset from within HTML source in case of BOM not present;

					var sNew=importAccompanyingObjsWithinHtml(xNyf, xChild, sHtml, sDir);

					if(sHtml!=sNew){
						sNew=changeHtmlCharset(sNew, 'UTF-8');
						xTmpFn.saveUtf8(sNew);
						xFn=xTmpFn;
					}
				}

				if(xNyf.createFolder(xChild)){
					xNyf.setFolderHint(xChild, sTitle||'untitled');
					var xSsgFn=new CLocalFile(xChild); xSsgFn.append(sFileName);
					var nBytes=xNyf.createFile(xSsgFn, xFn);
					if(nBytes>=0){
						xNyf.setModifyTime(xSsgFn.toString(), tMod);
						nDone++;
					}else{
						if(!confirm(_lc2('GoOnAnyway', 'Failed to import the file. Continue anyway?')+'\n\n'+sFn)){
							break;
						}
					}
				}
			}

			xTmpFn.remove(); //actively clean it up;

			if(nDone>0){
				plugin.refreshOutline(-1, sCurItem);
				plugin.destroyProgressBar();
				var sMsg=_lc2('Done', 'Total %nDone% child item(s) successfully imported.').replace(/%nDone%/gi, ''+nDone);
				alert(sMsg);
			}

		}

	}else{
		alert(_lc('Prompt.Warn.ReadonlyDb', 'Cannot modify the database opened as Readonly.'));
	}

}else{
	alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
}
