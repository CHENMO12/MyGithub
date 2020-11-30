
//sValidation=nyfjs
//sCaption=Replicate database ...
//sHint=Replicate the currently working database to a new .nyf file
//sCategory=MainMenu.File.Maintenance
//sCondition=CURDB
//sID=p.ReplicateDatabase
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

		//plugin.initProgressRange(plugin.getScriptTitle());

		var sCfgKey1='ReplicateDatabase.sDbPath', sCfgKey2='ReplicateDatabase.bTrash';

		var sInclTrashes=(localStorage.getItem(sCfgKey2)?'1':'0')+'|'+_lc2('InclTrashes', 'Including trashed entries');
		var vFields = [
			  {sField: 'savefile', sLabel: _lc2('DestFile', 'New database'), sTitle: plugin.getScriptTitle(), sFilter: 'myBase database (*.nyf);;All files(*.*)', sInit: localStorage.getItem(sCfgKey1)||''}
			, {sField: 'lineedit', sLabel: _lc2('Passwd', 'New password'), sInit: '', bReq: false}
			, {sField: 'check', sLabel: '', vItems: [sInclTrashes]}
		];

		var vRes=input(plugin.getScriptTitle(), vFields, {nMinSize: 550, vMargins: [6, 0, 30, 0], bVert: false});
		if(vRes && vRes.length==3){

			var sDbFn=vRes[0], sPasswd=vRes[1], bTrash=vRes[2][0], nZlib=9, bUtf8=true;

			localStorage.setItem(sCfgKey1, sDbFn);
			localStorage.setItem(sCfgKey2, bTrash);

			var xFn=new CLocalFile(sDbFn);
			if(xFn.createFile()){
				var bRO=false;
				var xDbDst=new CNyfDb(sDbFn, bRO);
				if(xDbDst.isOpen()){

					if(sPasswd) xDbDst.setDbPassword(sPasswd);
					if(nZlib>=0 && nZlib<=9) xDbDst.setCompressLevel(nZlib);

					//var sDefNoteFn=plugin.getDefNoteFn();

					var _copy_entry_attr=function(sSsgPath){
						xDbDst.setEntryHint(sSsgPath, xNyf.getEntryHint(sSsgPath));
						xDbDst.setEntryAttr(sSsgPath, xNyf.getEntryAttr(sSsgPath));
						xDbDst.setEntryAppAttr(sSsgPath, xNyf.getEntryAppAttr(sSsgPath));

						var n=xNyf.getEntryAppDataCount(sSsgPath);
						for(var i=0; i<n; ++i){
							var x=xNyf.getEntryAppDataAt(sSsgPath, i, -1);
							xDbDst.setEntryAppDataAt(sSsgPath, i, x);
						}

						xDbDst.setCreateTime(sSsgPath, xNyf.getCreateTime(sSsgPath));
						xDbDst.setModifyTime(sSsgPath, xNyf.getModifyTime(sSsgPath));
					};

					var nInfoItems=0, vFail=[];
					var sUtf8Tag='__encoding.utf8';
					var xUtf8Tag=new CLocalFile(plugin.getDefRootContainer()); xUtf8Tag.append(sUtf8Tag);
					var _act_on_treeitem=function(sSsgPath, iLevel){

						if(xNyf.folderExists(sSsgPath, false)){

							var sTitle=xNyf.getFolderHint(sSsgPath); if(!sTitle) sTitle='New info item';

							var bContinue=plugin.ctrlProgressBar('#'+nInfoItems+' '+sTitle, 1, true);
							if(!bContinue) return true;

							if(xDbDst.createFolder(sSsgPath)){
								_copy_entry_attr(sSsgPath);
								var vFiles=xNyf.listFiles(sSsgPath, bTrash);
								for(var i in vFiles){
									var sName=vFiles[i];

									//var sMsg=sName; if(sMsg==sDefNoteFn) sMsg=sTitle;
									var sMsg=sName; if(plugin.isReservedNoteFn(sName)) sMsg=sTitle;

									bContinue=plugin.ctrlProgressBar(sMsg, 1, true);
									if(!bContinue) return true;

									var xSsgFn=new CLocalFile(sSsgPath); xSsgFn.append(sName);

									//2013.10.15 the UTF8 tag is already inserted while the new db was created.
									if(sName==sUtf8Tag && xSsgFn.toString()==xUtf8Tag.toString()){
										continue;
									}
									var sTmpFn=platform.getTempFile(); plugin.deferDeleteFile(sTmpFn);
									var xTmpFn=new CLocalFile(sTmpFn);
									if(xNyf.exportFile(xSsgFn, sTmpFn)>=0){
										if(xDbDst.createFile(xSsgFn, sTmpFn)<0){
											vFail.push('Failed to createFile: ' + xSsgFn);
										}
									}else{
										vFail.push('Failed to exportFile: ' + xSsgFn);
									}

									xTmpFn.remove();
									_copy_entry_attr(xSsgFn.toString());
								}
							}else{
								vFail.push('Failed to createFolder: ' + sSsgPath);
							}

							nInfoItems++;
							//if(xDbDst.getSsgVer()==5)
							{
								if(nInfoItems % 400 == 0){
									plugin.ctrlProgressBar('commiting ...', 1, false);
									xDbDst.save();
								}
							}
						}
					};

					xNyf.traverseOutline('/', false, _act_on_treeitem);

					plugin.ctrlProgressBar('Finishing ...', 1, false);
					if(xDbDst.save()){
						plugin.destroyProgressBar();
						if(vFail.length<=0){
							alert(_lc2('Done', 'Successfully replicated the database.')+'\n\n'+xNyf.getDbFile()+'\n-> '+sDbFn);
						}else{
							var sMsg=_lc2('Errors', 'Replicated the database but with some errors as follows;') + '\n\n' + vFail.join('\n');
							alert(sMsg);
						}
					}else{
						plugin.destroyProgressBar();
						alert("Failed to save changes to new database."+'\n\n'+sDbFn);
					}

				}else{
					alert('Failed to create the new database.'+'\n\n'+sDbFn);
				}
			}else{
				alert('Failed to create the new file.'+'\n\n'+sDbFn);
			}
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
