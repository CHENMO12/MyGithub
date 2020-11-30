
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function replaceAnchorHref(sUrl, sNewUrl)
{
	var _act_on_elm=function(e, iLevel, xUserData){
		if(e.nodeName.toLowerCase()=='a' ){
			var sHref=e.getAttribute('href');
			if(sHref==sUrl){
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(e, 'href', sNewUrl));
			}
		}
	};

	g_xUndoStack.beginMacro('replace links');
	traverseDomBranch(document.body, 0, null, _act_on_elm, null);
	g_xUndoStack.endMacro();
}

function extractHrefLinks(sHtml)
{
	var vHrefs=[];

	var _select_hrefs=function(xElm){
		if(xElm && xElm.nodeType==Node.ELEMENT_NODE){
			if(xElm.nodeName.toLowerCase()=='a'){
				var sHref=xElm.getAttribute('href');
				vHrefs.push(sHref);
			}
			for(var i=0; i<xElm.childNodes.length; ++i){
				var xSub=xElm.childNodes[i];
				_select_hrefs(xSub);
			}
		}
	};

	var xDiv=document.createElement('div');
	xDiv.innerHTML=sHtml;
	_select_hrefs(xDiv);

	var sTxt='';
	for(var i in vHrefs){
		var sUrl=vHrefs[i];
		if(sUrl){
			if(sTxt) sTxt+='\n';
			sTxt+=sUrl;
		}
	}

	return sTxt;
}

/*function replaceAnchorWithImg(sUrl, sData)
{
	var bDirty=false;
	var vItems = [];
	var _act_on_elm=function(e, iLevel, xUserData){
		if(e.nodeName.toLowerCase()=='a' ){
			var sHref=e.getAttribute('href');
			if(sHref==sUrl){
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(e, 'href', null));
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(e, 'src', null));
				vItem.push({path: pathOfNode(e), tagNew: 'img'});
			}
		}
	};

	g_xUndoStack.beginMacro('replace links');
	traverseDomBranch(document.body, 0, null, _act_on_elm, null);
	g_xUndoStack.pushMacro(new _CCmdReplaceElmTags(vItems));
	g_xUndoStack.endMacro();

	return bDirty;
}*/

