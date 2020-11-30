
/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2016 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////


//sValidation=domjs
//sAuthor=wjjsoft

if(!window.removeFormatting){
	window.removeFormatting=function(xNode){

		xNode=xNode||document;

		g_xUndoStack.beginMacro('Remove formatting');

		//remove class/style attributes;
		{
			var _remove_attributes=function(xElm, v){
				var nDel=0, sTag=xElm.nodeName.toLowerCase();
				for(var i in v||[]){
					if(xElm.hasAttribute(v[i])){
						g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, v[i], ''));
						nDel++;
					}
				}
				return nDel;
			};

			var _remove_style_class=function(xElm, iLevel, xUserData){
				if(xElm.nodeType==Node.ELEMENT_NODE){
					var sTag=xElm.nodeName.toLowerCase(), sAttrToDel='class';
					if(sTag=='style'){

						var i=xElm.childNodes.length;
						while( i-- > 0 ){
							g_xUndoStack.pushMacro(new _CCmdRemoveElm(xElm, xElm.childNodes.item(i), 0));
						}

						var sCss='table{border-collapse: collapse; border: 1px solid gray; border-width: 2px 1px 2px 1px;}\n'
							+ 'th{border: 1px solid gray; padding: 4px; background-color: #ddd;}\n'
							+ 'td{border: 1px solid gray; padding: 4px;}\n'
							+ 'tr:nth-child(2n){background-color: #f8f8f8;}\n'
							;
						g_xUndoStack.pushMacro(new _CCmdInsertElm(xElm, document.createTextNode(sCss), -1));

					}else if(sTag=='body'){
						sAttrToDel+='|style|bgcolor|background|alink|link|vlink|text';
					}else if(sTag=='font'){
						sAttrToDel+='|style|face|size|color';
					}else if(sTag=='tr' || sTag=='td'){
						sAttrToDel+='|style|align|width|height|border|cellspacing|cellpadding';
					}else if(sTag=='link'){
						sAttrToDel+='|style|href';
					}else if(sTag=='table'){

						//2014.12.31 consider default formatting for tables;
						//g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, 'border', '1'));
						//g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, 'cellspacing', '0'));
						//g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, 'cellpadding', '5px'));

						//2015.8.6 default css for tables;
						//var sCss='table-layout: fixed; word-break: break-all; empty-cells: show; background-color:#EAF2D3; margin-left: 1em;';

						//2016.7.23 defaults to the new style of html tables, to comply with beta-24;
						var sCss='width: 60%;'
							+ ' border-collapse: collapse; border: 1px solid gray; border-width: 2px 1px 2px 1px;'
							+ ' table-layout: automatic; empty-cells: show; word-break: break-all; margin-left: 0px;'
							+ ' background-color: transparent;'
							;
						g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElm, 'style', sCss));

						sAttrToDel+='|align|width|height|border|cellspacing|cellpadding';
					}else{
						sAttrToDel+='|style';
					}

					//sAttrToDel+='|id'; //2015.8.6 'id' doesn't matter as <style> has been cleared;

					_remove_attributes(xElm, sAttrToDel.split('|'));
				}
			}

			if(xNode==document){
				traverseDomChildren(xNode, 0, null, _remove_style_class, null);
			}else{
				traverseDomBranch(xNode, 0, null, _remove_style_class, null);
			}

			//traverseSelection(_remove_style_class, 0, null);
		}

		//substitute for those old-fashioned and certain html-based formatting tags;
		{

			var xSubst={
				  'div': 'p|center|h1|h2|h3|h4|h5|h6|h7|dl|dt|dd|blockquote'.split('|')
				, 'span': 'font|b|u|i|s|em|strong|ins|del|strike|small|sub|sup'.split('|')
			};

			//2015.9.3 to remove bad tags; e.g. <o:p> from MS-Word RTF2HTML conversion;
			//as those bad tags e.g. <o:p> not working in ePub;
			var xBadTag=new RegExp('[:]');

			var vRepls=[];
			var _remove_old_html_tags=function(xElm, iLevel, xUserData){
				if(xElm.nodeType==Node.ELEMENT_NODE){
					for(var j=0; j<xElm.childNodes.length; j++){
						var xSub=xElm.childNodes.item(j), iPos=j;
						var sTag=xSub.nodeName.toLowerCase();
						if(sTag.search(xBadTag)>=0){
							vRepls.push({path: pathOfNode(xSub), tagNew: 'span'});
						}else{
							for(var sNewTag in xSubst){
								if(xSubst[sNewTag].indexOf(sTag)>=0){

									//2014.12.29 Substituting Tags needs to clone child nodes, so it must immediately take action for each sub branches,
									//otherwise, it may make wrong clones if in the case that sub tags have precedingly been substituted;

									vRepls.push({path: pathOfNode(xSub), tagNew: sNewTag});

									break; //Each element can be substituted only once;
								}
							}
						}
					}
				}
			}

			if(xNode==document){
				traverseDomChildren(xNode, 0, null, null, _remove_old_html_tags);
			}else{
				traverseDomBranch(xNode, 0, null, null, _remove_old_html_tags);
			}

			//traverseSelection(_remove_old_html_tags, 0, null);

			g_xUndoStack.pushMacro(new _CCmdReplaceElmTags(vRepls));
		}

		g_xUndoStack.endMacro();
	};
}
