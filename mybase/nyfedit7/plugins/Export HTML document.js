
//sValidation=nyfjs
//sCaption=Export HTML document ...
//sHint=Export current content as a .html document
////sCategory=MainMenu.Share; Context.HtmlEdit; Context.HtmlView; Context.RichEdit; Context.RichView; Context.TextEdit; Context.TextView; Context.Hyperlink
//sCategory=MainMenu.Share;
//sCondition=CURDB; OUTLINE; CURINFOITEM; CURDOC;
//sID=p.ExportHtmlContent
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

		var sCurDocFn=plugin.getCurDocFile(), sCurDocPath=plugin.getCurDocPath();
		var sExt=new CLocalFile(sCurDocFn).getSuffix(false).toLowerCase();
		var sItemTitle=xNyf.getFolderHint(sCurDocPath);

		var sName;
		if(!xNyf.folderExists(sCurDocFn)){ //consider of non-file contents e.g. image-gallery;

			var xDocFn=new CLocalFile(sCurDocFn);

			sName=xDocFn.getLeafName();
			if(plugin.isReservedNoteFn(sName)){
				sName=(_validate_filename(sItemTitle)||'untitled') + '.html';
			}else{
				var sExt=xDocFn.getSuffix(false).toLowerCase();
				if(sExt!='html'){
					sName+='.html'; //consider of non-html contents, forcedly turn into .html;
				}
			}
		}

		var sCfgKey='ExportHtmlContent.sDstFn';

		var xInitFn = new CLocalFile(localStorage.getItem(sCfgKey)||platform.getHomePath()||'', sName);

		var sDstFn=platform.getSaveFileName(
					{ sTitle: plugin.getScriptTitle()
						, sInitDir: xInitFn
						, sFilter: 'Html documents (*.html;*.htm);;All files (*.*)'
					});

		if(sDstFn){

			var xDstFn=new CLocalFile(sDstFn);
			localStorage.setItem(sCfgKey, xDstFn.getParent());

			var sHtml = plugin.getTextContent(-1, true);
			if(sHtml){

				{
					//2016.4.14 invoke the common functions predefined for plugins;
					var xFn=new CLocalFile(new CLocalFile(plugin.getScriptFile()).getDirectory(false), 'comutils.js');
					var sCode=xFn.loadText('auto');
					if(sCode){
						eval.call(null, sCode);
					}
				}

				var vBadRefs=[];
				sHtml=substituteUrisWithinHtml(sHtml, 'img,link,a', function(sObj, sTagName){
					var u=sObj.toString();
					if(u.search(/^nyf:\/\/entry\?/i)>=0){
						//2017.10.19 handle bookmarks inside the document;
						//e.g. <a href="nyf://entry?bmid=302&bmname=xxx">xxx</a>
						var t='bmid=', p=u.indexOf(t);
						if(p>0){
							var sArg=u.substr(p+t.length);
							if(sArg){
								var nBmID=parseInt(sArg), sBm;
								if(xNyf.getBookmarkByID){ //2017.10.19 the newly added API;
									sBm=xNyf.getBookmarkByID(nBmID);
								}else{
									var v=xNyf.listBookmarks().split('\n');
									for(var i in v){
										if(nBmID==parseInt(v[i]||'-1')){
											sBm=v[i];
										}
									}
								}
								if(sBm){
									var f=sBm.split('\t');
									if(f && f.length>=5){
										var iSsgPath=parseInt(f[1]), sSsgName=f[2], sAnchor=f[3], sBmName=f[4];
										var sSsgPath=xNyf.getPathByItemID(iSsgPath);
										var xSsgPath=new CLocalFile(sSsgPath); xSsgPath.append(sSsgName);
										if(sCurDocFn==xSsgPath.toString() && sAnchor){
											u='#'+sAnchor;
										}
									}
								}
							}
						}
						if(u==sObj.toString()){
							vBadRefs.push(u);
						}
					}else if(u.search(/(\.jpg|\.jpeg|\.gif|\.png|\.bmp)$/i)>0){
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
							var xCssFn=new CLocalFile(xDstFn.getParent(), sCssName);
							if(!xCssFn.exists()){
								var nBytes=xNyf.exportFile(xSsgFn.toString(), xCssFn.toString());
								if(nBytes>0){
									;
								}
							}
						}else if(u.search(/^file:\/\//i)==0){ //for href objects, possibly linked to local files;
							var sFn=localFileFromUrl(u, true);
							if(sFn){
								sFn=xNyf.evalRelativePath(sFn);
								var xFn=new CLocalFile(sFn);
								if(xFn.exists()){

									var sCssName=xFn.getLeafName();
									var xCssFn=new CLocalFile(xDstFn.getParent(), sCssName);

									//if(xCssFn.exists() && xCssFn.getModifyTime()==xFn.getModifyTime() && xCssFn.getFileSize()==xFn.getFileSize()){
									if(xCssFn.exists()){
										u=percentEncode(sCssName);
									}else if(xCssFn.toString()!=xFn.toString()){
										var bSucc=xFn.copyTo(xDstFn.getParent(), sCssName); //it may fail if the destination file exists;
										if(bSucc){
											u=percentEncode(sCssName);
										}
									}

								}
							}
						}
					}
					return u;
				});

				if(xDstFn.saveUtf8(sHtml)>0){
					var sMsg=_lc2('Done', 'Successfully exported current content and saved as a .html document. View it now?');
					sMsg+='\n\n'+xDstFn;
					//if(vBadRefs.length>0) sMsg+="\n\nBut links not working from outside the application:\n"+vBadRefs.join('\n');
					if(confirm(sMsg)){
						xDstFn.launch('');
					}
				}
			}else{
				alert(_lc2('NoTextAvail', 'No contents available to export.'));
			}
		}
	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
