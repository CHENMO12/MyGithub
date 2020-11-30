
//sValidation=nyfjs
//sCaption=Import data from .nyf file ...
//sHint=Import info items from a .nyf file in a specified branch
//sCategory=MainMenu.Capture
//sCondition=CURDB; DBRW; OUTLINE; CURINFOITEM
//sID=p.ImportNyf
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

try{

	var xNyf=new CNyfDb(-1)

	if(xNyf.isOpen()){

		if(!xNyf.isReadonly()){

			var sCfgKey='ImportNyf.Dir';
			var sDbSrc=platform.getOpenFileName(
				{ sTitle: plugin.getScriptTitle()
				, sInitDir: localStorage.getItem(sCfgKey)||''
				, sFilter: 'myBase .nyf files (*.nyf)|*.nyf|All files (*.*)|*.*'
				, bMultiSelect: false
				, bHideReadonly: true
				});

			if(sDbSrc){

				if(plugin.getDbIndex(sDbSrc)<0){

					var sDir=new CLocalFile(sDbSrc).getDirectory();
					localStorage.setItem(sCfgKey, sDir);

					var sPathSrc='', sDefRoot=plugin.getDefRootContainer();

					var sMsg=_lc2('SelSrc', 'Select a source branch to import.');
					var xDbSrc=new CNyfDb(sDbSrc, true);
					if(xDbSrc.isOpen()){
						sPathSrc=xDbSrc.browseOutline(sMsg, sDefRoot);
						xDbSrc.close();
					}else{
						alert(_lc('Prompt.Failure.OpenDb', 'Failed to open the database.')+'\n\n'+sDbSrc);
					}

					if(sPathSrc){
						var bSucc=plugin.importNyfFile(-1, sDbSrc, sPathSrc);
						if(bSucc){
							alert(_lc2('Done', 'Successfully imported data from within the .nyf file.')+'\n\n'+sDbSrc);
						}else{
							sMsg=_lc2('Failure', 'Failed to import data from within the .nyf file.');
							alert(sMsg+'\n\n'+sDbSrc);
						}
					}
				}else{
					alert('Cannot import data from the database that is in use. Please be sure first to close it before operation.'+'\n\n'+sDbSrc);
				}
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
