
//sValidation=nyfjs
//sCaption=Export HTML tree ...
//sHint=Export content as webpages with an HTML tree navigation
//sCategory=MainMenu.Share
//sCondition=CURDB; CURINFOITEM; OUTLINE
//sID=p.ExportHtmlTree
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
var _trim_l=function(s){return (s||'').replace(/^\s+/g, '');};
var _trim_r=function(s){return (s||'').replace(/\s+$/g, '');};
var _trim_cr=function(s){return (s||'').replace(/\r+$/g, '');};

var _html_encode=function(s)
{
	//http://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
	s=s.replace(/&/g,	'&amp;');
	s=s.replace(/</g,	'&lt;');
	s=s.replace(/>/g,	'&gt;');
	s=s.replace(/\"/g,	'&quot;');
	s=s.replace(/\'/g,	'&apos;');
	s=s.replace(/\xA0/g,	'&nbsp;'); //http://www.fileformat.info/info/unicode/char/a0/index.htm
	s=s.replace(/  /g,	'&nbsp; ');
	s=s.replace(/\t/g,	'&nbsp; &nbsp; &nbsp; &nbsp; '); //&emsp;
	//and more ...
	return s;
};

var _html_decode=function(s)
{
	s=s.replace(/&lt;/g,		'<');
	s=s.replace(/&gt;/g,		'>');
	s=s.replace(/&quot;/g,		'"');
	s=s.replace(/&apos;/g,		'\'');
	s=s.replace(/&nbsp;/g,		' ');
	s=s.replace(/&circ;/g,		'^');
	s=s.replace(/&tilde;/g,		'~');
	//and more ...
	s=s.replace(/&amp;/g,		'&');
	return s;
};

var _pack_array=function(v, xPred){
	var vTmp=[];
	for(var i=0; i < v.length; ++i){
		var bDel=false, val=v[i];
		if(typeof(xPred)=='function'){
			bDel=xPred(i, val);
		}else{
			bDel=xPred ? (val==xPred) : (!val);
		}
		if(!bDel){
			vTmp[vTmp.length]=val;
		}
	}
	return vTmp;
};

var _compare_array=function(v1, v2)
{
	var iRes=0;
	if(v1.length>v2.length){
		iRes=1;
	}else if(v1.length<v2.length){
		iRes=-1;
	}else{
		for(var i=0; i < v1.length; ++i){
			if(v1[i]>v2[i]){
				iRes=1;
				break;
			}else if(v1[i]<v2[i]){
				iRes=-1;
				break;
			}else{
			}
		}
	}
	return iRes;
};

try{

	var xNyf=new CNyfDb(-1);
	if(xNyf.isOpen()){

		if(plugin.isContentEditable()) plugin.commitCurrentChanges();

		var vRange=[
			  _lc('p.Common.CurBranch', 'Current branch')
			, _lc('p.Common.CurDB', 'Current database')
		];

		var sCfgKey1='ExportHtmlTree.sDir', sCfgKey2='ExportHtmlTree.iRange';
		var vFields = [
			{sField: "folder", sLabel: _lc2('DstPath', 'Destination folder'), sTitle: plugin.getScriptTitle(), sInit: localStorage.getItem(sCfgKey1)||''}
			, {sField: "combolist", sLabel: _lc('p.Common.Range', 'Range'), vItems: vRange, sInit: localStorage.getItem(sCfgKey2)||'0'}
		];

		var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 500, vMargins: [2, 0, 50, 0], bVert: true});
		if(vRes && vRes.length==2){

			var sDstDir=vRes[0], iRange=vRes[1], bOverwriteAlways=false;
			if(sDstDir && iRange>=0){

				localStorage.setItem(sCfgKey1, sDstDir);
				localStorage.setItem(sCfgKey2, iRange);

				var bCurBranch=(iRange==0);
				var sCurItem=bCurBranch ? plugin.getCurInfoItem(-1) : plugin.getDefRootContainer();
				var sTitle=bCurBranch ? xNyf.getFolderHint(sCurItem) : xNyf.getDbTitle();

				{
					//2016.4.14 invoke the common functions predefined for plugins;
					var xFn=new CLocalFile(new CLocalFile(plugin.getScriptFile()).getDirectory(false), 'comutils.js');
					var sCode=xFn.loadText('auto');
					if(sCode){
						eval.call(null, sCode);
					}
				}

				{
					//copy static files to the destination folder;
					var xNames={
						'jquery.js': 'jquery-1.5.min.js'
						, 'index.html': '_htmltree_index.html'
						, 'nav.html': '_htmltree_navpane.html'
						, 'itemlink.js': '_htmltree_itemlink.html' //2013.3.27 to enable item-links nyf://entry?...
						, 'icon_plus.gif': 'icon_plus.gif'
						, 'icon_minus.gif': 'icon_minus.gif'
						, 'icon_itemlink.gif': 'icon_itemlink.gif'
						, 'icon_attachment.gif': 'icon_attachment.gif'
						, 'icon_newwin.gif': 'icon_newwin.gif'
						, 'icon_jump.gif': 'icon_jump.gif'
						, 'icon_email.gif': 'icon_email.gif'
					};
					var sPathSrc=new CLocalFile(plugin.getScriptFile()).getDirectory(); var sMissing='';
					for(var sFn in xNames){
						var sNameDst=xNames[sFn];
						var xSrc=new CLocalFile(sPathSrc); xSrc.append(sNameDst);
						if(xSrc.exists()){
							var xDst=new CLocalFile(sDstDir); xDst.append(sFn);
							if('gif;jpg;png'.split(';').indexOf(xSrc.getExtension(false).toLowerCase())>=0){
								xSrc.copyTo(sDstDir, sFn);
							}else{
								var s=xSrc.loadText('auto').replace(/\n/g, '\r\n');
								if(xSrc.getExtension(false).toLowerCase()=='html'){
									s=s.replace(/%DbTitle%/g, sTitle);
								}
								xDst.saveUtf8(s);
							}
						}else{
							if(sMissing) sMissing+='\n'; sMissing+=xSrc;
						}
					}
					if(sMissing){
						alert('The following files are missing. You may need to re-install the software.'+'\n\n'+sMissing);
					}
				}

				var _validate_filename=function(s){
					s=s||'';
					s=s.replace(/[\*\?\.\(\)\[\]\{\}\<\>\\\/\!\$\^\&\+\|,;:\"\'`~@#]/g, ' ');
					s=s.replace(/\s{2,}/g, ' ');
					s=_trim(s);
					if(s.length>64) s=s.substr(0, 64);
					s=_trim(s);
					s=s.replace(/\s/g, '_');
					return s;
				};

				var _xNameCache={}, _xHashUsed={};
				var _hash_name=function(s1, s2, sExt, sTag){
					var sName='', k=s1+'/'+s2;
					sName=_xNameCache[k];
					if(!sName){
						var i=0;
						do{
							//2011.2.8 make signed integers into unsigned by using the operator 'n>>>0';
							sName=(adler32(s1)>>>0).toString(16).toLowerCase();
							if(s2) sName+='_'+(adler32(s2)>>>0).toString(16).toLowerCase();
							sName+=('_'+i);
							sName+=('.'+sExt.replace(/^\.+/, ''));
							i++;
						}while(_xHashUsed[sName]);
						//2013.11.2 push the name into cache in case of hash conflicts;
						_xHashUsed[sName]=1;
						_xNameCache[k]=sName;
					}
					return sName;
				};

				var _isModified=function(sSsgFn, sWinFn){
					if(bOverwriteAlways) return true;
					var xWinFn=new CLocalFile(sWinFn), t1=xNyf.getModifyTime(sSsgFn), bUpd=true;
					if(xWinFn.exists()){
						var t2=xWinFn.getModifyTime();
						bUpd=t1>t2;
					}
					return bUpd;
				}

				plugin.initProgressRange(plugin.getScriptTitle());

				var sCss='table{border: 1px solid gray;} td{border: 1px dotted gray;} '
					+ 'p{margin: 3px 0 3px 0; padding: 0;} '
					+ '#ID_Footer{font-size: small; font-style: italic;} '
					+ 'a{padding-right: 20px; background: URL(./icon_newwin.gif) no-repeat center right;} '
					+ 'a[href ^= "mailto:"]{padding: 0 20px 0 0; background: URL(./icon_email.gif) no-repeat center right;} '
					+ 'a[href ^= "nyf:"]{padding: 0 20px 0 0; background: URL(./icon_jump.gif) no-repeat center right;} '
					;

				//2013.3.27 enable item links to work;
				var xIDofPath={}, xPathOfID={}, xIDofDoc={};
				{
					var vLines=xNyf.listItemIDs().split('\r\n');
					for(var i in vLines){
						var v=vLines[i].split('\t');
						if(v.length==2){
							var sID=v[0], sPath=v[1];
							if(sID && sPath){
								xIDofPath[sID]=sPath;
								xPathOfID[sPath]=sID;
							}
						}
					}
				}

				//2013.3.29 enable bookmarks to work;
				var xIDofBkmk={};
				{
					var vLines=xNyf.listBookmarks().split('\r\n');
					for(var i in vLines){
						var v=vLines[i].split('\t');
						if(v.length>=2){
							//var sBkmkID=v[0], sPath=v[1], sItemID=v[2];
							var sBkmkID=v[0], sItemID=v[1], sSsgName=v[2], sAnchor=v[3]; //2017.10.21 new data format;
							if(sBkmkID && sItemID){
								xIDofBkmk[sBkmkID]=sItemID + '\t' + sSsgName + '\t' + sAnchor;
							}
						}
					}
				}

				var _remove_scripts=function(sHtml){
					//2016.5.17 QRegExp doesn't work well with multi-line, so <\t> acts as a temporary substitution of '\n';
					sHtml=(sHtml||'').replace(/\r/igm, '').replace(/\n/igm, '<\t>');
					sHtml=sHtml.replace(/<script\b.*?>.*?<\/script>/igm, '');
					sHtml=sHtml.replace(/<\t>/igm, '\n');
					return sHtml;
				};

				var _install_script=function(sHtml, vJsFn){
					var sRes=sHtml;
					var p=sHtml.indexOf('</body>'); if(p<0) p=sHtml.indexOf('</head>');
					if(p>=0){
						sRes=sHtml.substr(0, p);
						for(var i in vJsFn){
							sRes+= '\n<script type="text/javascript" language="javascript" src="'+vJsFn[i]+'"></script>';
						}
						sRes+= sHtml.substr(p);
					}
					return sRes;
				};

				var _add_attachment_list=function(sHtml, vAttach){
					var sRes=sHtml;
					if(vAttach.length>0){
						var p=sHtml.indexOf('</body>'); //if(p<0) p=sHtml.indexOf('</head>');
						if(p>=0){
							sRes=sHtml.substr(0, p);
							var sStyle=''; //'position:fixed;bottom:0px;width:100%;';
							var sList='\n<footer style="%STYLE%">\n<hr noshade>'.replace(/%STYLE%/gi, sStyle);
							for(var i in vAttach){
								var d=vAttach[i];
								sList+='\n<a href="%sDstName%" title="%sDstName%" target=_blank style="padding-left: 1em; background: URL(icon_attachment.gif) no-repeat center left; padding: 0 0 0 16px;">%sSrcName%</a>'
									.replace(/%sDstName%/ig, d.sDstName)
									.replace(/%sSrcName%/ig, _html_encode(d.sSrcName))
									;
							}
							sList+='\n<hr noshade>\n</footer>';
							sRes+=sList;
						}
						sRes+= sHtml.substr(p);
					}
					return sRes;
				};

				var _idOfSsgPath=function(sSsgPath){
					var sID;
					{
						var v=sSsgPath.toString().replace(/\\/g, '/').split('/'), s='';
						for(var i in v){
							if(v[i]){
								s+='/';
								s+=v[i];
							}
						}
						if(s){
							s+='/';
							sID=xPathOfID[s];
						}
					}
					return sID;
				};

				var nDone=0, vInfoItems=[], vLocalFiles={}, vFails=[];
				var _act_on_treeitem=function(sSsgPath, iLevel){

					var xLI={}, sTitle=xNyf.getFolderHint(sSsgPath);

					var bContinue=plugin.ctrlProgressBar(sTitle||'Untitled', 1, true);
					if(!bContinue) return true;

					xLI['sSsgPath']=sSsgPath;
					xLI['sTitle']=sTitle;
					xLI['iLevel']=iLevel;
					xLI['sHref']='';
					xLI['vFiles']=[];
					xLI['nSub']=xNyf.getFolderCount(sSsgPath);
					xLI['nID']=xNyf.getItemIDByPath(sSsgPath, false)

					var xPath=new CLocalFile(sSsgPath); xPath.append('/');
					var sID=_idOfSsgPath(xPath.toString()); //xPathOfID[xPath.toString()];

					var sRel='', vRel=xNyf.listRelated(sSsgPath);
					for(var i in vRel){
						var nID=xNyf.getItemIDByPath(vRel[i], false);
						if(nID>=0){
							if(sRel) sRel+=';';
							sRel+=nID;
						}
					}
					xLI['sRelated']=sRel;

					var sDefNoteFn=xNyf.detectPreferredFile(sSsgPath, 'html;htm;qrich;md;txt;rtf>jpg;png;gif;bmp;svg');

					//export attached files;
					var vFiles=xNyf.listFiles(sSsgPath), vAttach=[];
					for(var i in vFiles){
						var sName=vFiles[i];
						if(sName!=sDefNoteFn){
							var xSrc=new CLocalFile(sSsgPath, sName);
							if(!xNyf.isShortcut(xSrc)){
								//if('gif;jpg;jpeg;png;bmp;css'.split(';').indexOf(xSrc.getExtension(false).toLowerCase())>=0)
								{
									var sDstName=_hash_name(sSsgPath, sName, xSrc.getExtension(false), 'Attachment');
									var xDst=new CLocalFile(sDstDir); xDst.append(sDstName);
									if(_isModified(xSrc, xDst)){
										if(xNyf.exportFile(xSrc, xDst)<0){
											sName='';
										}
									}
									if(sName){
										var v=xLI['vFiles']; v[v.length]=sName;
										vAttach.push({sSsgPath: sSsgPath, sSrcName: sName, sDstName: sDstName, nSize: 0});
									}
								}
							}
						}
					}

					var sHtml0='', sHtml='', xDst;
					if(sDefNoteFn){
						var xSrc=new CLocalFile(sSsgPath, sDefNoteFn);
						if(!xNyf.isShortcut(xSrc)){
							var sExt=xSrc.getExtension(false).toLowerCase();
							var sName=_hash_name(sSsgPath, sTitle||'Untitled', sExt, 'defnote'); if(sExt.search(/^(rtf|md|qrich|txt)$/i)==0) sName+='.html';
							xDst=new CLocalFile(sDstDir, sName);
							if(_isModified(xSrc, xDst) && xNyf.exportFile(xSrc, xDst)>=0){
								if(sExt.search(/^(html|htm|qrich|md|txt|rtf)$/i)==0){
									sHtml0=xDst.loadText('auto');
									sHtml=sHtml0;
									if(sExt=='rtf'){
										sHtml=platform.convertRtfToHtml(sHtml
											, {bInner: false
											, bPicture: true
											, sImgDir: sDstDir
											, sTitle: sTitle
											//, sFooter: (plugin.isAppLicensed() ? '' : 'Generated with myBase/HtmlTree Converter by Wjj Software')
											, sFooter: (plugin.isAppLicensed() ? '' : '%MYBASE-HTMLTREE-MAKER%')
											, sStyle: sCss
											, sJsFiles: 'jquery.js;itemlink.js'
											}
										);
										sHtml=sHtml.replace('%MYBASE-HTMLTREE-MAKER%', 'Generated with <a href="http://www.wjjsoft.com/mybase#htmltree" target="_blank">myBase/HtmlTree Maker</a> by <a href="http://www.wjjsoft.com/#htmltree" target="_blank">Wjj Software</a>');
									}else if(sExt=='md'){
										sHtml=platform.convertMarkdownToHtml(sHtml);
									}else if(sExt=='txt'){
										sHtml=('<!DOCTYPE html>'
												+ '<html>'
												+ '<head>'
												+ '<style>body,pre{font-family: sans-serif;}</style>'
												+ '</head>'
												+ '<body>'
												+ '<article><pre>%TEXT_CONTENT%</pre></article>'
												+ '</body></html>')
												.replace(/%TEXT_CONTENT%/g, sHtml)
										;
									}else{
										sHtml=_remove_scripts(sHtml); //get rid of scripts from random html documents;
									}
								}
							}
							xLI['sHref']=sName;
							if(sID) xIDofDoc[sID]=sName;
						}
					}else{
						//2018.4.4 make a default page for listing attachments if any;
						if(xLI['vFiles'].length>0){
							//<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
							//<html xmlns="http://www.w3.org/1999/xhtml">
							sHtml='<!DOCTYPE html>'
									+ '<html>'
									+ '<head>'
									+ '<style>body,pre{font-family:system, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "Helvetica", "Arial", "sans-serif";}</style>'
									+ '</head>'
									+ '<body>'
									//+ '<p>No text content but the following attachments available.</p>'
									+ '</body></html>'
							;
							var sName=_hash_name(sSsgPath, sTitle||'Untitled', 'html', 'placeholder');
							xDst=new CLocalFile(sDstDir, sName);
							xLI['sHref']=sName;
							if(sID) xIDofDoc[sID]=sName;
						}
					}

					if(sHtml && xDst){
						sHtml=substituteUrisWithinHtml(sHtml, 'img,link,a,script', function(sObj, sTagName){
							var u=sObj.toString();
							if(u.search(/\.(jpg|jpeg|gif|png|bmp|svg|swf|css|js)$/i)>0){
								if(u.search(/[:\?\*\|\/\\<>]/)<0){ //for linked objs, possibly saved in the attachments section;
									var xObjSrc=new CLocalFile(sSsgPath);
									xObjSrc.append(percentDecode(u)); //2016.5.8 percentDecoding is required;
									if(xNyf.fileExists(xObjSrc)){ //2018.4.4 prevent from producing zero-sized image files;
										var sExt2=xObjSrc.getExtension(false)||'';
										if(sExt2 && sExt2.length<8){
											var sObjWinName=_hash_name(sSsgPath, u, sExt2, 'linked-img');
											var xObjDst=new CLocalFile(sDstDir, sObjWinName);
											if(_isModified(xObjSrc, xObjDst)){
												if(xNyf.exportFile(xObjSrc, xObjDst)>=0){
													u=sObjWinName;
												}
											}else{
												u=sObjWinName; //already existing with no changes;
											}
										}
									}
								}else if(u.search(/^file:\/\//i)==0){ //for href objects, possibly linked to local files;
									var sFn=localFileFromUrl(u, true);
									if(sFn){
										sFn=xNyf.evalRelativePath(sFn);
										var sDiskFn=vLocalFiles[sFn];
										if(sDiskFn){
											u=sDiskFn; //the file already exported from in previous other items;
										}else{
											var xFn=new CLocalFile(sFn);
											if(xFn.exists()){
												var sExt2=xFn.getExtension(false)||'';
												if(sExt2 && sExt2.length<8){
													var sObjWinName=_hash_name(xFn.getDirectory(false), xFn.getLeafName(), sExt2, 'file-link');
													var xObjDst=new CLocalFile(sDstDir); xObjDst.append(sObjWinName);
													if(xFn.copyTo(sDstDir, sObjWinName)>=0){
														u=sObjWinName;
														vLocalFiles[sFn]=sObjWinName;
													}
												}
											}
										}
									}
								}
							}else if(u.search(/^file:\/\//i)==0){ //consider evaluation of file links with relative paths; e.g. file:///${xxx}/...
								var sFn=localFileFromUrl(u, true);
								if(sFn){
									sFn=xNyf.evalRelativePath(sFn);
									if(sFn){
										u=urlFromLocalFile(sFn, true);
									}
								}
							}
							return u;
						});

						sHtml=_add_attachment_list(sHtml, vAttach);
						sHtml=_install_script(sHtml, 'jquery.js;itemlink.js'.split(';'));

						if(xDst && sHtml!=sHtml0){
							xDst.saveUtf8(sHtml);
						}
					}

					vInfoItems[vInfoItems.length]=xLI;

				};

				xNyf.traverseOutline(sCurItem, bCurBranch, _act_on_treeitem);

				if(vInfoItems.length>0){
					var sHtm='';
					for(var j in vInfoItems){
						var xLI=vInfoItems[j];

						var sAttach='';
						for(var i in xLI.vFiles){
							if(sAttach) sAttach+=';';
							sAttach+=xLI.vFiles[i];
						}

						if(sHtm) sHtm+='\r\n';

						var sID=xLI.nID>=0 ? xLI.nID : '', sSub=xLI.nSub>0 ? xLI.nSub : '';

						sHtm+='\t<li';
						sHtm+=' level=\"'+xLI.iLevel+'\"';
						if(sSub) sHtm+=' sub=\"'+sSub+'\"';
						if(sID) sHtm+=' id=\"'+sID+'\"';
						if(xLI.sRelated) sHtm+=' related=\"'+(xLI.sRelated||'')+'\"';
						if(xLI.sHref) sHtm+=' href=\"'+(xLI.sHref||'')+'\"';
						if(sAttach) sHtm+=' attach=\"'+sAttach+'\"';
						sHtm+='>';
						sHtm+=_html_encode(xLI.sTitle);
						sHtm+='</li>';
					}

					if(sHtm){
						var xFn=new CLocalFile(sDstDir); xFn.append('nav.html');
						var sHtml=xFn.loadText('html').replace(/\n/g, '\r\n');
						xFn.saveUtf8(sHtml.replace(/%InfoItems%/, sHtm));
					}

					//2013.3.27 export IDs of info items, so the item link can work within web pages.
					var xFn=new CLocalFile(sDstDir); xFn.append('itemlink.js');
					var sTxt=xFn.loadText('auto').replace(/\n/g, '\r\n');
					if(sTxt){
						//for item links;
						{
							var sTmp='';
							for(var sID in xIDofDoc){
								if(sTmp) sTmp+='\r\n\t, ';
								sTmp+='"'+sID+'": ';
								sTmp+='"'+xIDofDoc[sID]+'"';
							}
							sTmp='{'+sTmp+'}';
							sTxt=sTxt.replace(/%xItemIDs%/gi, sTmp);
						}
						//for bookmark links;
						{
							var sTmp='';
							for(var sBkmkID in xIDofBkmk){
								if(sTmp) sTmp+='\r\n\t, ';
								sTmp+='"'+sBkmkID+'": ';
								sTmp+='"'+xIDofBkmk[sBkmkID]+'"';
							}
							sTmp='{'+sTmp+'}';
							sTxt=sTxt.replace(/%xBkmkIDs%/gi, sTmp);
						}
						xFn.saveUtf8(sTxt);
					}

					if(confirm(_lc2('Done', 'The HTML tree successfully generated. View it now?'))){
						var xStartPage=new CLocalFile(sDstDir); xStartPage.append('index.html');
						xStartPage.launch();
					}
				}
			}else{
				alert('Bad input of directory or range');
			}
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
