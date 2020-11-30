
//sValidation=nyfjs
//sCaption=Open externally ...
//sHint=Open the selected attachment or current text contents within the associated application
//sCategory=Context.HtmlEdit; Context.HtmlView; Context.RichEdit; Context.RichView; Context.TextEdit; Context.TextView; Context.Hyperlink
//sCondition=CURDB; OUTLINE; CURINFOITEM; CURDOC;
//sID=p.OpenExternally
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

		var sCurDocFn=plugin.argumentAt(0);

		if(!sCurDocFn){

			//pick a document from visual components by input focus;
			var sFocus=plugin.getFocusPane().toLowerCase();

			if(sFocus=='attachments'){

				var bFullPath=true, v=plugin.getSelectedAttachments(-1, bFullPath);
				if(v && v.length>0){
					//var vExts='html;htm;txt;ini;log;csv;css;js;xml;pl;php;asp;c;h;cpp;hpp;cxx;hxx;pas;cs;java;py;rb;go;erl;asm;sql;bat;sh;bas;m;mm;swift;md'.split(';');
					for(var i in v){
						var xFn=new CLocalFile(v[i]), sExt=xFn.getExtension(false).toLowerCase();
						//if(vExts.indexOf(sExt)>=0){
						if(sExt){
							sCurDocFn=xFn.toString();
							break;
						}
					}

					if(!sCurDocFn){
						sCurDocFn=v[0]; //select the first one if no matches;
					}
				}

				if(!sCurDocFn){
					//if no attachments selected, choose the currently opened document;
					sCurDocFn=plugin.getCurDocFile();
				}

				if(sCurDocFn && sCurDocFn==plugin.getCurDocFile()){
					if(plugin.isContentEditable()) plugin.commitCurrentChanges();
				}

			}else if(sFocus=='htmlview'){

				var sSsgFn=plugin.getCurDocFile(); //2016.6.1 consider of image-gallery;
				if(xNyf.fileExists(sSsgFn)){
					sCurDocFn=sSsgFn;
				}

			}else if(sFocus=='htmledit'){

				sCurDocFn=plugin.getCurDocFile();
				if(plugin.isContentEditable()) plugin.commitCurrentChanges();

			}else{

				sCurDocFn=plugin.getCurDocFile();
				if(plugin.isContentEditable()) plugin.commitCurrentChanges();

			}
		}

		if(sCurDocFn){

			var bShortcut=xNyf.isShortcut(sCurDocFn), xPeer;
			if(bShortcut){

				var sPeer=xNyf.getShortcutFile(sCurDocFn, true);
				if(sPeer){
					xPeer=new CLocalFile(sPeer);
				}

			}else{

				var sPeer=xNyf.getPeerFile(sCurDocFn), sCurDocPath=new CLocalFile(sCurDocFn).getParent();
				if(!sPeer){

					var sName;
					{
						sName=new CLocalFile(sCurDocFn).getLeafName();
						if(plugin.isReservedNoteFn(sName)){
							var sItemTitle=xNyf.getFolderHint(sCurDocPath);
							var sExt=new CLocalFile(sName).getExtension(true);
							if(sExt==".qrich") sExt='.html';
							sName=(_validate_filename(sItemTitle)||'untitled') + sExt;
						}
					}

					if(sName){
						var sTmpDir=platform.getTempFolder(), sMagic='__nyf7_external_opens', xTmpSubDir=new CLocalDir(sTmpDir, sMagic);
						if(!xTmpSubDir.exists()){
							new CLocalDir(sTmpDir).createDirectory(sMagic);
						}

						if(xTmpSubDir.exists()){
							sTmpDir=xTmpSubDir.toString();
						}

						if(sTmpDir){
							var xTmpFn=new CLocalFile(sTmpDir, sName), sTitle=xTmpFn.getTitle(), sExt=xTmpFn.getSuffix(true), i=1;
							while(xTmpFn.exists()){
								sName=sTitle+'_'+i+sExt;
								xTmpFn=new CLocalFile(sTmpDir, sName);
								i++;
							}
							sPeer=xTmpFn.toString(); platform.deferDeleteFile(sPeer);
						}
					}
				}

				if(sPeer){

					xPeer=new CLocalFile(sPeer); var sExt=xPeer.getSuffix(false).toLowerCase();

					if(xNyf.fileExists(sCurDocFn)){

						var tSsg=xNyf.getModifyTime(sCurDocFn), tPeer=0;
						if(xPeer.exists()) tPeer=xPeer.getModifyTime();
						if(tSsg>tPeer){

							var nBytes=xNyf.exportFile(sCurDocFn, xPeer.toString());
							if(nBytes>0 && (sExt=='html' || sExt=='htm')){

								{
									//2016.4.14 invoke the common functions predefined for plugins;
									var xFn=new CLocalFile(new CLocalFile(plugin.getScriptFile()).getDirectory(false), 'comutils.js');
									var sCode=xFn.loadText('auto');
									if(sCode){
										eval.call(null, sCode);
									}
								}

								var sHtml=xPeer.loadText('html');
								var sNew=substituteUrisWithinHtml(sHtml, 'img,link', function(sObj, sTagName){
									var u=sObj.toString();
									if(u.search(/(\.jpg|\.jpeg|\.gif|\.png|\.bmp)$/i)>0){
										var ba, sExt;
										if(u.search(/[:\?\*\|\/\\<>]/)<0){ //for linked objs, possibly saved in the attachments section;
											var xSsgFn=new CLocalFile(sCurDocPath, percentDecode(u));
											ba=xNyf.loadBytes(xSsgFn.toString());
											sExt=xSsgFn.getSuffix(false).toLowerCase()||'jpg';
										}else if(u.search(/^file:\/\//i)==0){ //for href objects, possibly linked to local files;
											var sFn=localFileFromUrl(u, true);
											if(sFn){
												sFn=xNyf.evalRelativePath(sFn);
												var xFn=new CLocalFile(sFn);
												if(xFn.exists()){
													ba=xFn.loadBytes();
													sExt=xFn.getSuffixe(false).toLowerCase()||'jpg';
												}
											}
										}
										if(ba && ba.size()>0){
											u='data:image/'+sExt+';base64,'+ba.toString('base64');
										}
									}else if(u.search(/(\.css)$/i)>0){
										if(u.search(/[:\?\*\|\/\\<>]/)<0){ //for linked objs, possibly saved in the attachments section;
											var sCssName=percentDecode(u);
											var xSsgFn=new CLocalFile(sCurDocPath, sCssName);
											var xCssFn=new CLocalFile(xPeer.getParent(), sCssName);
											if(!xCssFn.exists()){
												var nBytes=xNyf.exportFile(xSsgFn.toString(), xCssFn.toString());
												if(nBytes>0){
													platform.deferDeleteFile(xCssFn);
												}
											}
										}else if(u.search(/^file:\/\//i)==0){ //for href objects, possibly linked to local files;
											var sFn=localFileFromUrl(u, true);
											if(sFn){
												sFn=xNyf.evalRelativePath(sFn);
												var xFn=new CLocalFile(sFn);
												if(xFn.exists()){
													var sCssName=xFn.getLeafName();
													var xCssFn=new CLocalFile(xPeer.getParent(), sCssName);
													if(!xCssFn.exists() && xCssFn.toString()!=xFn.toString()){
														var bSucc=xFn.copyTo(xPeer.getParent(), sCssName);
														if(bSucc){
															platform.deferDeleteFile(xCssFn);
															u=percentEncode(sCssName);
														}
													}

												}
											}
										}
									}
									return u;
								});

								if(sNew!=sHtml){
									if(xPeer.saveUtf8(sNew)>0){
										xPeer.setModifyTime(tSsg);
									}
								}
							}
						}

					}else{
						//consider of new info items with no HTML contents saved;
						if(sExt=='html' || sExt=='htm'){
							var sHtml=plugin.getTextContent(-1, true)||'<html><body><div>No contents available<br /></div></body></html>';
							if(xPeer.saveUtf8(sHtml)>0){
								//xPeer.setModifyTime(new Date());
							}
						}
					}

				}
			}

			if(xPeer){
				if(xPeer.exists()){
					if(xPeer.launch()){
						if(!xNyf.isReadonly() && !bShortcut){
							plugin.watchPeerFile(-1, sCurDocFn, xPeer.toString(), true);
						}
					}
				}else{
					alert('File not found' + '\n\n' + xPeer);
				}
			}else{
				alert('Failed to retrieve the attachment file.');
			}

		}else{
			alert('No documents available to open externally.');
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
