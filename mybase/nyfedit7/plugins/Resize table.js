
//sValidation=nyfjs
//sCaption=Resize table ...
//sHint=Resize the current table
//sCategory=MainMenu.Table;
//sPosition=TBL-03-ATTR-01
//sCondition=CURDB; DBRW; CURINFOITEM; HTMLEDIT; TABLE
//sID=p.Table.Resize
//sAppVerMin=7.0
//sShortcutKey=
//sAuthor=wjjsoft

/////////////////////////////////////////////////////////////////////
// Extension scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
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

				//var sCfgKey1='TableSize.nWidth';

				var vVals=[
					'|'+_lc('p.Common.Initial', 'Initial')
					, '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%'
					, '100%|'+'100% (Full)'
					, '10pt', '20pt', '30pt', '40pt', '50pt', '60pt', '70pt', '80pt', '90pt'
					, '100pt', '150pt', '200pt', '250pt', '300pt', '350pt', '400pt', '450pt'
					, '500pt', '550pt', '600pt', '650pt', '700pt', '750pt', '800pt', '850pt'
					, '900pt', '950pt', '1000pt'
					, '10px', '20px', '30px', '40px', '50px', '60px', '70px', '80px', '90px'
					, '100px', '150px', '200px', '250px', '300px', '350px', '400px', '450px'
					, '500px', '550px', '600px', '650px', '700px', '750px', '800px', '850px'
					, '900px', '950px', '1000px'
				];

				var sCode='tableCssUtil("width");';
				var sOld=plugin.runDomScript(-1, sCode); if(sOld=='undefined') sOld='';

				var vFields = [
					{sField: "comboedit", sLabel: _lc2('Descr', 'Width of table'), vItems: vVals, sInit: sOld||''}
				];

				var vRes = input(plugin.getScriptTitle(), vFields, {nMinSize: 400, vMargins: [8, 0, 30, 0]});
				if(vRes && vRes.length>0){

					var sVal=vRes[0];

					//localStorage.setItem(sCfgKey1, sVal);

					sCode='tableCssUtil("width", "%WIDTH%");'.replace(/%WIDTH%/, sVal);
					if(plugin.runDomScript(-1, sCode)){
						//done;
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