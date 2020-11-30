
/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2016 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

var _dbgShowObj=function(obj){
	var s='';
	if(obj){

		var type=typeof(obj);
		s='TYPE = '+type;

		if(type == 'object'){
			for(var x in obj){

				if(x=='typeDetail') continue; //weird things with in IE7

				var val=obj[x];
				if(val){
					type=typeof(val);
					if(type=='string' || type=='number'){
						val=obj[x];
					}else if(type=='function'){
						val='{function}';
					}else{
						val='['+type+']';
					}
				}else{
					val='?';
				}

				if(s) s+='\n';

				s+=x;
				s+=' = ';
				s+=val;
			}
		}else if(type=='string'){
			s+='\n';
			s+=obj;
		}else{
		}
	}
	alert(s);
}

var validateFilename=function(s){
	s=s||'';
	s=s.replace(/[\*\?\.\(\)\[\]\{\}\<\>\\\/\!\$\^\&\+\|,;:\"\'`~@#]/g, ' ');
	s=s.replace(/\s{2,}/g, ' ');
	s=_trim(s);
	if(s.length>64) s=s.substr(0, 64);
	s=_trim(s);
	s=s.replace(/\s/g, '_');
	return s;
};

var htmlEncode=function(s){
	//http://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
	//http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=dec
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

var htmlDecode=function(s){
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

var percentEncode=function(sTxt, sExcl, sIncl){
	var sRes='';
	if(sTxt){
		var v=new CByteArray(sTxt, 'utf8');
		if(!v.isEmpty()){
			if(v.percentEncoded){
				//By default, this function will encode all characters that are not one of the following:
				//ALPHA ("a" to "z" and "A" to "Z") / DIGIT (0 to 9) / "-" / "." / "_" / "~"
				sRes=v.percentEncoded(sExcl||'', sIncl||'').toString('utf8');
			}else{
				sRes=sTxt;
			}
		}
	}
	return sRes;
};

var percentDecode=function(sTxt){
	var sRes='';
	if(sTxt){
		var v=new CByteArray(sTxt, 'utf8');
		if(!v.isEmpty()){
			if(v.percentDecoded){
				sRes=v.percentDecoded().toString('utf8');
			}else{
				sRes=sTxt;
			}
		}
	}
	return sRes;
};

var urlFromLocalFile=function(sFn, bPercentEncoding, sExcl, sIncl){
	var sUrl=''; sFn=(sFn||'').toString().replace(/\\/g, '/');
	if(sFn){

		if(bPercentEncoding){
			sFn=percentEncode(sFn, (sExcl || '/:'), sIncl);
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
};

var localFileFromUrl=function(sUrl, bPercentDecoding){
	var sFn='', sScheme='file://'; sUrl=(sUrl||'').toString();
	if(sUrl.search(/^file:\/\//i)==0){

		sFn=sUrl.replace(/^file:\/\//i, '');

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
			sFn=percentDecode(sFn);
		}
	}
	return sFn;
};

var changeHtmlCharset=function(sHtml, sCodec){

	//<meta http-equiv=Content-Type content="text/html; charset=unicode">
	//<meta http-equiv=Content-Type content="text/html; charset=windows-1253">

	var s=(sHtml||'').toString(); sCodec=(sCodec||'').toString().replace(/^\s+|\s+$/g, '');
	s=s.replace(/(<meta\s+http-equiv=(['"]?)Content-Type\2\s+content=(['"])text\/html;\s+charset=)\s*([\w-]+)\s*(\3\s*>)/im, function(s0, s1, s2, s3, s4, s5){
		if(sCodec){
			return s1+sCodec+s5;
		}else{
			return '';
		}
	});
	return s;
};

var substituteUriWithinHtml=function(sHtml, sUri0, sUri2, bWithQuotations){

	var _replace=function(s, sFrom, sTo){
		var sRes='', sRight=s;
		while(sRight && sFrom){
			var p=sRight.indexOf(sFrom);
			if(p>=0){
				sRes+=sRight.substr(0, p)+sTo;
				sRight=sRight.substr(p+sFrom.length);
			}else{
				sRes+=sRight;
				break;
			}
		}
		return sRes;
	};

	var sRes=sHtml;
	if(sUri0!=sUri2){

		sRes=_replace(sRes, ( '"'+sUri0+'"' ), ( '"'+sUri2+'"' ) );
		sRes=_replace(sRes, ( "'"+sUri0+"'" ), ( "'"+sUri2+"'" ) );

		if(!bWithQuotations && sRes==sHtml){
			//in case of urls with no quotation marks;
			sRes=_replace(sRes, sUri0, sUri2);
		}
	}

	return sRes;
};

var substituteUrisWithinHtml=function(sHtml, sTagNames, xHandler){

	//2016.4.14 detect linked images/links and then redirect them accordingly by calling app-defined xHandler;

	var sNew=sHtml||'', vTagNames=(sTagNames||'img,link').toString().toLowerCase().replace(/[,;\s-+]/g, '|').split('|');
	if(sNew && xHandler && vTagNames.length>0){

		//2013.11.13 MSOutlook embeds images with different filenames in <v:imageata> & <img>;
		//<v:imagedata src="~jj5C7A_files/image001.jpg" o:href="cid:image003.jpg@01CEDF8C.24786AD0"/>
		//<![if !vml]><img width=385 height=326 src="~jj5C7A_files/image001.jpg" v:shapes="Picture_x0020_1"><![endif]>
		//Track the <img ...> tag for linked image filenames, but with <v:imagedata src=...> ignored;

		//2016.5.12 For MS-Outlook, the <v:imagedata o:href='cid:...'> stands for files in attachments area of messages;
		//However, we still need to retrieve image files from <img src='...'> in the HTML content,
		//as all the linked images are already present in the accompanying sub folder when MS-Outlook exports the HTML contents;
		//As for the attached files, it's handled later on by calling to MSOutlook OLE APIs;

		//2016.5.8 The RegExp version of the function not working; As QRegExp doesn't work well with the multi-line option;
		var _extract_html_elements__NOT_WORKING=function(s, sTagName, vElms){
			if(s && sTagName && vElms){
				var sPat='<%tag%\\b.*?>'.replace('%tag%', sTagName);
				var m, xRE=new RegExp(sPat, 'igm');
				while(m=xRE.exec(s)){
					var sElm=m[0];
					if(sElm && vElms.indexOf(sElm)<0){
						vElms.push(sElm);
					}
				}
			}
		};

		var _extract_html_elements__2222=function(s, sTagName, vElms){
			if(s && vElms){

				//2016.5.8 MS-Office exports HTML contents with line-breaks, there may be no blankspaces but linebreaks after the tag '<img', like this:
				//<span lang=EN-US style='font-family:"Times New Roman","serif"'><img
				//width=789 height=43 src=“xx_files/image003.png"></span><span lang=EN-US><br>
				//</span><span lang=EN-US style='font-family:"Times New Roman","serif"'><img
				//width=249 height=35 src=“xx_files/image004.png"></span>

				var sElm, xRE=new RegExp('<'+sTagName+'[\\r\\n\\s]', 'i');
				while(s){
					sElm='';
					var p=s.search(xRE);
					if(p<0) break;
					s=s.substr(p); //+sTag.length
					p=s.indexOf('>');
					if(p>0){
						sElm=s.substr(0, p+1);
						s=s.substr(p+1);
					}else if(p<0){
						sElm=s;
						s='';
					}

					if(sElm && vElms.indexOf(sElm)<0){
						vElms.push(sElm);
					}
				}
			}
		};

		var _extract_html_elements=function(s, sTagName, vElms){
			if(s && vElms){

				//2016.5.8 MS-Office exports HTML contents with line-breaks, there may be no blankspaces but linebreaks after the tag '<img', like this:
				//<span lang=EN-US style='font-family:"Times New Roman","serif"'><img
				//width=789 height=43 src=“xx_files/image003.png"></span><span lang=EN-US><br>
				//</span><span lang=EN-US style='font-family:"Times New Roman","serif"'><img
				//width=249 height=35 src=“xx_files/image004.png"></span>

				var sElm;
				while(s){
					sElm='';
					var p=s.indexOf('<'+sTagName.toLowerCase()); if(p<0) p=s.indexOf('<'+sTagName.toUpperCase());
					if(p<0) break;
					s=s.substr(p); //+sTag.length
					p=s.indexOf('>');
					if(p>=0){
						sElm=s.substr(0, p+1);
						s=s.substr(p+1);
					}else if(p<0){
						sElm=s;
						s='';
					}

					if(sElm && vElms.indexOf(sElm)<0){
						vElms.push(sElm);
					}
				}
			}
		};

//		var _extract_attr_value=function(s, sAttrName){
//			var sVal='';
//			if(s && sAttrName){
//				//e.g. <img src="cid:687392502@12112013-049d" />
//				//e.g. <img src="image004.gif" alt="cid:image001.png@01D0D9C1.74D05430" v:shapes="Picture_x0020_2">
//				//var re=new RegExp('\\b'+sAttrName+'=([\\\'\\"])(.+?)\\1', 'ig');
//				var re=new RegExp('\\b'+sAttrName+'=([\'"])(.+?)\\1', 'ig');
//				var m=re.exec(s);
//				if(m && m[1] && m[2]){
//					sVal=m[2].replace(/^\s+|\s+$/g, '').replace(/[\r\n]+/g, '');
//				}
//			}
//			return sVal;
//		};

		var _extract_attr_value=function(s, sAttrName){
			var sVal='';
			if(s && sAttrName){
				//e.g. <img src="cid:687392502@12112013-049d" />
				//e.g. <img src="image004.gif" alt="cid:image001.png@01D0D9C1.74D05430" v:shapes="Picture_x0020_2">
				var xRE=new RegExp('\\b'+sAttrName+'=([\'"])(.*?)\\1', 'im');
				var m=s.match(xRE);
				if(m && m[2]){
					sVal=m[2].replace(/^\s+|\s+$/g, '').replace(/[\r\n]+/g, '');
				}
			}
			return sVal;
		};

		if(0 && sNew.indexOf('<!--[if gte vml 1]>')>=0){ //No longer required.

			//2016.5.6 what a mess with filenames in HTML contents exported by MS-Outlook, e.g.
			//<img src="xxx_files/image004.gif" alt="cid:image001.png@01D0D9C1.74D05430" v:shapes="Picture_x0020_2">
			//it indicates that the image file is located at "xxx_files/image004.gif", but with the filename 'image001.png' in the attachments area;

			//Here's another sample code with image file names that is totally in a mess:
			//<!--[if gte vml 1]><v:shape id=...>...
			//<v:imagedata src="__nyf7_import_msoutlook_items_files/image001.png" o:href="cid:image008.png@01D1A137.70036940"/>
			//</v:shape><![endif]--><![if !vml]><img width=808 height=517
			//src="__nyf7_import_msoutlook_items_files/image002.jpg"
			//alt="cid:image008.png@01D1A137.70036940" v:shapes="Picture_x0020_7"><![endif]></span></p>

			//In order to fix the file names, composed the regexp to match the image filenames, and make corrections to filenames accordingly;

			//It's said that Qt::QRegExp doesn't handle well multi-line patterns, as matter of fact, it simply doesn't work in this case;
			//therefore a workaround: the <CRLN> temporarily substitutes for all of [\r\n].
			//see also: http://stackoverflow.com/questions/20660579/can-qregexp-do-multiline-and-dotall-match
			//see also: http://doc.qt.io/qt-4.8/qregexp.html

			sNew=sNew.replace(/\r\n/g, '\n').replace(/\n/g, '<CRLN>'); //line-break substitution;

			var xRE=/(<!--\[if\s+gte\s+vml\s+1\]>.*?<v:imagedata\s+src=")(.*?)("\s+o:href="cid:)(image\d{3}\.(png|jpg|gif|bmp|tif))(@[\w\.\-]+"\/>.*?<!\[endif\]-->.*?<!\[if\s+!vml\]>.*?<img\b.+?src=")(.*?)(".*?>.*?<!\[endif\]>)/igm;
			sNew=sNew.replace(xRE, function(s0, s1, s2, s3, s4, s5, s6, s7, s8){
				if(s2 && s4 && s7){
					var sDir=new CLocalFile(s2).getDirectory(false) || new CLocalFile(s7).getDirectory(false);
					if(!sDir || sDir=='./'){
						s2=s7=s4;
					}else{
						s2=s7=new CLocalFile(sDir, s4);
					}
				}
				return s1+s2+s3+s4+s6+s7+s8; //ignore +s5 => (png|jpg|gif|bmp|tif)
			});

			sNew=sNew.replace(/<CRLN>/igm, '\n'); //restore normal line-breaks;
		}
var _vLog=[];
		for(var j in vTagNames){
			var sTagName=vTagNames[j];
			if(sTagName){
				var vObjs=[];
				{
					var sAttrName='src';
					{
						if(sTagName=='link') sAttrName='href';
						else if(sTagName=='a') sAttrName='href';
					}
					if(sAttrName){
						var vElms=[]; _extract_html_elements(sNew, sTagName, vElms);
						for(var i in vElms){
							var sElm=vElms[i].replace(/[\r\n]+/g, ' ');
							var sObj=_extract_attr_value(sElm, sAttrName);
//_vLog.push('');
//_vLog.push('elm['+i+']='+sElm);
//_vLog.push('uri['+i+']='+sObj);
							if(sObj){
								if(vObjs.indexOf(sObj)<0){
									vObjs.push(sObj);
								}
							}
						}
					}
				}
				for(var i in vObjs){
					var sObj=vObjs[i];
					if(sObj){
						//var sPat=sUri.replace(/([\.\/\\\!\[\]])/ig, '\\$1');
						//sNew=sNew.replace(new RegExp(sPat, 'ig'), sUriNew);
						sNew=substituteUriWithinHtml(sNew, sObj, xHandler(sObj, sTagName));
					}
				}
			}
		}
if(_vLog.length>0){
textbox(
	{
		sTitle: plugin.getScriptTitle()
		, sDescr: 'Debug info'
		, sDefTxt: _vLog.join('\n')
		, bReadonly: true
		, bWordwrap: false
		, nWidth: 80
		, nHeight: 60
		, bFind: false
	}
);
}
	}
	return sNew;
};

var getUniqueSsgFileName=function(xNyf, sSsgPath, sSsgName0){

	var sRes='';

	sSsgPath=sSsgPath ? sSsgPath.toString(): ''; //in case of non-string wrapped objects, e.g. CLocalFile;
	sSsgName0=sSsgName0 ? sSsgName0.toString(): 'untitled';

	if(xNyf && sSsgPath && sSsgName0){
		var xFn=new CLocalFile(sSsgPath, sSsgName0), n=1, sMagic='';
		var sTitle=xFn.getTitle(), sExt=xFn.getExtension(false); //false: without dot;
		do{
			var sName=sTitle; if(sMagic) sName=sName+'_'+sMagic; if(sExt) sName+=('.'+sExt);
			var f=new CLocalFile(sSsgPath, sName);
			if(!xNyf.entryExists(f.toString())){
				sRes=sName;
				break;
			}
			sMagic=''+n; n++;
		}while(n<=0xffff);
	}

	return sRes;
};

var importAccompanyingObjsWithinHtml=function(xNyf, sSsgPath, sHtml, sDir, xActPre, xActPost){

	if(sHtml){

		sSsgPath=sSsgPath ? sSsgPath.toString(): ''; //in case of wrapped objects;
		sDir=sDir ? sDir.toString() : '';

		sHtml=substituteUrisWithinHtml(sHtml, 'img,link', function(sObj, sTagName){

			var u=sObj.toString();

			if(!xActPre || xActPre(sObj, sTagName)){

				var nBytes=-1;

				//2011.12.3 test if it's javascript:, mailto:, xxxx://, or contains any of ?/*/#;
				if(u.search(/^javascript:/i)<0 && u.search(/^mailto:/i)<0 && u.search(/^\w+?:\/\//i)<0 && u.search(/[\?\*\#]/)<0){

					if(u.search(/(\.jpg|\.jpeg|\.gif|\.png|\.bmp|\.swf|\.css)$/i)>0){ //images or styles;

						var f, sLeaf;
						{
							if(u.search(/^[\/\\].+/)==0 || u.search(/^[a-z]\:[\/\\].+/i)==0){
								//absolute path; e.g. "/Users/uid/1.png", "C:/Users/uid/2.png"
								f=new CLocalFile(u);
							}else if(u.search(/^\.[\/\\].+/)==0 ){
								//relative path with a prefix dot; e.g. "./xxx.files/image001.png"
								f=new CLocalFile(sDir, u.substr(2));
							}else{
								//relative path with no prefix dots, it may be NON-ASCII chars; e.g. "NON-ASCIIxxx.files/image001.png"
								f=new CLocalFile(sDir, u);
							}
							sLeaf=f ? f.getLeafName() : '';
						}

						if(f && sLeaf){
							var xSsg=new CLocalFile(sSsgPath, sLeaf);
							if(f.exists()){
								if(!xNyf.fileExists(xSsg.toString()) || xNyf.getFileSize(xSsg.toString())!=f.getFileSize()){
									sLeaf=getUniqueSsgFileName(xNyf, sSsgPath, sLeaf);
									if(sLeaf){
										xSsg=new CLocalFile(sSsgPath, sLeaf);
										nBytes=xNyf.createFile(xSsg, f);
									}
								}
								u=percentEncode(xSsg.getLeafName());
							}else if(xNyf.fileExists(xSsg.toString())){
								//2016.5.13 consider of the case that the image is already present in SSG;
								u=percentEncode(xSsg.getLeafName());
							}
						}
					}

				}else if(u.search(/^file:\/\//i)==0){ //consider of full file:// paths;

					var bImg=(sTagName=='src' && u.search(/(\.jpg|\.jpeg|\.gif|\.png|\.bmp|\.swf)$/i)>0);
					var bCss=(sTagName=='href' && u.search(/\.css$/i)>0);

					if(bImg || bCss){ //images or styles;
						var sFn=localFileFromUrl(u, true);
						if(sFn){
							sFn=xNyf.evalRelativePath(sFn);
							if(sFn){
								var f=new CLocalFile(sFn), sLeaf=f.getLeafName();
								if(f.exists() && sLeaf){
									var xSsg=new CLocalFile(sSsgPath, sLeaf);
									if(!xNyf.fileExists(xSsg.toString()) || xNyf.getFileSize(xSsg.toString())!=f.getFileSize()){
										sLeaf=getUniqueSsgFileName(xNyf, sSsgPath, sLeaf);
										if(sLeaf){
											xSsg=new CLocalFile(sSsgPath, sLeaf);
											nBytes=xNyf.createFile(xSsg, f);
										}
									}
									u=percentEncode(xSsg.getLeafName());
								}
							}
						}
					}
				}

				if(xActPost){
					u=xActPost(sObj, sTagName, u, nBytes);
				}
			}
			return u;
		});
	}
	return sHtml;
};
