
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

var htmlEncode=function(s){
	//http://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
	//http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=dec
	s=s.replace(/&/g,	'&amp;');
	s=s.replace(/</g,	'&lt;');
	s=s.replace(/>/g,	'&gt;');
	s=s.replace(/\"/g,	'&quot;');
	s=s.replace(/\'/g,	'&apos;');
	s=s.replace(/\xA0/g,	'&nbsp;'); //http://www.fileformat.info/info/unicode/char/a0/index.htm
	//s=s.replace(/\t/g,	'&nbsp; &nbsp; &nbsp; &nbsp; '); //&emsp;
	s=s.replace(/  /g,	'&nbsp; '); //&nbsp; = non-breaking space;
	//more ...
	return s;
};

var htmlDecode=function(s){
	s=s.replace(/&lt;/g,		'<');
	s=s.replace(/&gt;/g,		'>');
	s=s.replace(/&quot;/g,		'"');
	s=s.replace(/&apos;/g,		'\'');
	s=s.replace(/&emsp;/g,		'    '); //2015.10.23 bugfix: just 4 spaces, not the '&nbsp; &nbsp; &nbsp; &nbsp; '
	s=s.replace(/&nbsp;/g,		' ');
	s=s.replace(/&circ;/g,		'^');
	s=s.replace(/&tilde;/g,		'~');
	//more ...
	s=s.replace(/&amp;/g,		'&');
	return s;
};

function _percentEncoding(sData)
{
	var r='';
	for(var i=0; i<sData.length; ++i){
		var n=sData.charCodeAt(i)&0xff;
		var sHex=new Number(n).toString(16);
		if(sHex.length==1) sHex='0'+sHex;
		r+=sHex;
	}
	return r;
};

var _trim=function(s){return (s||'').replace(/^\s+|\s+$/g, '');};
var _trim_cr=function(s){return (s||'').replace(/\r+$/g, '');};

function _reveal_obj(obj)
{
	var s='NULL';
	if(obj){
		
		var type=typeof(obj);
		s='TYPE = '+type+'\n';

		if(type == 'object'){
			for(var x in obj){

				if(x=='typeDetail') continue; //weird thing in IE7
			
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

function suffixNameOf(sUri)
{
	//2015.4.6 extract suffix name from a URL, like: http://www.abc.com/dir/file.png?parameters#hash
	sUri=sUri||'';

	var p=sUri.lastIndexOf('#');
	if(p>=0){
		sUri=sUri.substr(0, p);
	}

	p=sUri.lastIndexOf('?');
	if(p>=0){
		sUri=sUri.substr(0, p);
	}

	p=sUri.lastIndexOf('.'), sExt='';
	if(p>=0){
		sExt=sUri.substr(p+1);
		if(sExt.length>4) sExt='';
	}

	return sExt;
}
