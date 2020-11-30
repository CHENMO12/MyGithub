
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function makeBookmarkAnchor()
{
	var sBmName, xRng=getSelRange();
	if(xRng){
		var xElm=xRng.startContainer;
		//if(xElm && xElm.nodeType==Node.TEXT_NODE) xElm=xElm.parentNode;
		if(xElm && xElm.parentNode){

			{
				var t=new Date();
				var n=Math.floor(t.getTime()/1000);
				sBmName='nyf_'+n.toString(16);
			}

			var xA=document.createElement('A');
			xA.setAttribute('name', sBmName);
			xElm.parentNode.insertBefore(xA, xElm);
			app.setDomDirty(true);
		}
	}
	return sBmName;
}

function triggerBookmarkAnchor(sBmName)
{
	var bFound=false;
	if(sBmName){

		var s_vTagsBlock="body|address|blockquote|center|code|div|p|pre|h1|h2|h3|h4|h5|h6|hr|dl|dd|dt|table|tbody|thead|tfoot|th|tr|td|ul|ol|li|fieldset|form|script|noscript|meta|link|title|colgroup|col".split('|');

		var _is_block_elm=function(e){return e && (s_vTagsBlock.indexOf(e.nodeName.toLowerCase())>=0);};

		var xPara = null;
		var v=document.getElementsByTagName('a');
		for(var i=0; i<v.length; ++i){
			var xA=v[i];
			if(xA){
				var sName=xA.getAttribute('name');
				if(sName==sBmName){
					xPara = xA.parentNode;
					while(xPara && !_is_block_elm(xPara)){
						xPara = xPara.parentNode;
					};

					bFound=true;
					break;
				}
			}
		}

		if(!bFound){
			if(document.getElementById(sBmName)){
				xPara = document.getElementById(sBmName);
				bFound=true;
			}
		}

		if(bFound && window.location){
			window.location.hash = "";
			window.location.hash = "#" + sBmName;

			blink(xPara);
		}
	}
	return bFound;
}

function blink(o)
{
	var bg = document.createElement("div");
	bg.style.width = o.offsetWidth + "px";
	bg.style.height = o.offsetHeight + "px";
	bg.style.position = "absolute";
	bg.style.left = o.offsetLeft + "px";
	bg.style.top = o.offsetTop + "px";
	bg.style.background = "rgb(70, 162, 218)";
	bg.style.zIndex = -1;
	bg.style.opacity = 1.0;
	document.body.appendChild(bg);

	var interval = setInterval(function () {
		bg.style.opacity-=0.06;
		if (bg.style.opacity <= 0.05) {
			clearInterval(interval);
			document.body.removeChild(bg);
		}
	}, 50);
}


















function allocBkmkId()
{
	var sBkmk;
	var n = 0;
	do{
		sBkmk = "nyf_bkmk_" + n++;
	}while(document.getElementById(sBkmk));
	/*while(true){
		sBkmk = "nyf_bkmk_" + n;
		if(!document.getElementById(sBkmk)){
			break;
		}
		n++;
	}*/
	return sBkmk;
}

function createBkmk()
{
	var sID;
	var s_vTagsBlock='body|address|blockquote|center|code|div|p|pre|h1|h2|h3|h4|h5|h6|hr|dl|dd|dt|table|tbody|thead|tfoot|th|tr|td|ul|ol|li|fieldset|form|script|noscript|meta|link|title|colgroup|col'.split('|');

	var _is_block_elm=function(e){return e && (s_vTagsBlock.indexOf(e.nodeName.toLowerCase())>=0);};

	var xRng=getSelRange();

	//if(xRng){
		var xElm=xRng.endContainer;

		if(xElm.nodeType==Node.TEXT_NODE) xElm=xElm.parentNode;

		var e=xElm;

		//2015.5.21 Do not seek parent node, but just skip TEXT_NODE;
		//It may go beyond the current selection, as blankspace/CR/LF separators 
		//between HTML tags are also parsed as 'TEXT_NODE's within DOM;
		//if(e.nodeType==Node.TEXT_NODE) e=e.parentNode;

		if(e && e.nodeType==Node.ELEMENT_NODE){

			while(e && !_is_block_elm(e)){ //2015.5.21 only apply to the block-level tags;
				e=e.parentNode;
			}

			if(e && _is_block_elm(e)){
				sID = e.getAttribute("id") || "";
				if(sID == ""){
					sID = allocBkmkId() || "";
				}

				if(sID != ""){
					e.setAttribute("id", sID);
					app.setDomDirty(true);
					//g_xUndoStack.pushMacro(new _CCmdChgElmAttr(e, 'id', sID));
					//bDirty=true;
				}
			}
		}
	//}

	/*var _act_on_elm=function(xElm, iLevel, xUserData){

		var e=xElm;

		//2015.5.21 Do not seek parent node, but just skip TEXT_NODE;
		//It may go beyond the current selection, as blankspace/CR/LF separators 
		//between HTML tags are also parsed as 'TEXT_NODE's within DOM;
		//if(e.nodeType==Node.TEXT_NODE) e=e.parentNode;

		if(e && e.nodeType==Node.ELEMENT_NODE){

			while(e && !_is_block_elm(e)){ //2015.5.21 only apply to the block-level tags;
				e=e.parentNode;
			}

			if(e && _is_block_elm(e)){
				var sID = e.getAttribute("id") || "";
				if(sID != ""){
					sID = allocBkmkId() || "";
				}
				if(sID != ""){
					g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, 'id', sID));
					bDirty=true;
				}
			}
		}

	};*/

	return sID;
}

function jumpToBkmk(sBmk)
{
	var bSucc = false;
	var xEle = document.getElementById(sBmk);
	if(xEle){
		window.location.hash = "";
		window.location.hash = "#" + sBmk;

		blink(xEle);

		bSucc = true;
	}
	return bSucc;
}


