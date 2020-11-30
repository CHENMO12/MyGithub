
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function curImage()
{
	var _is_image=function(e){
		var bImg=false;
		if(e && e.nodeType == Node.ELEMENT_NODE){
			if(e.nodeName.toLowerCase()=='img'){
				bImg=true;
			}
		}
		return bImg;
	};

	//2014.12.27 look at both the startContainer and endContainer;
	var xImg=null, xRng=getSelRange();
	if(xRng){
		var t=seekInnerElementByName(xRng.startContainer, 'img');
		if(t){
			xImg=t;
		}else{
			t=seekInnerElementByName(xRng.endContainer, 'img');
			if(t){
				xImg=t;
			}
		}
	}
	return xImg;
}

function focusOnImage(){return curImage() ? true : false;}

//function localPathFromUrl(sUrl)
//{
//	var sFn=''; sUrl=sUrl||'';
//	if(sUrl){
//		if(sUrl.match(/^file\:[\/\\]{2,}[a-z]\:\/(.*)$/i)){ // file:///c:/WINDOWS/clock.avi
//			sFn=sUrl.replace(/^file\:[\/\\]{2,}/i, '');
//		}else if(sUrl.match(/^file\:[\/\\]{2,}(.*)$/i)){ // file:///etc/fstab, file://///t440p/dir/123.txt
//			sFn=sUrl.replace(/^file\:[\/\\]{2,}/i, '');
//		}
//	}
//	return sFn;
//}

function urlFromLocalFile(sFn, bPercentEncoding, sExcl, sIncl){
	var sUrl=''; sFn=(sFn||'').toString().replace(/\\/g, '/');
	if(sFn){

		if(bPercentEncoding){
			sFn=app.percentEncode(sFn, (sExcl || '/:'), sIncl);
		}

		sUrl='file://';

		//2015.1.15 prepend a slash for local file path if necessary e.g. for DOS;
		//2015.3.2 consider of UNC path: file://///servername/share/file.txt
		//http://rubenlaguna.com/wp/2007/04/20/firefox-and-file-windows-unc-paths/
		//http://en.wikipedia.org/wiki/File_URI_scheme
		if(sFn.search(/^\//)<0 || sFn.search(/^\/\/[\w\d]+/)==0){
			sUrl+='/';
		}

		sUrl+=sFn;
	}
	return sUrl;
}

function localFileFromUrl(sUrl, bPercentDecoding){
	var sFn='', sScheme='file://'; sUrl=(sUrl||'').toString();
	if(sUrl.search(/^file:\/\//i)==0){

		sFn=sUrl.replace(/^file:\/\//i, '');

		sFn=sFn.replace(/\\/g, '/'); //2016.6.4 MS-Word uses the windows style back-slashes in its file path, within clips;

		if(sFn && sFn.search(/^\/[c-z][\:\|]\/.+/i)==0 || sFn.search(/^\/\/\/.+/i) ==0|| sFn.search(/^\/\.\/.+/i)==0 || sFn.search(/^\/\$\{.+?\}/i)==0){
			//2016.4.6 consider of UNC names on Windows & old style of relative path; e.g.
			//file:///C:/temp/123.txt
			//file://///t440p/temp/123.txt
			//file://./temp/123.txt
			//file:///${HOME}/temp/123.txt
			sFn=sFn.substr(1);
		}

		//2016.4.7 consider of special characters in percent-encoding;
		if(bPercentDecoding && sFn.indexOf('%')>=0 ){
			sFn=app.percentDecode(sFn);
		}
	}
	return sFn;
};

//function validateHtmlFragment(sHtml)
//{
//	//2015.4.27 msexcel copies incomplete table structure but just <tr> or <td> without <table> tags;
//	if(sHtml.match(/^<\!--StartFragment-->/gi) && sHtml.match(/<\!--EndFragment-->$/gi)){

//		sHtml=sHtml.replace(/^<\!--StartFragment-->/i, '');
//		sHtml=sHtml.replace(/<\!--EndFragment-->$/i, '');

//		sHtml=_trim(sHtml);

//		//msexcel/msword uses leading Blankspaces for html source indentation, but Tab is proposed for this purpose in NYF7;
//		//The redundant leading spaces would produce unwanted '&nbsp;' after each Table cells: <td>...</td>&nbsp;
//		var _removeLeadingSpaces=function(s){
//			var v=s.split('\n'), r='';
//			for(var i in v){
//				var sLine=v[i].replace(/^\s+/, '');
//				if(r) r+='\n';
//				r+=sLine;
//			}
//			return r;
//		};

//		if(sHtml.match(/^<col>|^<col\b|^<tr>|^<tr\b/i) && sHtml.match(/<\/tr>$/i)){ //tweaks for msexcel

//			sHtml='<table border="1" cellpadding="5" cellspacing="0">'+sHtml+'</table>';
//			sHtml=_removeLeadingSpaces(sHtml);

//		}else if(sHtml.match(/^<td>|^<td\b/i) && sHtml.match(/<\/td>$/i)){ //tweaks for msexcel

//			sHtml='<table border="1" cellpadding="5" cellspacing="0"><tr>'+sHtml+'</tr></table>';
//			sHtml=_removeLeadingSpaces(sHtml);

//		}else if(sHtml.match(/^<table>|^<table\b/i) && sHtml.match(/<\/table>$/i)){ //tweaks for msword

//			//seemed not to work with mulitple lines (CR/LF);
//			//sHtml=sHtml.replace(/^<table\b(.*?)>(.*)</table>$>/gi, '<table border="1" cellpadding="5" cellspacing="0">$2</table>');

//			//2015.4.27 This code tries to make some tweaks for msword/table clips,
//			//unfortunately, it causes confusion with other web clips constrcuted by <table>;
//			/*
//			var _cleanUp=function(xElm){
//				for(var i=0; i<xElm.childNodes.length; ++i){

//					var xSub=xElm.childNodes[i];
//					if(xSub.nodeType==Node.ELEMENT_NODE){

//						xSub.removeAttribute('id');
//						xSub.removeAttribute('class');
//						xSub.removeAttribute('style');

//						if(xSub.nodeName.toLowerCase()=='table'){
//							xSub.setAttribute('border', '1');
//							xSub.setAttribute('cellpadding', '5');
//							xSub.setAttribute('cellspacing', '0');
//						}else if(xSub.nodeName.toLowerCase()=='td'){
//							xSub.removeAttribute('valign');
//							xSub.removeAttribute('width');
//						}

//						_cleanUp(xSub);
//					}
//				}
//			};

//			var xDiv=document.createElement('div');
//			xDiv.innerHTML=sHtml;
//			_cleanUp(xDiv);

//			sHtml=xDiv.innerHTML;
//			*/
//		}
//	}else if(sHtml.match(/^<html><head>.*?<\/head><body>.*<\/body><\/html>$/i)){
//		//2016.4.9 A full HTML frame is contructed when copying selected content in the integrated webkit on Mac; like this;
//		//<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>.......<body></html>
//		//attempts to get rid of it and avoid the redundant <meta> tags being inserted;
//		sHtml=sHtml.replace(/^<html><head>.*?<\/head><body>(.*)<\/body><\/html>$/i, function(t0, t1){return t1;});
//	}else{
//		//2016.3.25 bugfix: forcedly get rid of the prefix tags "<meta ...><header ...>";
//		//Google Chrome for Mac inserts the prefix tags in front of copied HTML text;
//		//sHtml=sHtml.replace(/^<meta\s.*?>/i, '');
//		//sHtml=sHtml.replace(/^<header\s.*?>/i, '');

//		//2018.9.14 clip text coplied from in RichEditor contains a header block like this;
//		//<meta name="qrichtext" content="1" />
//		//<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
//		//<style type="text/css">
//		//	p, li { white-space: pre-wrap; }
//		//</style>
//		alert(sHtml);
//		sHtml=sHtml.replace(/<meta\s[^>]*?\/>/igm, '');
//		sHtml=sHtml.replace(/<style\s[^>]*?>.*?<\/style>/igm, '');
//		sHtml=sHtml.replace(/<head>.*?<\/head>/igm, '');
//		alert(sHtml);
//	}

//	return sHtml;
//}

function validateHtmlFragment(sHtml)
{
	if(sHtml.match(/^<\!--StartFragment-->/gi) && sHtml.match(/<\!--EndFragment-->$/gi)){ //for table/cells copied from MS-Office

		sHtml=sHtml.replace(/^<\!--StartFragment-->/i, '');
		sHtml=sHtml.replace(/<\!--EndFragment-->$/i, '');

		sHtml=_trim(sHtml);

		//msexcel/msword uses leading Blankspaces for html source indentation, but Tab is supposed for this purpose in NYF7;
		//The redundant leading spaces would produce unwanted '&nbsp;' after each Table cells: <td>...</td>&nbsp;
		var _removeLeadingSpaces=function(s){
			var v=s.split('\n'), r='';
			for(var i in v){
				var sLine=v[i].replace(/^\s+/, '');
				if(r) r+='\n';
				r+=sLine;
			}
			return r;
		};

		//2015.4.27 msexcel copies incomplete table structure but just <tr> or <td> without <table> tags;
		if(sHtml.match(/^<col>|^<col\b|^<tr>|^<tr\b/i) && sHtml.match(/<\/tr>$/i)){ //tweaks for msexcel

			sHtml='<table border="1" cellpadding="5" cellspacing="0">'+sHtml+'</table>';
			sHtml=_removeLeadingSpaces(sHtml);

		}else if(sHtml.match(/^<td>|^<td\b/i) && sHtml.match(/<\/td>$/i)){ //tweaks for msexcel

			sHtml='<table border="1" cellpadding="5" cellspacing="0"><tr>'+sHtml+'</tr></table>';
			sHtml=_removeLeadingSpaces(sHtml);

		}else if(sHtml.match(/^<table>|^<table\b/i) && sHtml.match(/<\/table>$/i)){ //tweaks for msword

			//seemed not to work with mulitple lines (CR/LF);
			//sHtml=sHtml.replace(/^<table\b(.*?)>(.*)</table>$>/gi, '<table border="1" cellpadding="5" cellspacing="0">$2</table>');

			//2015.4.27 This code tries to make some tweaks for msword/table clips,
			//unfortunately, it causes confusion with other web clips constrcuted by <table>;
			/*
			var _cleanUp=function(xElm){
				for(var i=0; i<xElm.childNodes.length; ++i){

					var xSub=xElm.childNodes[i];
					if(xSub.nodeType==Node.ELEMENT_NODE){

						xSub.removeAttribute('id');
						xSub.removeAttribute('class');
						xSub.removeAttribute('style');

						if(xSub.nodeName.toLowerCase()=='table'){
							xSub.setAttribute('border', '1');
							xSub.setAttribute('cellpadding', '5');
							xSub.setAttribute('cellspacing', '0');
						}else if(xSub.nodeName.toLowerCase()=='td'){
							xSub.removeAttribute('valign');
							xSub.removeAttribute('width');
						}

						_cleanUp(xSub);
					}
				}
			};

			var xDiv=document.createElement('div');
			xDiv.innerHTML=sHtml;
			_cleanUp(xDiv);

			sHtml=xDiv.innerHTML;
			*/
		}

	}else{

		//2018.9.15 the RegExp in Qt487 sucks, with no support of multiple lines; A workaround required to bypass all [\r\n] !!!
		var rSubst='<__0A__>', nSubst='<__0D__>';
		sHtml=sHtml.replace(/\r/igm, rSubst).replace(/\n/igm, nSubst);

		{
			//app.log('<0>: '+sHtml+'\n');

			//2018.9.15 html fragments copied from in Rich editor includes the full <DOCTYPE/html/head/meta/style/body> structure;
			//In order to keep full formatting data, we just need to strip off some unwanted tags, such as <meta> <head>, and keep all others intact;
			//get rid of all <meta/style/head> tags copied from Chrome, that looks like: <meta charset='utf-8'>...
			//The <style> may contains: "p, li { white-space: pre-wrap; }" which is unwanted;
			sHtml=sHtml.replace(/<meta[^>]*>/igm, '');
			sHtml=sHtml.replace(/<style[^>]*>.*?<\/style>/igm, '');
			sHtml=sHtml.replace(/<head[^>]*>.*?<\/head>/igm, '');

			//app.log('<1>: '+sHtml+'\n');

			//2016.4.9 contents copied from in the integrated webkit for Mac adds the full <html/head/meta/body> structure, but without "<!--EndFragment-->";
			//<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>.......<body></html>
			//simply strip off all those unwanted surrounding HTML tags, just keep the fragment contents in <body>;
			sHtml=sHtml.replace(/^<html><head>.*?<\/head><body>(.*)<\/body><\/html>$/igm, function(m0, m1){return m1;});

			//app.log('<2>: '+sHtml+'\n');
		}

		//restore the \r\n
		sHtml=sHtml.replace(new RegExp(rSubst, 'g'), '\r').replace(new RegExp(nSubst, 'g'), '\n');

	}

	return sHtml;
}

function makeLocalImagesEmbedded(sHtml)
{
	var _make_embedded=function(xElm){
		if(xElm && xElm.nodeType==Node.ELEMENT_NODE){
			if(xElm.nodeName.toLowerCase()=='img'){

				var sUrl=xElm.getAttribute('src');
				var sFn=localFileFromUrl(sUrl, true);

				if(sFn){
					var sBase64=app.loadFileBase64(sFn);
					if(sBase64){
						var sExt=suffixNameOf(sFn);
						var sSrc='data:image/' + (sExt||'jpg') + ';base64,' + sBase64;
						xElm.setAttribute('src', sSrc);
					}
				}
			}
			for(var i=0; i<xElm.childNodes.length; ++i){
				var xSub=xElm.childNodes[i];
				_make_embedded(xSub);
			}
		}
	};

	var xDiv=document.createElement('div');
	xDiv.innerHTML=sHtml;
	_make_embedded(xDiv);
	return xDiv.innerHTML;
}

function tweaksOnHtmlFragment(sHtml)
{
	//2015.4.27 tweaks on html fragment prior to being inserted into HTML Editor;
	if(!sHtml) sHtml=app.arg(0);
	if(sHtml){
		sHtml=validateHtmlFragment(sHtml||'');
		sHtml=makeLocalImagesEmbedded(sHtml);
	}
	return sHtml;
}

function extractImageLinks(sHtml)
{
	var vImgs=[];

	var _push=function(d0){
		if(d0 && d0.xElm && d0.sSrc){
			var bFound=false;
			for(var i in vImgs){
				var d=vImgs[i];
				if(d.sSrc==d0.sSrc){
					bFound=true;
					break;
				}
			}
			if(!bFound) vImgs.push(d0);
		}
	};

	var _select_images=function(xElm){
		if(xElm && xElm.nodeType==Node.ELEMENT_NODE){
			if(xElm.nodeName.toLowerCase()=='img'){
				var sSrc=xElm.getAttribute('src')||'';
				//https links won't download, but better list them out for awareness;
				if(sSrc.search(/^(file|http|https):\/\//i)==0){
					_push({xElm: xElm, sSrc: sSrc}); //2015.4.26 ignore duplicates;
				}
			}
			for(var i=0; i<xElm.childNodes.length; ++i){
				var xSub=xElm.childNodes[i];
				_select_images(xSub);
			}
		}
	};

	if(!sHtml) sHtml=app.arg(0);

	var sRes='';
	if(sHtml){

		var xDiv=document.createElement('div');
		xDiv.innerHTML=sHtml;
		_select_images(xDiv);

		for(var i in vImgs){
			var sUrl=vImgs[i].sSrc;
			if(sUrl){
				if(sRes) sRes+='\n';
				sRes+=sUrl;
			}
		}
	}

	return sRes;
}

/*function makeRemoteImagesEmbedded(sHtml)
{
	var vImgs=[];
	var _select_images=function(xElm){
		if(xElm && xElm.nodeType==Node.ELEMENT_NODE){
			if(xElm.nodeName.toLowerCase()=='img'){
				var sSrc=xElm.getAttribute('src');
				if(sSrc && sSrc.match(/^http\:\/\/(.*)$/i)){
					vImgs.push({xElm: xElm, sSrc: sSrc});
				}
			}
			for(var i=0; i<xElm.childNodes.length; ++i){
				var xSub=xElm.childNodes[i];
				_select_images(xSub);
			}
		}
	};

	var nDone=0;
	var _download_images=function(){
		for(var j in vImgs){
			var d=vImgs[j], bAsync=false, bSilent=true;
			ajax.run(bAsync, 'GET', d.sSrc, '', d, function(sData, d){
				if(sData){
					var sBase64=app.base64Encoding(sData);
					if(sBase64){
						var sSrc=d.sSrc;
						var sExt=suffixNameOf(sFn);
						sSrc='data:image/' + (sExt||'jpg') + ';base64,' + sBase64;
						d.xElm.setAttribute('src', sSrc);
						nDone++;
					}
				}
			}, function(xReq, sMsg, d){
				//alert(sMsg);
			}, bSilent);
		}
	};

	var xDiv=document.createElement('div');
	xDiv.innerHTML=sHtml;
	_select_images(xDiv);

	_download_images();

	var sRes='';
	if(nDone>0){
		sRes=xDiv.innerHTML;
	}

	return sRes;
}*/

function getDataByUrl(sUrl, bBase64, bSilent)
{
	var sRes; sUrl=sUrl||'';
	if(sUrl){

		var sFn=localFileFromUrl(sUrl, true);
		if(sFn){
			if(bBase64){
				sRes=app.loadFileBase64(sFn);
			}else{
				//not supported;
			}
		}else{
			var bAsync=false, sParam='';
			ajax.run(bAsync, 'GET', sUrl, sParam, null, function(sData){
				if(sData){
					if(bBase64){
						sRes=app.base64Encode(sData, 'binary');
					}else{
						sRes=sData;
					}
				}
			}, function(xReq, sMsg){
				//alert(sMsg);
			}, bSilent);
		}
	}

	return sRes;
}

function replaceImageSrc(sUrl, sImgSrcDat, bSelection)
{
	var bDirty=false;

	if(!sImgSrcDat) sImgSrcDat=app.arg(0);

	var _act_on_elm=function(e, iLevel, xUserData){
		if(e.nodeName.toLowerCase()=='img' ){
			var sSrc=e.getAttribute('src');
			if(sSrc==sUrl){
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(e, 'src', sImgSrcDat));
				bDirty=true;
			}
		}
	};

	g_xUndoStack.beginMacro('replace src of <img>');
	if(bSelection){
		traverseSelection(_act_on_elm, 0, null);
	}else{
		traverseDomBranch(document.body, 0, null, _act_on_elm, null);
	}
	g_xUndoStack.endMacro();

	return bDirty;
}

//function getContextImgElm()
//{
//	var e;
//	if(app.getContextDomElement) e=app.getContextDomElement();
//	if(!e || e.nodeName.toLowerCase()!='img') e=curImage();
//	return (e && e.nodeName.toLowerCase()=='img') ? e : undefined;
//}

function getContextImgElm()
{
	var xElm=app.getContextDomElement();
	return (xElm && xElm.nodeName.toLowerCase()=='img') ? xElm : undefined;
}

function dimOfImage(xImg, bNatural)
{
	var sRes;
	xImg=xImg||getContextImgElm();
	if(xImg){
		var r={width: xImg.naturalWidth, height: xImg.naturalHeight};
		if(!bNatural){
			var w=xImg.getAttribute('width');
			var h=xImg.getAttribute('height');
			if(w && h){
				w=parseInt(w);
				h=parseInt(h);
				if(w>0 && h>0) r={width: w, height: h};
			}
		}
		sRes=''+r.width+'x'+r.height;
	}
	return sRes;
}

//function selectedImages()
//{
//	var vImg=[];
//	var _xAct=function(xElm, iLevel, xUserData){
//		if(xElm && xElm.nodeName.toLowerCase()=='img'){
//			vImg.push(xElm);
//		}
//	};
//	traverseSelection(_xAct, 0, null);
//	return vImg;
//}

//function ResizeImage(xImg, w, h)
//{
//	var v=[];
//	{
//		//2017.12.15 first look at the image under the mouse cursor;
//		//then try to retrieve all the images within the current selection;
//		xImg=xImg||getContextImgElm();
//		if(xImg){
//			v.push(xImg);
//		}else{
//			v=selectedImages();
//		}
//	}

//	if(v && v.length>0){
//		g_xUndoStack.beginMacro('resize <img>');
//		for(var i=0; i< v.length; ++i){
//			var xImg=v[i];
//			if(xImg){
//				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xImg, 'width', ''+w));
//				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xImg, 'height', ''+h));
//			}
//		}
//		g_xUndoStack.endMacro();
//	}
//}

function ResizeImage(xImg, w, h)
{
	xImg=xImg||getContextImgElm();
	if(xImg){
		g_xUndoStack.beginMacro('resize <img>');
		g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xImg, 'width', ''+w));
		g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xImg, 'height', ''+h));
		g_xUndoStack.endMacro();
	}
}

function RotateImage(xImg, d)
{
	//http://www.w3school.com.cn/cssref/pr_transform.asp
	//http://www.cssportal.com/blog/rotating-images-with-css/
	//http://stackoverflow.com/questions/11732363/stacking-css3-transform-functions-from-multiple-selectors-in-stylesheet

	xImg=xImg||getContextImgElm();
	if(xImg){

		var sVal=''; if((d%360)!=0) sVal='rotate(%DEGREE%deg)'.replace('%DEGREE%', ''+d);

		var vCss=[];
		vCss.push({key: '-webkit-transform', val: sVal});
		vCss.push({key: '-moz-transform', val: sVal});
		vCss.push({key: '-ms-transform', val: sVal});
		vCss.push({key: '-o-transform', val: sVal});
		vCss.push({key: 'transform', val: sVal});

		g_xUndoStack.beginMacro('rotate <img>');
		cssUtil(xImg, vCss);
		g_xUndoStack.endMacro();
	}
}
