
//sValidation=nyfjs
//sCaption=Copy selected Html contents
//sHint=Copy selected HTML content to clipboard with images cached in TEMP folder
//sCategory=
//sCondition=CURDB; DBRW; OUTLINE; CURINFOITEM
//sID=p.CopySelHtml
//sAppVerMin=7.0
//sAuthor=wjjsoft

/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2016 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

var _lc=function(sTag, sDef){return plugin.getLocaleMsg(sTag, sDef);};
var _lc2=function(sTag, sDef){return _lc(plugin.getLocaleID()+'.'+sTag, sDef);};

var _trim=function(s){return (s||'').replace(/^\s+|\s+$/g, '');};
var _trim_cr=function(s){return (s||'').replace(/\r+$/g, '');};

var g_bPutImagesInTmpDir=false;

try{

	var xNyf=new CNyfDb(-1);
	if(xNyf.isOpen()){

		{
			//2016.4.14 invoke the common functions predefined for plugins;
			var xFn=new CLocalFile(new CLocalFile(plugin.getScriptFile()).getDirectory(false), 'comutils.js');
			var sCode=xFn.loadText('auto');
			if(sCode){
				eval.call(null, sCode);
			}
		}

		if(g_bPutImagesInTmpDir){
			var sTmpDir=platform.getTempFolder();
			var sImgDirName='__nyf7_clip_images';
			var xImgDir=new CLocalDir(sTmpDir, sImgDirName);

			if(xImgDir.exists()){
				var vFiles=xImgDir.listFiles();
				for(var i in vFiles){
					var xImgFn=new CLocalFile(xImgDir.toString(), vFiles[i]);
					xImgFn.remove();
				}
			}else{
				var tmp=new CLocalDir(sTmpDir);
				tmp.createDirectory(sImgDirName);
			}
		}

		var sCurDocPath=plugin.getCurInfoItem();
		if(sCurDocPath){
			var sHtml=plugin.getSelectedText(-1, true), sTxt=plugin.getSelectedText(-1, false);
			{
				plugin.initProgressRange(plugin.getScriptTitle(), 0);

				sHtml=substituteUrisWithinHtml(sHtml, 'img,link', function(sObj, sTagName){
					var u=sObj.toString();

					var bContinue=plugin.ctrlProgressBar(u, 1, true);
					if(!bContinue) throw 'User abort by the Esc key';

//					var m=u.match(/(data:image\/)(gif|jpg|png|bmp|tif)(;base64,)/i);
//					if(m && m[1] && m[2] && m[3]){

//						var sExt=m[2], sDat=u.replace(m[0], ''), sTmpFn=platform.getTempFile(xImgDir.toString(), 'image_', sExt);
//						var ba=new CByteArray(sDat, 'base64');
//						var nBytes=ba.saveToFile(sTmpFn);
//						if(nBytes>0){
//							platform.deferDeleteFile(sTmpFn);
//							u=urlFromLocalFile(sTmpFn);
//						}

//					//}else if(u.search(/[\/\\]/)<0){
//					}else if(u.search(/[:\?\*\|\/\\<>]/)<0){ //for linked objs, possibly saved in the attachments section;

//						var xSsgFn=new CLocalFile(sCurDocPath, percentDecode(u));
//						if(xNyf.fileExists(xSsgFn) && xImgDir.exists()){
//							var sLeaf=xSsgFn.getLeafName();
//							if(sLeaf){
//								var sTmpFn=new CLocalFile(xImgDir.toString(), sLeaf);
//								var nBytes=xNyf.exportFile(xSsgFn.toString(), sTmpFn.toString());
//								if(nBytes>0){
//									platform.deferDeleteFile(sTmpFn);
//									u=urlFromLocalFile(sTmpFn);
//								}
//							}
//						}
//					}

					if(g_bPutImagesInTmpDir){
						//attempts to put all embedded images into the temp folder;
						var m=u.match(/(data:image\/)(gif|jpg|png|bmp|tif|svg)(;base64,)/i);
						if(m && m[1] && m[2] && m[3]){

							var sExt=m[2], sDat=u.replace(m[0], ''), sTmpFn=platform.getTempFile(xImgDir.toString(), 'image_', sExt);
							var ba=new CByteArray(sDat, 'base64');
							var nBytes=ba.saveToFile(sTmpFn);
							if(nBytes>0){
								platform.deferDeleteFile(sTmpFn);
								u=urlFromLocalFile(sTmpFn);
								//log('==>' + u);
							}

						//}else if(u.search(/[\/\\]/)<0){
						}else if(u.search(/[:\?\*\|\/\\<>]/)<0){ //for linked objs, possibly saved in the attachments section;

							var xSsgFn=new CLocalFile(sCurDocPath, percentDecode(u));
							if(xNyf.fileExists(xSsgFn) && xImgDir.exists()){
								var sLeaf=xSsgFn.getLeafName();
								if(sLeaf){
									var sTmpFn=new CLocalFile(xImgDir.toString(), sLeaf);
									var nBytes=xNyf.exportFile(xSsgFn.toString(), sTmpFn.toString());
									if(nBytes>0){
										platform.deferDeleteFile(sTmpFn);
										u=urlFromLocalFile(sTmpFn);
									}
								}
							}
						}
					}else{
						//2019.1.22 attempt to embed all images into HTML in BASE64
						if(u.search(/[:\?\*\|\/\\<>]/)<0){ //for linked objs, possibly saved in the attachments section;
							if(u.search(/\.(png|jpg|jpeg|gif|svg|bmp|tif)$/i)>0){
								var xSsgFn=new CLocalFile(sCurDocPath, percentDecode(u));
								var sExt=xSsgFn.getSuffix(false).toLowerCase();
								if(xNyf.fileExists(xSsgFn)){
									var v=xNyf.loadBytes(xSsgFn.toString());
									if(v.size()>0){
										u='data:image/%TYPE%;base64,'.replace(/%TYPE%/gi, sExt) + v.base64();
										//log('==>' + u);
									}
								}
							}
						}
					}

					return u;
				});

				plugin.destroyProgressBar();
			}

			var vUrls=[]; //2016.5.8 ignore urls, as on pasting it has higher priority than HTML/TEXT;
			{
//				substituteUrisWithinHtml(sHtml, 'a', function(sObj, sTagName){
//					var u=sObj.toString();
//					if(vUrls.indexOf(u)<0) vUrls.push(u);
//					return u;
//				});
			}

			var sDataType='', vMimeData=[];
			{
				if(sHtml){
					if(sDataType) sDataType+=',';
					sDataType+='html';
					vMimeData.push(sHtml);
				}
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
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}

}catch(e){
	alert(e);
}
