
//sValidation=nyfjs
//sCaption=Resize image ...
//sHint=Resize the image in context
//sCategory=Context.ImgUtils
//sPosition=
//sCondition=CURDB; DBRW; CURINFOITEM; FORMATTED; EDITING; IMAGE;
//sID=p.Image.Resize
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

try{
	var xNyf=new CNyfDb(-1);

	if(xNyf.isOpen()){

		if(!xNyf.isReadonly()){

			if(plugin.isContentEditable()){

				var sEditor=plugin.getCurEditorType().toLowerCase();
				if(sEditor=='htmledit'){

					//var sCode='dimOfImage(null, true);';
					//var s=plugin.runDomScript(-1, sCode);

					var s=plugin.getImageDimension(-1);
					var v=(s||'').split('x');

					if(v && v.length==2){

						var w0=parseInt(v[0]), h0=parseInt(v[1]);

						var vOpts=[], vWidth=[], vHeight=[];
						for(var i=0; i<40; ++i){
							var d=5*(i+1);
							var w=Math.floor(w0*d/100), h=Math.floor(h0*d/100);
							vWidth.push(w);
							vHeight.push(h);
							var sTmp='' + d + '%  ( ' + w + ' x ' + h + ' )'; if(d==100) sTmp+=' ('+_lc2('Natural', 'Natural')+')';
							vOpts.push(sTmp);
						}

						for(var i=0; i<40; ++i){
							var w=20*(i+1);
							var d=Math.floor(w*100.0/w0), h=Math.floor(h0*d/100);
							vWidth.push(w);
							vHeight.push(h);
							var sTmp='' + w + ' x ' + h + ' ( ' + d + '% )';
							vOpts.push(sTmp);
						}

						for(var i=0; i<16; ++i){
							var w=16*(i+1), h=16*(i+1);
							vWidth.push(w);
							vHeight.push(h);
							vOpts.push( '( ' + w + ' x ' + h + ' )' );
						}

						for(var i=0; i<30; ++i){
							var w=20*(i+1), h=20*(i+1);
							vWidth.push(w);
							vHeight.push(h);
							vOpts.push( '( ' + w + ' x ' + h + ' )' );
						}

						var sCfgKey1='ResizeImage.Html.iSize';
						var vFields = [
							{sField: "combolist", sLabel: _lc2('Dimension', 'Dimension'), vItems: vOpts, sInit: localStorage.getItem(sCfgKey1)||''}
						];

						var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 400, vMargins: [8, 0, 30, 0]});
						if(vRes && vRes.length>0){

							var iSel=vRes[0];

							localStorage.setItem(sCfgKey1, iSel);

							var w=parseInt(vWidth[iSel]), h=parseInt(vHeight[iSel]);
							//{
							//	sCode='ResizeImage(null, %WIDTH%, %HEIGHT%)'.replace(/%WIDTH%/, w).replace(/%HEIGHT%/, h);
							//	plugin.runDomScript(-1, sCode);
							//}

							plugin.setImageDimension(-1, w, h);
						}
					}

				}else if(sEditor=='richedit'){

					var s=plugin.getImageDimension(-1);
					var v=(s||'').split('x');

					if(v && v.length==2){

						var w0=parseInt(v[0]), h0=parseInt(v[1]);

						//var sCfgKey1='ResizeImage.Rich.nWidth', sCfgKey2='ResizeImage.Rich.nHeight';
						var vFields = [
							{sField: "lineedit", sLabel: _lc2('Width', 'Width'), sInit: w0||'', bReq: false}
							, {sField: "lineedit", sLabel: _lc2('Height', 'Height'), sInit: h0||'', bReq: false}
						];

						var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 400, vMargins: [8, 0, 30, 0]});
						if(vRes && vRes.length>=2){

							var w=parseInt(vRes[0]), h=parseInt(vRes[1]);

							//localStorage.setItem(sCfgKey1, w);
							//localStorage.setItem(sCfgKey2, h);

							plugin.setImageDimension(-1, w, h);
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
