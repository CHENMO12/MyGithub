
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

var ajax={

	onstart: null,
	onsuccess: null,
	onerror: null,

	sReferer: '',

	run: function(bAsync, sType, sUri, sCgiParams, xUserData, onSucc, onFail, bSilent)
	{
		var xReq=new XMLHttpRequest();

		if(ajax.onstart) ajax.onstart(xReq, sUri);

		var _onStateChange=function(){

			if(xReq.readyState == 4){

				var scode=xReq.status;
				if(scode==200){

					var sTxt=xReq.responseText;
					if(onSucc) onSucc(sTxt, xUserData);

					if(ajax.onsuccess) ajax.onsuccess(xReq, sUri);

				}else{

					if(ajax.onerror) ajax.onerror(xReq, sUri);
					
					var sMsg='';
					
					if(scode>=400 && scode<500) sMsg='Request URI specific error';
					if(scode>=500 && scode<600) sMsg='HTTP server specific error';

					if(sMsg){
						sMsg='Failed to complete the Ajax request.\n\n[ ErrCode: '+scode+' '+sMsg+' ]';
					}else{
						sMsg='Failed to talk to the website.\n\n[ ErrCode: '+scode+' '+xReq.statusText+' ]'+'\n\n'+sUri;
					}

					if(onFail){
						onFail(xReq, sMsg, xUserData);
					}else{
						if(!bSilent) alert(sMsg, 'Ajax Request Failure.');
					}
				}
			}

		};

		xReq.open(sType, sUri, bAsync);

		xReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		xReq.setRequestHeader('referer', this.sReferer||'');

		//xReq.setRequestHeader('Cache-Control', 'no-cache');
		//xReq.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

		xReq.setRequestHeader('Accept-Charset', 'x-user-defined');
		xReq.overrideMimeType('text/plain; charset=x-user-defined');

		xReq.onreadystatechange=_onStateChange;

		try{

			xReq.send(sCgiParams||'');

		}catch(e){
			if(!bSilent) alert('Failure requesting: '+sUri);
		}
	}

};
