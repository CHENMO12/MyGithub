
//sValidation=nyfjs
//sCaption=Import MS-Word outline ...
//sHint=Import MSWord outline items and text contents via OLE-Automation
//sCategory=MainMenu.Capture
//sCondition=CURDB; DBRW; OUTLINE; CURINFOITEM;
//sPlatform=Windows
//sID=p.ImportMSWordOutline
//sPlatform=Windows
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
	var xNyf=new CNyfDb(-1);

	if(xNyf.isOpen()){

		if(!xNyf.isReadonly()){

			var sCfgKey='ImportMSWordOutline.Dir';

			var sSrcFn=platform.getOpenFileName(
				{ sTitle: plugin.getScriptTitle()
				, sInitDir: localStorage.getItem(sCfgKey)||''
				, sFilter: 'MS-Word documents (*.doc;*.docx)|*.doc;*.docx|All files (*.*)|*.*'
				, bMultiSelect: false
				, bHideReadonly: true
				});

			if(sSrcFn){

				var sDir=new CLocalFile(sSrcFn).getDirectory();
				localStorage.setItem(sCfgKey, sDir);

				var _find_unique_id=function(sSsgPath){
					return xNyf.getChildEntry(sSsgPath, 0);
				};

				var xMsw=new CAppWord();
				if(xMsw && xMsw.init()){

					xMsw.setVisible(false);

					plugin.initProgressRange(plugin.getScriptTitle());

					var sCurItem=plugin.getCurInfoItem(-1) || plugin.getDefRootContainer();

					var xTmpFn=new CLocalFile(platform.getTempFile('', '', '.html')); plugin.deferDeleteFile(xTmpFn);

					var _commit_infoitem=function(sSsgPath, sTitle, xDoc){
						var sPathSub='';
						var xChild=new CLocalFile(sSsgPath); xChild.append(_find_unique_id(sSsgPath));
						if(xNyf.createFolder(xChild)){
							xNyf.setFolderHint(xChild, sTitle);
							sPathSub=xChild.toString();
							if(xDoc){
								var xSsgFn=new CLocalFile(xChild); xSsgFn.append(plugin.getDefNoteFn('html'));
								xDoc.saveAs(xTmpFn, 8);
								xDoc.close();
								var nBytes=xNyf.createFile(xSsgFn, xTmpFn);
								if(nBytes<0){
									sPathSub='';
									if(!confirm('Problems importing content of outline item: '+sTitle)){
										throw ('Failed to import content of the outline item: '+sTitle);
									}
								}
							}
						}
						return sPathSub;
					};

					var xDocs=xMsw.getDocuments();
					var xDoc0, nDone=0; if(xDocs) xDoc0=xDocs.open(sSrcFn, true);
					if(xDoc0){
						//2014.1.8 xParagraph.getOutlineLevel() throws exception (#-2147352567) with documents created by xDocs.open(FN);
						//Workaround: forcedly transfer contents into another document created with xDocs.add('');
						var xDoc1=xDocs.add('');
						var xRng0=xDoc0.getRange(0, 0); xRng0.setEnd(0x7fffFFFF); xRng0.copy();
						var xRng1=xDoc1.getRange(0, 0); xRng1.paste(); xRng1.setEnd(0x7fffFFFF);
						xDoc0.close(false);
						var xParagraphs=xRng1.getParagraphs();
						var c=xParagraphs.getCount();
						var sSsgPath=sCurItem, iLevelPrev=-1, sTitle='', xDoc2=undefined, xRng2=undefined;
						for(var j=0; j<c; ++j){
							var xParagraph=xParagraphs.getItem(j+1);
							if(xParagraph){
								var xRng=xParagraph.getRange();
								if(xRng){
									var iLevel=xParagraph.getOutlineLevel();
									if(iLevel>=1 && iLevel<10){

										var sPathSub=sSsgPath;
										var sTxt=xRng.getText();

										var bContinue=plugin.ctrlProgressBar(sTxt, 1, true);
										if(!bContinue) break;

										//commit the cached content;
										if(sTitle || xDoc2){
											sPathSub=_commit_infoitem(sSsgPath, sTitle, xDoc2);
											nDone++;
										}

										//then clear the data cache;
										if(xDoc2) xDoc2.release(); xDoc2=undefined;
										if(xRng2) xRng2.release(); xRng2=undefined;

										sTitle=sTxt;

										//determine ssg path of info item by level;
										if(iLevel>iLevelPrev){
											sSsgPath=sPathSub;
										}else if(iLevel<iLevelPrev){
											var iLvl=iLevel;
											while(iLvl++<iLevelPrev){
												sSsgPath=new CLocalFile(sSsgPath).getParent();
											}
										}

										iLevelPrev=iLevel;

									}else if(iLevel>=10){
										if(!xDoc2){
											xDoc2=xDocs.add('');
											xRng2=xDoc2.getRange(0, 0);
										}
										xRng.copy();
										xRng2.collapse(0); //wdCollapseEnd(0) //getStart(xRng2.setEnd());
										xRng2.paste();
									}
									xRng.release();
								}
								xParagraph.release();
							}
						}

						if(sTitle || xDoc2){
							_commit_infoitem(sSsgPath, sTitle, xDoc2);
							nDone++;
						}

						plugin.refreshOutline(-1, sCurItem);
					}

					if(xMsw) xMsw.quit(); xMsw=undefined;

					var sMsg=_lc2('Done', 'Total [ %nDone% ] outline items successfully imported.').replace(/%nDone%/ig, nDone);
					alert(sMsg);

				}else{
					alert(_lc('p.Common.Fail.LoadMSWord', 'Failed to invoke Microsoft Word.'));
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
	if(xMsw) xMsw.quit(); xMsw=undefined;
}
