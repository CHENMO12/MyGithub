
//sValidation=nyfjs
//sCaption=Export MS-Word outline ...
//sHint=Export contents to Microsoft Word outline view via OLE-Automation
//sCategory=MainMenu.Share
//sCondition=CURDB; CURINFOITEM; OUTLINE;
//sPlatform=Windows
//sID=p.ExportMSWordOutline
//sPlatform=Windows
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

		var vRange=[
			  _lc('p.Common.CurBranch', 'Current branch')
			, _lc('p.Common.CurDB', 'Current database')
			];

		var sCfgKey1='ExportMSWordOutline.iRange', sCfgKey2='ExportMSWordOutline.sDstFn', sCfgKey3='ExportMSWordOutline.bInclText';
		var vFields = [
			{sField: "savefile", sLabel: _lc2('DstFn', 'Save as MS-Word document'), sTitle: plugin.getScriptTitle(), sFilter: 'MS-Word documents (*.doc;*.docx);;All files (*.*)', sInit: localStorage.getItem(sCfgKey2)||''}
			, {sField: "combolist", sLabel: _lc('p.Common.Range', 'Range'), vItems: vRange, sInit: localStorage.getItem(sCfgKey1)||''}
			, {sField: "checkbox", sLabel: '', vItems: [(localStorage.getItem(sCfgKey3)||'')+'|'+_lc2('TxtContent', 'Include text content')]}
		];

		var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 500, vMargins: [2, 0, 30, 0], bVert: true});
		if(vRes && vRes.length==3){

			var sDstFn=vRes[0], iRange=vRes[1], vOpts=vRes[2];
			if(iRange>=0 && sDstFn && vOpts && vOpts.length>0){

				var bCurBranch=(iRange==0);
				var bInclContents=vOpts[0];

				localStorage.setItem(sCfgKey1, iRange);
				localStorage.setItem(sCfgKey2, sDstFn);
				localStorage.setItem(sCfgKey3, bInclContents);

				var xMsw=new CAppWord();
				if(xMsw && xMsw.init()){

					//2011.8.7 Set it visible, in case users press ESC and select No to continue without losing connection with MSWord;
					xMsw.setVisible(true);

					var xDocs=xMsw.getDocuments();
					var xDoc; if(xDocs) xDoc=xDocs.add('');
					if(xDoc){

						var sCurItem=plugin.getCurInfoItem(-1), sDefHtmlNoteFn=plugin.getDefNoteFn();

						if(!sCurItem || !bCurBranch){
							sCurItem=plugin.getDefRootContainer();
							bCurBranch=false;
						}

						var nFolders=0, iLastLvl=0, xRng=xDoc.getRange(0, 0), bAbort=false;

						xNyf.traverseOutline(sCurItem, true, function(){
							nFolders++;
						});

						plugin.initProgressRange(plugin.getScriptTitle(), nFolders);

						//var vImgFileTypes='bmp|jpg|jpeg|png|gif|tif'.split('|');

						var _act_on_item=function(sSsgPath, iLevel){
							var iBakLvl=iLevel;
							if(xNyf.folderExists(sSsgPath)){

								var sTitle=xNyf.getFolderHint(sSsgPath); if(!sTitle) sTitle='Untitled';

								var bContinue=plugin.ctrlProgressBar(sTitle, 1, true);
								if(!bContinue) return (bAbort=true);

								//xRng.setStart(xRng.getStoryLength());

								//xRng.setStart(xRng.getEnd());
								//xRng.setText('\n');

								xRng.setStart(xRng.getEnd());
								xRng.setText(sTitle+'\n');

								var xPars=xRng.getParagraphs();
								if(xPars){
									if(iLevel == iLastLvl){
										xPars.outlinePromote();
									}else if(iLevel < iLastLvl){
										while(iLevel++ <= iLastLvl) xPars.outlinePromote();
									}else if(iLevel > iLastLvl){
										xPars.outlineDemote();
									}
								}

								if(xPars) xPars.release();

								xRng.setStart(xRng.getEnd());
								if(bInclContents){
									var sPreferred=xNyf.detectPreferredFile(sSsgPath, "html;htm;qrich;txt;md;rtf>ini;log");
									if(sPreferred){
										var xSsgFn=new CLocalFile(sSsgPath, sPreferred);
										var sExt=xSsgFn.getSuffix(false), sExt2=sExt; if(sExt2.search(/^(md|qrich)$/i)==0) sExt2+='.html';
										var xTmpFn=new CLocalFile(platform.getTempFile('', '', sExt2)); plugin.deferDeleteFile(xTmpFn);
										if(xNyf.exportFile(xSsgFn, xTmpFn)>0){
											var vFilesToDel=[];
											if(sExt=='md'){

												var s0=xTmpFn.loadText('auto'), s=s0;
												s=platform.convertMarkdownToHtml(s);

												var v=s.split('\n');
												for(var i=0; i<v.length; ++i){
													var sLine=v[i];

													//2018.1.12 MS-Word outline recognize <h[1-9] ...> in HTML as outline titles;
													sLine=sLine.replace(/<h[1-9]\s+[^>]*>/i, "<p style='font-size: medium; font-weight: bold;'>");
													sLine=sLine.replace(/<\/h[1-9]>/i, '</p>');

													v[i]=sLine;
												}
												s=v.join('\n');

												if(s!=s0) xTmpFn.saveUtf8(s);

											}else if(sExt=='qrich'){

												//2018.1.12 the rich-text contains spaces/tabs that are not recognized by msword;
												//<p style="margin:0px;"><span style="font-family:'Courier'; font-size:13pt;">    abc	def    xyz</span></p>
												var s0=xTmpFn.loadText('auto'), s=s0;

												var v=s.split('\n');
												for(var i=0; i<v.length; ++i){
													var sLine=v[i];
													sLine=sLine.replace(/(<span\s+[^>]*>)(.*)(<\/span>)/ig, function(m0, m1, m2, m3){
														m2=m2.replace(/  /g, '&nbsp; ');
														m2=m2.replace(/\t/g, '&nbsp; &nbsp; &nbsp; &nbsp; ');
														return m1+m2+m3;
													});

													if(sLine=='p, li { white-space: pre-wrap; }') sLine='';
													v[i]=sLine;
												}
												s=v.join('\n');

												if(s!=s0) xTmpFn.saveUtf8(s);

											}else if(sExt=='html' || sExt=='htm'){

												var sHtml=xTmpFn.loadText('auto');
												if(sHtml){

//													var vFiles=xNyf.listFiles(sSsgPath);
//													for(var i in vFiles){
//														var xImgFn=new CLocalFile(sSsgPath); xImgFn.append(vFiles[i]);
//														var sExt=xImgFn.getExtension(false).toLowerCase();
//														if(vImgFileTypes.indexOf(sExt)>=0){
//															if(sHtml.indexOf(vFiles[i])>0){
//																var xTmpFn2=new CLocalFile(platform.getTempFolder()); xTmpFn2.append(vFiles[i]);
//																if(xNyf.exportFile(xImgFn, xTmpFn2)>0){
//																	vFilesToDel.push(xTmpFn2);
//																}
//															}
//														}
//													}

													//2015.5.11 msword 'insertFile' doesn't recognize this tag (geneated by msword itself);
													var sTmp=sHtml.replace(/<\!\[if\s\!supportEmptyParas\]>&nbsp;<\!\[endif\]><o\:p><\/o\:p>/g, '&nbsp;');
													if(sTmp!=sHtml){
														if(sTmp.indexOf('<meta http-equiv=Content-Type content="text/html; charset=UTF-8">')>0){
															xTmpFn.saveUtf8(sTmp);
														}else{
															xTmpFn.saveAnsi(sTmp);
														}
													}
												}
											}

											//msword dones't insert image data, but only with links preserved;
											xRng.insertFile(xTmpFn);

//											for(var i in vFilesToDel){
//												vFilesToDel[i].remove();
//											}
										}
										xTmpFn.remove();
									}
								}

								xRng.setStart(xRng.getStoryLength());
								xRng.setText('\n');

								iLastLvl=iBakLvl;
							}
						};

						xNyf.traverseOutline(sCurItem, bCurBranch, _act_on_item);

						if(!bAbort){
							xDoc.getActiveWindow().getActivePane().getView().setType(2);
							xDoc.saveAs(sDstFn);
						}

						if(xDocs) xDocs.release();
						if(xRng) xRng.release();
					}

					if(xMsw) xMsw.quit(); xMsw=undefined;

					if(!bAbort){
						sMsg=_lc2('Done', 'Successfully generated the outline view within MS-Word. Open it now?');
						if(confirm(sMsg+'\n\n'+sDstFn)){
							new CLocalFile(sDstFn).exec();
						}else{
						}
					}
				}else{
					alert(_lc('p.Common.Fail.LoadMSWord', 'Failed to invoke Microsoft Word.'));
				}
			}else{
				alert('Bad input of destination file path.');
			}
		}
	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
	if(xMsw) xMsw.quit(); xMsw=undefined;
}
