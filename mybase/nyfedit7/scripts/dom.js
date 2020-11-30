
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2016 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function getSelRange()
{
	var xRng;
	var xSel=document.getSelection();
	if(xSel && xSel.rangeCount>0){
		xRng = xSel.getRangeAt(0);
	}
	return xRng;
}

function cloneSelection(xRng)
{
	var xDiv; xRng=xRng || getSelRange();
	if(xRng){
		var vElms=xRng.cloneContents();
		xDiv=document.createElement('div');
		xDiv.appendChild(vElms);
	}
	return xDiv;
}

function hasSelection()
{
	//2014.8.4 test if any range is selected and is not collapsed, ie. test if the selection is not empty;
	var bSel=false, xRng=getSelRange();
	if(xRng && !xRng.collapsed){
		bSel=true;
	}
	return bSel;
}

function getSelectedHtml()
{
	var sSel='';
	if(hasSelection()){
		var xDiv=cloneSelection(null);
		if(xDiv){
			//sSel=xDiv.innerHTML;
			sSel=htmlTextOf(xDiv, 0, true); //2014.12.27 an advanced version for HTML indentation;
		}
	}
	return sSel;
}

function isEmpty(xElm)
{
	var s_vTagsData='hr|img|table|object'.split('|');
	var _seekIn=function(e){
		var bRes=true;
		if(e){
			switch(e.nodeType){
				case Node.ELEMENT_NODE:
					var sTag=e.nodeName.toLowerCase();
					if(s_vTagsData.indexOf(sTag)>=0){
						bRes=false;
					}else{
						for(var i=0; i<e.childNodes.length; ++i){
							var xSub=e.childNodes[i];
							bRes=_seekIn(xSub);
							if(!bRes) break;
						}
					}
					break;
				case Node.TEXT_NODE:
					var sTxt=e.nodeValue||'';
					if(sTxt.replace(/^[\r\n\t]+|[\r\n\t]+$/g, '')){
						bRes=false;
					}
					break;
			}
		}
		return bRes;
	};

	var bEmpty=_seekIn(xElm||document.body||document);
	//app.log('isEmpty: '+bEmpty);
	return bEmpty;
}

function seekOuterElementByName(xElm, sNodeName)
{
	//2014.8.5 seek the nearest element surrounding the given element by node name;
	sNodeName=sNodeName.toLowerCase();
	var _seekOut=function(e){
		var r;
		while(e){
			var n=e.nodeName.toLowerCase();
			if(n=='body' || n=='html'){
				break;
			}else if(n==sNodeName){
				r=e;
				break;
			}
			e=e.parentNode;
		}
		return r;
	};
	return _seekOut(xElm);
}

function seekInnerElementByName(xElm, sNodeName)
{
	//2014.8.5 seek the first element inside the given element by node name;
	sNodeName=sNodeName.toLowerCase();
	var _seekIn=function(e){
		var r;
		if(e && e.nodeType == Node.ELEMENT_NODE){
			if(e.nodeName.toLowerCase()==sNodeName){
				r=e;
			}else{
				for(var i=0; i<e.childNodes.length; ++i){
					var xSub=e.childNodes[i];
					r=_seekIn(xSub);
					if(r) break;
				}
			}
		}
		return r;
	};
	return _seekIn(xElm);
}

function getSelectedHyperlink(bExact)
{
	//2014.8.4 retrieve URL from selected range;
	var sUrl='', xRng=getSelRange();
	if(xRng){
		if(xRng.startContainer === xRng.endContainer){
			//If in the case that only link label text is selected, look at its container node <A>;
			var a=seekOuterElementByName(xRng.startContainer, 'a');
			if(a){
				sUrl=a.getAttribute('href');
			}
		}else if(!bExact){
			//Otherwise, seek the first URL in the range;
			var xDiv=cloneSelection(xRng);
			var a=seekInnerElementByName(xDiv, 'a');
			if(a){
				sUrl=a.getAttribute('href');
			}
		}
	}
	return sUrl;
}

function getCurrentHyperlink()
{
	//2014.8.4 extract current hyperlink for triggering context menu;
	//The selection should be empty(collapsed), so you can handle with the link at input cursor;
	var sUrl, xRng=getSelRange();
	if(xRng){
		if(xRng.collapsed && xRng.startContainer){
			//2014.8.5 The link label may be surrounded by some more tags, like this;
			//<div><a href="file:///C:/Users/wph/Documents/desktop.ini"><b>desktop.ini</b></a></div><div></div>
			var a=seekOuterElementByName(xRng.startContainer, 'a');
			if(a){
				sUrl=a.getAttribute('href');
			}
		}
	}
	return sUrl;
}

function changeCurrentHyperlink(sUrl)
{
	//2014.8.5 change the href for the current one at the input focus;
	var bSucc=false, xRng=getSelRange();
	if(xRng){
		if(xRng.collapsed){
			//2014.8.5 The link label may be surrounded by some more tags, like this;
			//<div><a href="file:///C:/Users/wph/Documents/desktop.ini"><b>desktop.ini</b></a></div><div></div>
			var a=seekOuterElementByName(xRng.startContainer, 'a');
			if(a){
				/*var sTmp=a.getAttribute('href');
				if(sTmp!=sUrl){
					a.setAttribute('href', sUrl);
					bSucc=true;
				}*/
				g_xUndoStack.beginMacro('Change hyperlink');
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(a, 'href', sUrl));
				g_xUndoStack.endMacro();
			}
		}
	}
	return bSucc;
}

function clearCurrentHyperlink()
{
	//2014.8.5 cancel the hyperlink for the current one at the input focus;
	var bSucc=false, xRng=getSelRange();
	if(xRng){
		if(xRng.collapsed){
			//2014.8.5 The link label may be surrounded by some more tags, like this;
			//<div><a href="file:///C:/Users/wph/Documents/desktop.ini"><b>desktop.ini</b></a></div><div></div>
			var a=seekOuterElementByName(xRng.startContainer, 'a');
			if(a){
				//move all its sub nodes as siblings, then remove <A> itself;
				/*var vSub=a.childNodes, p=a.parentNode;
				for(var i=0; i<vSub.length; ++i){
					p.insertBefore(vSub[i]);
				}
				p.removeChild(a);
				bSucc=true;*/
				g_xUndoStack.beginMacro('Remove hyperlink');
				g_xUndoStack.pushMacro(new _CCmdReplaceElmTags([{path: pathOfNode(a), tagNew: 'span'}]));
				g_xUndoStack.endMacro();
			}
		}
	}
	return bSucc;
}

function posOfNode(xElm)
{
	var iPos=-1;
	if(xElm && xElm.parentNode){
		var p=xElm.parentNode;
		for(var i=0; i<p.childNodes.length; ++i){
			if(p.childNodes[i]==xElm){
				iPos=i;
				break;
			}
		}
	}
	return iPos;
}

function pathOfNode(xElm)
{
	if(xElm && xElm.parentNode){
		return pathOfNode(xElm.parentNode)+'/'+posOfNode(xElm);
	}else{
		return '';
	}
}

function nodeByPath(sPath, bAllowPartialMatch)
{
	sPath=(sPath||'').replace(/\\/g, '/').replace(/\/+/g, '/');
	var v=sPath.split('/'), e=document, eRes;
	if(v.length>0){
		var i=0;
		while(i<v.length){
			var s=v[i++];
			if(!s) continue;
			var iPos=parseInt(s);
			if(iPos>=0 && iPos<e.childNodes.length){
				e=e.childNodes[iPos];
			}else{
				if(bAllowPartialMatch){
					break;
				}else{
					return undefined;
				}
			}
		}
		eRes=e;
	}
	return eRes;
}

function getCurrentNodePath()
{
	//2017.9.27 retrieve path of current element in HTML DOM tree;
	//1	Element
	//2	Attribute
	//3	Text
	//4	CDATA Section
	//5	Entity Reference
	//6	Entity
	//7	Processing Instrucion
	//8	Comment
	//9	Document
	//10	Document Type
	//11	Document Fragment
	//12	Notation
	var vRes=[], xRng=getSelRange();
	if(xRng){
		//if(xRng.collapsed)
		{
			var e=xRng.endContainer||xRng.startContainer;
			while(e){
				var sTag;
				{
					if(e.nodeType==1) sTag=e.nodeName;
					else if(e.nodeType==3) sTag='#TEXT';
					else if(e.nodeType==6) sTag='#ENTITY';
					else if(e.nodeType==9) sTag='#DOCUMENT';
					else sTag='?';
				}
				if(sTag) vRes.unshift(sTag);
				e=e.parentNode;
			}
		}
	}
	return vRes.join('/');
}

function childNodesOf(xElm, x)
{
	var vSub=[];
	if(xElm && xElm.childNodes){
		for(var i=0; i<xElm.childNodes.length; ++i){
			var xSub=xElm.childNodes[i];
			if(typeof(x)=='string'){
				if(x=='' || xSub.nodeName.toLowerCase()==x.toLowerCase()){
					vSub.push(xSub);
				}
			}else if(typeof(x)=='function'){
				if(x(xSub)){
					vSub.push(xSub);
				}
			}else{
				vSub.push(xSub);
			}
		}
	}
	return vSub;
}

function isBlockLevelElement(s){
	//2019.12.23 See also: https://www.w3schools.com/htmL/html_blocks.asp
	return (/^(address|article|aside|blockquote|canvas|dd|div|dl|dt|fieldset|figcaption|figure|footer|form|h1|h2|h3|h4|h5|h6|header|hr|li|main|nav|noscript|ol|p|pre|section|table|tfoot|ul|video)$/i).test(s||'');
}

function isInlineElement(s){
	//2019.12.23 See also: https://www.w3schools.com/htmL/html_blocks.asp
	return (/^(a|abbr|acronym|b|bdo|big|br|button|cite|code|dfn|em|i|img|input|kbd|label|map|object|output|q|samp|script|select|small|span|strong|sub|sup|textarea|time|tt|var)$/i).test(s||'');
}

function htmlTextOf(xNode, iLevel, bInner)
{
	var s_CRLF='\n';
	var s_sDefDocType='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';

	var _qualify_uri=function(sUri){
		return sUri;
	};

	var s_xTagsXhtml={
		  'font': 'span'
		, 'b': 'strong'
		, 'i': 'em'
		//2019.9.28 The integrated qt487-webkit forcedly changes the CSS::text-decoration:line-through to <strike>
		//However it seemed that xhtml1-transitional.dtd doesn't support the html5::del tag, the <del> tag cannot be toggled by webkit;
		//Therefore, just leave the <s> and <strike> tags there without changing to html5 tags;
		//, 's': 'del'
		//, 'strike': 'del'
		};
	var _upgrade_tagname_to_xhtml=function(sTag){
		return s_xTagsXhtml[sTag] || sTag;
	};

	var _make_indentation=function(n){
		var s='';
		while(n-->0) s+='\t';
		return s;
	};

	var _doctype=function(sDefDocType, sDefPubID, sDefSysID){
		var xDT=document.doctype, sDT;
		if(xDT){
			sDT='<!DOCTYPE html';

			var sPubID=xDT.publicId||sDefPubID||'';
			if(sPubID){
				sDT+=' PUBLIC '+'"'+sPubID+'"';
			}

			var sSysID=xDT.systemId||sDefSysID||'';
			if(sSysID){
				sDT+=' '+'"'+sSysID+'"';
			}
			sDT+='>';
		}
		return sDT||sDefDocType||'';
	};

	// http://www.javascriptkit.com/domref/nodetype.shtml
	// nodeType values
	// 1 	ELEMENT_NODE
	// 2 	ATTRIBUTE_NODE
	// 3 	TEXT_NODE
	// 4 	CDATA_SECTION_NODE
	// 5 	ENTITY_REFERENCE_NODE
	// 6 	ENTITY_NODE
	// 7 	PROCESSING_INSTRUCTION_NODE
	// 8 	COMMENT_NODE
	// 9 	DOCUMENT_NODE
	// 10 	DOCUMENT_TYPE_NODE
	// 11 	DOCUMENT_FRAGMENT_NODE
	// 12 	NOTATION_NODE

	var _get_inner_html=function(xNode, iLevel){
		var s = '';
		for(var i=0; i<xNode.childNodes.length; i++){
			s += _get_outer_html(xNode.childNodes.item(i), iLevel);
		}
		return s;
	};

	//http://syntaxsandbox.co.uk/learnhtml/blocktags.html
	//http://www.w3schools.com/htmL/html_blocks.asp
	//http://www.htmlhelp.com/reference/html40/block.html
	//http://www.w3resource.com/html/HTML-block-level-and-inline-elements.php
	//http://xahlee.info/js/html5_non-closing_tag.html
	//http://stackoverflow.com/questions/97522/what-are-all-the-valid-self-closing-elements-in-xhtml-as-implemented-by-the-maj

	var s_vTagsSelfClosing='|area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|source|track|wbr'.split('|');
	var s_vTagsNoSelfClosing='html|body|head|style|p|div|span'.split('|');
	var s_vTagsBlock='html|head|style|body|address|blockquote|center|div|p|pre|h1|h2|h3|h4|h5|h6|hr|dl|dd|dt|table|tbody|thead|tfoot|th|tr|td|ul|ol|li|fieldset|form|script|noscript|meta|link|title|footer|colgroup|col'.split('|');
	var s_vTagsInline='a|span|font|b|u|i|s|em|strong|ins|del|strike|small|sub|sup|code'.split('|');
	var s_vTagsToIgnore='frame|iframe|frameset|frame|noscript|script'.split('|');
	var s_vTextToIgnore='<![CDATA[;]]>;/*<![CDATA[*/;/*]]>*/;//<![CDATA[;//]]>'.split(';');
	var s_vBoolAttr='checked,compact,declare,defer,disabled,ismap,multiple,noresize,noshade,nowrap,readonly,selected'.split(',');
	var s_vHtmlFontSize=[7, 10, 12, 13.5, 18, 24, 36];

	var _is_boolean_attr=function(k){return s_vBoolAttr.indexOf(k||'')>=0};

	var _htmlEncode=function(s){

		//http://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
		//http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=dec
		s=s.replace(/&/g,		'&amp;');
		s=s.replace(/</g,		'&lt;');
		s=s.replace(/>/g,		'&gt;');
		s=s.replace(/\"/g,		'&quot;');
		s=s.replace(/\'/g,		'&apos;');

		//https://mathiasbynens.be/notes/javascript-escapes
		//http://www.regular-expressions.info/nonprint.html
		//http://www.fileformat.info/info/unicode/char/a0/index.htm
		//http://www.fileformat.info/info/unicode/char/2002/index.htm
		//http://www.fileformat.info/info/unicode/char/2003/index.htm

		s=s.replace(/\xA0/g,		'&nbsp;');
		s=s.replace(/\u2002/g,		'&ensp;');
		s=s.replace(/\u2003/g,		'&emsp;');

		//Do not translate Tabs in 'nodeValue', just keep them there if any;
		//s=s.replace(/\t/g,		'&nbsp; &nbsp; &nbsp; &nbsp; '); //&emsp;

		s=s.replace(/  /g,		'&nbsp; '); //&nbsp; = non-breaking space;

		return s;
	};

	var xTmpDiv=document.createElement('div');
	var _get_outer_html=function(xNode, iLevel){
		var s = '';
		switch(xNode.nodeType){
			case Node.DOCUMENT_NODE:

				s += _get_inner_html(xNode, iLevel+1);

				break;

			case Node.ELEMENT_NODE:

				var sTag=xNode.nodeName.toLowerCase();
				var sTagSubst=_upgrade_tagname_to_xhtml(sTag);

				//ignore frames/scripts...;
				if(s_vTagsToIgnore.indexOf(sTag)<0){

					var bNewLine=(s_vTagsBlock.indexOf(sTagSubst)>=0);

					if(bNewLine) s += (s_CRLF + _make_indentation(iLevel));

					s += ('<' + sTagSubst);

					var sCls='';
					for(var j=0; j < xNode.attributes.length; j++){

						var attr = xNode.attributes.item(j);
						var sKey=(attr.nodeName||'').toLowerCase(), sVal=attr.nodeValue||'';

						//if(sVal.indexOf('"')>=0)
						{
							//2016.6.9 MS-Word sucks! and gives malformed CSS when copying HTML, like this:
							//<span style="font-size:42.0pt;mso-bidi-font-size:12.0pt;font-family:AAA;mso-ascii-font-family:"Times New Roman";
							//mso-hansi-font-family:"Times New Roman";mso-bidi-font-family:"Times New Roman";color:red;mso-font-width:80%;
							//mso-font-kerning:1.0pt;mso-ansi-language:EN-US;mso-fareast-language:ZH-CN;mso-bidi-language:AR-SA">TEXT</span>
							sVal=sVal.replace(/\"/g, '\'');
						}

						//Redirect to local filenames;
						if(sTag=='img' && sKey=='src'){ //img;

							//2015.6.18 gzhaha reported an issue:
							//Draging an image inside a document, its location may alter with current document's URL applied,
							//within v7x, the document's URL is dynamic and varies after db reopens,
							//that's to say, the altered image would not work after db reopens;
							//workaround: match the characteristic URL by RE pattern and forcedly clear the location path;
							//for example: file://82173928/Organizer/data/0/2_7/3/4/5.cpmv/6/7/9/btn_about.png
							//Note that SSG path is supposed to contain only ASCII characters [0-9a-z_.];

							sVal=sVal.replace(/^file:\/\/\d+\/Organizer\/data\/([0-9a-z_\.]+?\/)+(.+)$/i, '$2');

						}else if(sTag=='meta' && sKey=='content'){ //meta/charset;
							if(sVal.indexOf('text/html')>=0 && sVal.indexOf('charset')>0){
								sVal='text/html; charset=utf-8';
							}
						}else if(sTag=='a' && sKey=='href'){ //a;
							if(sVal){
								if(sVal.indexOf('javascript:')==0){
									sVal='';
								}else{
									sVal=_qualify_uri(sVal);
								}
							}
						}else if(sTag=='a' && sKey=='title'){ //a;
							if(sVal){
								//2015.6.24 consider of special characters in <a title='...'>;
								sVal=_htmlEncode(sVal);
							}
						}else if(sKey.match(/^on(.+)/)){ //onX... events;
							sVal='';
						}else if(sTag=='font'){
							if(sKey=='size'){
								var n=parseInt(''+sVal); if(n<=0 || n>s_vHtmlFontSize.length) n=3;
								if(sCls) sCls+='; ';
								sCls+='font-size: ' + s_vHtmlFontSize[n-1] + 'pt';
							}else if(sKey=='face'){
								if(sCls) sCls+='; ';
								sCls+='font-family: '+sVal;
							}else if(sKey=='color'){
								if(sCls) sCls+='; ';
								sCls+='color: '+sVal;
							}else if(sKey=='style'){ //webkit may use this field;
								if(sCls) sCls+='; ';
								sCls+=sVal;
							}
							sKey='';
						}

						if(sKey=='class'){

							//2014.12.20 elimiate webkit specific classes;
							var vCls=(sVal||'').split(' '), v='';
							for(var i in vCls){
								var a=vCls[i]||'';
								if(a.indexOf('Apple-style-')==0 || a.indexOf('Apple-tab-')==0){
									continue;
								}
								if(v) v+=' '; v+=a;
							}
							sVal=v;
							if(!sVal) sKey='';

						}else if(sKey==='style'){
							//2020.2.9 Html text copied from in VSCode: <div style='...; white-space: pre;'> produces duplicate line-breaks;
							//workaround: simply clear the 'white-space' css attribute;
							//https://www.w3school.com.cn/cssref/pr_text_white-space.asp
							if(sTag==='p' || sTag==='div'){
								//app.log(sVal);
								sVal=sVal.replace(/white-space:\s*(pre|pre-wrap|pre-line|nowrap)[;\s]*/gi, '');
							}
						}

						if(sKey){

							//2015.1.8 xhtml doesn't allow minimized attributes;
							//http://www.pubpixel.com/article/18/what-are-html-xhtml-boolean-attributes-and-how-do-i-use-them
							if(!sVal && _is_boolean_attr(sKey)){
								sVal=sKey;
							}

							s += (' ' + sKey + '=' + '\"' + sVal + '\"');
						}
					}

					if(sCls){
						s += ' ' + 'style';
						s += '=' + '\"' + sCls.replace('"', '\'') + '\"';
					}

					//if(!xNode.hasChildNodes() && s_vTagsNoSelfClosing.indexOf(sTag)<0){
					if(!xNode.hasChildNodes() && s_vTagsSelfClosing.indexOf(sTag)>=0){

						s += ' />';

					}else{

						s += '>';

						var bPreCode=(sTag=='pre' || sTag=='code');
						var bSingleLine=(sTag.search(/^(title|footer)$/i)==0); //2018.4.2 avoid line-break within the <title/footer> tags;

						if(sTag=='body'){
							//2014.12.27 'sSelection': inteneded for composing a complete HTML document with given HTML content;
							//For this project, it's no use but a placeholder;
							var sSelection;
							if(sSelection){
								s += sSelection;
							}else{
								s += _get_inner_html(xNode, iLevel+(bNewLine?1:0));
							}
						}else{
							if(sTag=='style'){
								var vLines=_trim(xNode.innerHTML).split('\n');
								for(var i in vLines){
									s += (s_CRLF + _make_indentation(iLevel+1) + _trim(vLines[i]));
								}
							}else if(bPreCode){
								s += s_CRLF;
								s += xNode.innerHTML;
							}else{
								s += _get_inner_html(xNode, iLevel+(bNewLine?1:0));
							}
						}

						if(bNewLine && !bPreCode && !bSingleLine) s += (s_CRLF + _make_indentation(iLevel));

						//2015.2.2 Trailing Returns have been trimmed while handling the last TEXT_NODE;
						//if(bNewLine && !bPreCode){
						//	if(!s.match(/\n+$/)) s += s_CRLF;
						//	s += _make_indentation(iLevel);
						//}

						s += ('</' + sTagSubst + '>');
					}
				}

				break;

			case Node.TEXT_NODE:

				var sVal=(xNode.nodeValue||'').replace(/^[\r\n\t]+|[\r\n\t]+$/g, ''); //preserve leading Tabs, but not trailing Tabs;

				//2015.2.15 The <head> section wouldn't contain literal text content execpt for blank spaces,
				//it's safe to trim all leading and trailing blankspaces for making indentation in HTML source;
				var xParent=xNode.parentNode;
				if(xParent && xParent.nodeName.toLowerCase()=='head'){
					sVal=_trim(sVal);
				}

				//2015.2.2 Within Webkit, 'xNode.nodeValue' always returns text content with all '&nbsp;' evaluated,
				//it's no way to determine if leading blankspaces should be trimmed or preserved for HTML source indentation;
				//so we assumed that all HTML source should use 'Tab' for indentation with all blankspaces preserved as HTML entities '&nbsp;'
				if(sVal){
					//2015.2.2 Avoid using Blankspaces for HTML indentation, Tab characters are proposed for this purpose instead;
					s+=_htmlEncode(sVal);
				}

				break;
		}
		return s;
	};

	if(typeof(iLevel)!='number') iLevel=0;

	if(!xNode){
		xNode=document;
		iLevel=-1;
	}

	var sHtml='NULL Element';
	if(xNode){
		sHtml=bInner ? _get_inner_html(xNode, iLevel) : _get_outer_html(xNode, iLevel);
	}

	sHtml=_trim(sHtml);

	if(!bInner){
		var sDT=_doctype(s_sDefDocType);
		if(sDT){
			sHtml=sDT+s_CRLF+sHtml
		}
	}

	return sHtml;
};

function traverseDomBranch(xElm, iLevel, xUserData, xActPre, xActPost)
{
	if(xActPre) xActPre(xElm, iLevel, xUserData);
	traverseDomChildren(xElm, iLevel+1, xUserData, xActPre, xActPost);
	if(xActPost) xActPost(xElm, iLevel, xUserData);
}

function traverseDomChildren(xElm, iLevel, xUserData, xActPre, xActPost)
{
	for(var i=0; i<xElm.childNodes.length; i++){
		traverseDomBranch(xElm.childNodes.item(i), iLevel, xUserData, xActPre, xActPost);
	}
}

function traverseSelection(xAct, iLevel, xUserData)
{
	var xRng=getSelRange();

	if(xAct && xRng && xRng.commonAncestorContainer){

		var xStart=xRng.startContainer, xEnd=xRng.endContainer;

		//if(xStart.nodeType==Node.TEXT_NODE) xStart=xStart.parentNode;
		//if(xEnd.nodeType==Node.TEXT_NODE) xEnd=xEnd.parentNode;

		var bEntering=false, bLeaving=false;
		var _act_on_elm=function(xElm, iLevel, xUserData){

			if(xElm===xStart){bEntering=true; bLeaving=false;}

			if(bEntering){
				if(!bLeaving){
					xAct(xElm, iLevel, xUserData);
				}
			}

			if(xElm===xEnd){bEntering=false; bLeaving=true;}
		};

		var xElm=xRng.commonAncestorContainer;

		//if(xElm.nodeType===Node.TEXT_NODE) xElm=xElm.parentNode;
		if(xElm.nodeType===Node.TEXT_NODE){
			xAct(xElm, 0, xUserData);
		}else{
			traverseDomBranch(xElm, iLevel, xUserData, _act_on_elm, null);
		}
	}
};
