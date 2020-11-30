
//sValidation=nyfjs
//sCaption=Insert code block ...
//sHint=Insert a block of source code into the current content
//sCategory=MainMenu.Insert; Context.HtmlEdit; Context.RichEdit
//sCondition=CURDB; DBRW; CURINFOITEM; FORMATTED; EDITING;
//sID=p.Ins.CodeBlock
//sAppVerMin=7.0
//sShortcutKey=
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

try{
	var xNyf=new CNyfDb(-1);

	if(xNyf.isOpen()){

		if(!xNyf.isReadonly()){

			if(plugin.isContentEditable()){

				var sEditor=plugin.getCurEditorType().toLowerCase();
				if(sEditor=='htmledit'){

					var _compare=function(x, y){
						if(x>y) return 1;
						else if(x<y) return -1;
						else return 0;
					};

					var xFn=new CLocalFile(plugin.getPathToDomScripts(), 'highlight.pack.js');
					var sHljsCode=xFn.loadText('auto');
					if(sHljsCode){

						var vLangsSupported=[];
						{
							//2016.12.1 168 languages supported by highlight.pack.js for now;
							//1c;abnf;accesslog;actionscript;ada;apache;applescript;arduino;armasm;asciidoc;aspectj;autohotkey;autoit;avrasm;
							//awk;axapta;bash;basic;bnf;brainfuck;cal;capnproto;ceylon;clean;clojure;clojure-repl;cmake;coffeescript;coq;cos;
							//cpp;crmsh;crystal;cs;csp;css;d;dart;delphi;diff;django;dns;dockerfile;dos;dsconfig;dts;dust;ebnf;elixir;elm;erb;
							//erlang;erlang-repl;excel;fix;flix;fortran;fsharp;gams;gauss;gcode;gherkin;glsl;go;golo;gradle;groovy;haml;
							//handlebars;haskell;haxe;hsp;htmlbars;http;inform7;ini;irpf90;java;javascript;json;julia;kotlin;lasso;ldif;less;
							//lisp;livecodeserver;livescript;lsl;lua;makefile;markdown;mathematica;matlab;maxima;mel;mercury;mipsasm;mizar;
							//mojolicious;monkey;moonscript;nginx;nimrod;nix;nsis;objectivec;ocaml;openscad;oxygene;parser3;perl;pf;php;pony;
							//powershell;processing;profile;prolog;protobuf;puppet;purebasic;python;q;qml;r;rib;roboconf;rsl;ruby;ruleslanguage;
							//rust;scala;scheme;scilab;scss;smali;smalltalk;sml;sqf;sql;stan;stata;step21;stylus;subunit;swift;taggerscript;tap;
							//tcl;tex;thrift;tp;twig;typescript;vala;vbnet;vbscript;vbscript-html;verilog;vhdl;vim;x86asm;xl;xml;xquery;yaml;zephir

							//2016.12.1 invoke highlight.pack.js;
							eval.call(null, sHljsCode);
							var sLangsSupported=eval.call(null, 'hljs.listLanguages();').toString();

							vLangsSupported=sLangsSupported.split(',');
							vLangsSupported.sort(function(x,y){
								var j=_compare(x, y);
								return (j==0) ? 0 : j;
							});

						}

						var sCfgKey1='InsCodeBlock.Html.iLang', sCfgKey2='InsCodeBlock.Html.bAutoNumber', sCfgKey3='InsCodeBlock.Html.bNewLineBefore', sCfgKey4='InsCodeBlock.Html.bNewLineAfter';

						var sSelTxt = plugin.getSelectedText(-1, false);
						var vLangs = [];
						{
							for(var i=0; i<vLangsSupported.length; ++i){
								var x=vLangsSupported[i];
								vLangs.push(x); //vLangs.push(x + ' ('+(i+1)+')');
							}
							vLangs.splice(0, 0, 'auto-detect', 'no-highlight');
						}

						var vOpts=[
							(localStorage.getItem(sCfgKey2)||'true')+'|'+_lc2('AutoNum', 'Auto-numbering')
							, (localStorage.getItem(sCfgKey3)||'true')+'|'+_lc2('NewLineBefore', 'Preserve new line before')
							, (localStorage.getItem(sCfgKey4)||'true')+'|'+_lc2('NewLineAfter', 'Preserve new line after')
						];

						var vFields=[
							{sField: 'textarea', sLabel: _lc2('SourceCode', 'Source code to insert as a code block'), sInit: sSelTxt}
							, {sField: 'combolist', sLabel: _lc2('Language', 'Language for syntax highlighting'), vItems: vLangs, sInit: localStorage.getItem(sCfgKey1)||''}
							, {sField: 'check', sLabel: '', vItems: vOpts}
						];

						var vRes=input(plugin.getScriptTitle(), vFields, {nMinSize: [900, 560], nSpacing: 10, vMargins: [6, 0, 30, 0], bVert: true});
						if(vRes && vRes.length>=2){
							var sSrc=vRes[0], iLang=parseInt(vRes[1]), vChk=vRes[2];
							if(sSrc && iLang>=0 && vChk && vChk.length>=3){

								var bAutoNumber=vChk[0], bNewLineBefore=vChk[1], bNewLineAfter=vChk[2];

								localStorage.setItem(sCfgKey1, iLang);
								localStorage.setItem(sCfgKey2, bAutoNumber?'true':'false');
								localStorage.setItem(sCfgKey3, bNewLineBefore?'true':'false');
								localStorage.setItem(sCfgKey4, bNewLineAfter?'true':'false');

								var sLang='';
								{
									if(iLang==0) sLang='';
									else if(iLang==1) sLang='no-highlight';
									else if(iLang>=2) sLang='lang-'+vLangsSupported[iLang-2];
								}

								sSrc=sSrc.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

								var sIdOfCode='ID_'+ (new Date()).getTime().toString(16).toUpperCase();

								var sHtml='<pre><code id="%sCodeBlockID%" class="%sLangTag%">%sSourceCode%</code></pre>'
								.replace(/%sCodeBlockID%/gi, sIdOfCode)
								.replace(/%sLangTag%/gi, sLang)
								.replace(/%sSourceCode%/gi, sSrc)
								;

								if(bNewLineBefore) sHtml='<div><br /></div>'+sHtml;
								if(bNewLineAfter) sHtml+='<div><br /></div>';

								plugin.replaceSelectedText(-1, sHtml, true);

								var xDomJsFn=new CLocalFile(plugin.getScriptFile()); xDomJsFn.changeExtension('dom.js');
								if(xDomJsFn.exists()){
									var sDomJsCode=xDomJsFn.loadText('auto');
									if(sDomJsCode){

										var sRunJsCode='window.doSyntaxHighlighting("%sCodeBlockID%"); window.makeLinkWithHighlightStyle(); window.autoNumberCodeLines("%sCodeBlockID%", %bAutoNumber%);'
										.replace(/%bAutoNumber%/ig, bAutoNumber?'true':'false')
										.replace(/%sCodeBlockID%/ig, sIdOfCode)
										;

										if(plugin.runDomScript(-1, sHljsCode+';'+sDomJsCode+';'+sRunJsCode)){
											//done;
										}
									}else{
										alert('DOM/JS code not found. You may need to re-install the software.'+'\n\n'+xDomJsFn);
									}
								}else{
									alert('DOM/JS code not found. You may need to re-install the software.'+'\n\n'+xDomJsFn);
								}
							}
						}

					}else{
						alert('Highlight.js not found.' + '\n\n' + xFn);
					}

				}else if(sEditor=='richedit'){

					var sCfgKey1='InsCodeBlock.Rich.iLang';

					var sSelTxt = plugin.getSelectedText(-1, false);
					var vLids=[], vTitles=[];
					{
						var vLines=(platform.languagesForSyntaxHighlight('\t')||'').split('\n');
						for(var i=0; i<vLines.length; ++i){
							var v=(vLines[i]||'').split('\t');
							if(v && v.length>0){
								var sLid=v[0], sTitle=sLid; if(v.length>1) sTitle=v[1] || v[0];
								if(sLid && sTitle){
									vLids.push(sLid);
									vTitles.push(sTitle);
								}
							}
						}
					}

					var vFields=[
						{sField: 'textarea', sLabel: _lc2('SourceCode', 'Source code to insert as a code block'), sInit: sSelTxt}
						, {sField: 'combolist', sLabel: _lc2('Language', 'Language for syntax highlighting'), vItems: vTitles, sInit: localStorage.getItem(sCfgKey1)||''}
					];

					var vRes=input(plugin.getScriptTitle(), vFields, {nMinSize: [900, 560], nSpacing: 10, vMargins: [6, 0, 30, 0], bVert: true});
					if(vRes && vRes.length>=2){
						var sSrc=vRes[0], iLang=parseInt(vRes[1]), sStyle='';
						if(sSrc && iLang>=0){

							localStorage.setItem(sCfgKey1, iLang);

							var sHtml=platform.syntaxHighlight(sSrc, vLids[iLang], sStyle);
							plugin.replaceSelectedText(-1, sHtml, true);
						}
					}

				}

			}else{
				alert(_lc('Prompt.Warn.ReadonlyContent', 'Cannot modify the content opened as Readonly.'));
			}

		}else{
			alert(_lc('Prompt.Warn.ReadonlyDb', 'Cannot modify the database opened as Readonly.'));
		}

	}else{
		alert(_lc('Prompt.Warn.NoDbOpened', 'No database is currently opened.'));
	}
}catch(e){
	alert(e);
}
