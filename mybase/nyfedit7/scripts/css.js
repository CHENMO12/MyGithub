
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function cssUtil(xElm, k, v)
{
	if(xElm && xElm.getAttribute){

		var sCssOld=xElm.getAttribute('style')||''; //<span style="line-height: 18px; margin: 3px;">

		var _parse_style=function(sCss){
			var v2=sCss.split(';'), xCss={};
			for(var i in v2){
				var a=_trim(v2[i]||'');
				var p=a.indexOf(':');
				if(p>0){
					var key=_trim(a.substr(0, p)), val=_trim(a.substr(p+1));
					if(key){
						xCss[key]=val;
					}
				}
			}
			return xCss;
		};

		var _set_style=function(xCss){

			var sCssNew='';
			for(var i in xCss||{}){
				var key=i, val=xCss[i];
				if(key && val){
					if(sCssNew) sCssNew+='; ';
					sCssNew+=key+': '+val;
				}
			}

			if(sCssNew!=sCssOld){
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, 'style', sCssNew));
				return true; //modified;
			}
		};

		if(k === undefined){

			//return value of the attribute 'style';
			return sCssOld;

		}else if(k.constructor === Array){
			if(k.length>0){
				var xCss=_parse_style(sCssOld)||{};
				for(var i in k){
					var d=k[i];
					var sKey=d.key||'', sVal=d.val||'';
					if(sKey){
						xCss[sKey]=sVal;
					}
				}
				return _set_style(xCss);
			}

		}else if(typeof(k) === 'string'){

			if(k){
				if(v === undefined){

					var xCss=_parse_style(sCssOld)||{};
					return xCss[k]||'';

				}else{
					var xCss=_parse_style(sCssOld)||{};
					xCss[k]=v||'';
					return _set_style(xCss);
				}
			}
		}
	}
}

function parCssUtil(k, v)
{
	var bDirty=false;

	//var s_vTagsBlock='body|address|blockquote|center|code|div|p|pre|h1|h2|h3|h4|h5|h6|hr|dl|dd|dt|table|tbody|thead|tfoot|th|tr|td|ul|ol|li|fieldset|form|script|noscript|meta|link|title|colgroup|col'.split('|');

	var _is_block_elm=function(e){return isBlockLevelElement(e.nodeName);}; //function(e){return e && (s_vTagsBlock.indexOf(e.nodeName.toLowerCase())>=0);};

	var _act_on_elm=function(xElm, iLevel, xUserData){

		var e=xElm;

		//2015.5.21 Do not seek parent node, but just skip TEXT_NODE;
		//It may go beyond the current selection, as blankspace/CR/LF separators 
		//between HTML tags are also parsed as 'TEXT_NODE's within DOM;
		//if(e.nodeType==Node.TEXT_NODE) e=e.parentNode;

		if(e && (e.nodeType===Node.ELEMENT_NODE || e.nodeType===Node.TEXT_NODE)){

			while(e && !_is_block_elm(e)){ //2015.5.21 only apply to the block-level tags;
				e=e.parentNode;
			}

			if(e && _is_block_elm(e)){
				if(cssUtil(e, k, v)===true){
					bDirty=true;
				}
			}
		}

	};

	if(k){
		g_xUndoStack.beginMacro('Paragraph formats');
		traverseSelection(_act_on_elm);
		g_xUndoStack.endMacro();
	}

	return bDirty;
}

function parAttrUtil(k, v)
{
	var bDirty=false, vRes=[];

	//var s_vTagsBlock='body|address|blockquote|center|code|div|p|pre|h1|h2|h3|h4|h5|h6|hr|dl|dd|dt|table|tbody|thead|tfoot|th|tr|td|ul|ol|li|fieldset|form|script|noscript|meta|link|title|colgroup|col'.split('|');

	var _is_block_elm=function(e){return isBlockLevelElement(e.nodeName);}; //function(e){return e && (s_vTagsBlock.indexOf(e.nodeName.toLowerCase())>=0);};

	var _act_on_elm=function(xElm, iLevel, xUserData){

		var e=xElm;

		//2015.5.21 Do not seek parent node, but just skip TEXT_NODE;
		//It may go beyond the current selection, as blankspace/CR/LF separators 
		//between HTML tags are also parsed as 'TEXT_NODE's within DOM;
		//if(e.nodeType==Node.TEXT_NODE) e=e.parentNode;

		if(e && (e.nodeType===Node.ELEMENT_NODE || e.nodeType===Node.TEXT_NODE)){
			while(e && !_is_block_elm(e)){ //2015.5.21 only apply to the block-level tags;
				e=e.parentNode;
			}
			if(e && _is_block_elm(e)){
				var sAttrOld = e.getAttribute(k);
				if(v===undefined){
					//2015.8.7 to retrieve the existing values;
					vRes.push(sAttrOld);
				}else{
					if(sAttrOld != v){
						g_xUndoStack.pushMacro(new _CCmdChgElmAttr(e, k, v));
						bDirty=true;
					}
				}
			}
		}

	};

	if(k){
		g_xUndoStack.beginMacro('Paragraph attribute set');
		traverseSelection(_act_on_elm);
		g_xUndoStack.endMacro();
	}

	if(vRes.length>0){
		return vRes;
	}else{
		return bDirty;
	}
}

function isParagraphsSelected()
{
	var bDirty=false;

	//var s_vTagsBlock='body|address|blockquote|center|code|div|p|pre|h1|h2|h3|h4|h5|h6|hr|dl|dd|dt|table|tbody|thead|tfoot|th|tr|td|ul|ol|li|fieldset|form|script|noscript|meta|link|title|colgroup|col'.split('|');

	var _is_block_elm=function(e){return isBlockLevelElement(e.nodeName);}; //function(e){return e && (s_vTagsBlock.indexOf(e.nodeName.toLowerCase())>=0);};

	var xPara = null, bRes = false;

	var _act_on_elm=function(xElm, iLevel, xUserData){

		var e=xElm;

		//2015.5.21 Do not seek parent node, but just skip TEXT_NODE;
		//It may go beyond the current selection, as blankspace/CR/LF separators 
		//between HTML tags are also parsed as 'TEXT_NODE's within DOM;
		//if(e.nodeType==Node.TEXT_NODE) e=e.parentNode;

		if(e && e.nodeType===Node.ELEMENT_NODE){

			while(e && !_is_block_elm(e)){ //2015.5.21 only apply to the block-level tags;
				e=e.parentNode;
			}

			if(e && _is_block_elm(e)){
				if(xPara && xPara != e){
					bRes = true;
				}
				if(!xPara) xPara = e;
			}
		}

	};

	traverseSelection(_act_on_elm);
	return bRes;
}
