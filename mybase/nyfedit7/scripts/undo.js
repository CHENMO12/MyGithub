
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function _CUndoStack()
{
	this.vUndoStack=[];
	this.iRedo=-1;
	this.xUndoMacroTrack={}; //{txt: txt, items: []}
}

_CUndoStack.prototype={

	redo: function()
	{
		var j=this.iRedo;
		if(j>=0 && j<this.vUndoStack.length){
			var um=this.vUndoStack[j];
			if(um && um.items && um.items.length>0){
				for(var i in um.items){
					var d=um.items[i];
					if(d && d.redo){
						d.redo();
					}
				}
			}
		}
		this.iRedo++;
	},

	undo: function()
	{
		var j=this.iRedo;
		if(j>0 && j<=this.vUndoStack.length){
			var um=this.vUndoStack[j-1];
			if(um && um.items && um.items.length>0){
				var i=um.items.length;
				while( i-- > 0 ){ //UNDO in reverse order;
					var d=um.items[i];
					if(d && d.undo){
						d.undo();
					}
				}
			}
		}
		this.iRedo--;
	},

	pushToUndoStack: function(um){
		if(um && um.txt && um.items && um.items.length>0){
			var i=this.iRedo;
			if(i<=0){
				this.vUndoStack=[];
			}else if(i<this.vUndoStack.length){
				this.vUndoStack.splice(i, this.vUndoStack.length-i);
			}

			this.vUndoStack.push(um);
			this.iRedo=this.vUndoStack.length-1; //always points to the current REDO entry;

			app.pushToDomUndoStack(um.txt);
		}
	},

	beginMacro: function(txt)
	{
		this.xUndoMacroTrack={txt: txt};
	},

	endMacro: function()
	{
		var um=this.xUndoMacroTrack;

		if(um && um.txt && um.items && um.items.length>0){
			this.pushToUndoStack(um);
		}
		this.xUndoMacroTrack=undefined;
	},

	pushMacro: function(d)
	{
		var um=this.xUndoMacroTrack;
		if(um && um.txt && d){
			if(!um.items) um.items=[];
			um.items.push(d);
		}
	}

};

///////////////////////////////////////////////////////////

if(window.g_xUndoStack===undefined) window.g_xUndoStack=new _CUndoStack();

if(window.redo===undefined) window.redo=function(){window.g_xUndoStack.redo();};
if(window.undo===undefined) window.undo=function(){window.g_xUndoStack.undo();};

///////////////////////////////////////////////////////////

function _CCmdChgElmAttr(xElm, sAttrName, sAttrVal)
{
	this.elm=xElm;
	this.name=sAttrName;
	this.value=sAttrVal;
}

_CCmdChgElmAttr.prototype={

	redo: function(){this.swap();},
	undo: function(){this.swap();},

	swap: function(){
		var e=this.elm, n=this.name, v=this.value;
		if(e){
			var sBak=e.getAttribute(n);
			if(sBak!=v){
				if(v){
					e.setAttribute(n, v);
				}else{
					e.removeAttribute(n);
				}
				this.value=sBak;
				app.setDomDirty(true);
			}
		}
	},

};

///////////////////////////////////////////////////////////

function _CCmdChgElmInnerHtml(xElm, sInnerHtml)
{
	this.elm=xElm;
	this.innerHtml=sInnerHtml;
}

_CCmdChgElmInnerHtml.prototype={

	redo: function(){this.swap();},
	undo: function(){this.swap();},

	swap: function(){
		var e=this.elm, v=this.innerHtml;
		if(e){
			var sBak=e.innerHTML;
			if(sBak!=v){
				if(v){
					e.innerHTML = v;
				}
				this.innerHtml=sBak;
				app.setDomDirty(true);
			}
		}
	},

};

///////////////////////////////////////////////////////////

function _CCmdRemoveElm(xParent, xSub, iPos)
{
	this.parent=xParent;
	this.sub=xSub;
	this.pos=iPos;
}

_CCmdRemoveElm.prototype={

	redo: function(){
		var p=this.parent, s=this.sub;
		p.removeChild(s);
		app.setDomDirty(true);
	},

	undo: function(){
		var p=this.parent, s=this.sub, i=this.pos;
		if(i>=0 && i<p.childNodes.length){
			p.insertBefore(s, p.childNodes[i]);
		}else{
			p.appendChild(s);
		}
		app.setDomDirty(true);
	}

};

///////////////////////////////////////////////////////////

function _CCmdInsertElm(xParent, xSub, iPos)
{
	this.parent=xParent;
	this.sub=xSub;
	this.pos=iPos;
}

_CCmdInsertElm.prototype={

	redo: function(){
		var p=this.parent, s=this.sub, i=this.pos;
		if(i>=0 && i<p.childNodes.length){
			p.insertBefore(s, p.childNodes[i]);
		}else{
			p.appendChild(s);
		}
		app.setDomDirty(true);
	},

	undo: function(){
		var p=this.parent, s=this.sub;
		p.removeChild(s);
		app.setDomDirty(true);
	}

};

///////////////////////////////////////////////////////////

function _CCmdReplaceElmTags(vItems)
{
	this.items=vItems; //[{path: '', tagNew: '', elmNew: null}];

	for(var i in this.items){
		var d=this.items[i];
		var elmOld=nodeByPath(d.path);
		if(elmOld && d.tagNew){
			d.elmNew=document.createElement(d.tagNew);
		}
	}
}

_CCmdReplaceElmTags.prototype={

	redo: function(){
		var bDirty=false;
		for(var j in this.items){
			var d=this.items[j];
			var elmOld=nodeByPath(d.path);
			var p=elmOld ? elmOld.parentNode : null;
			if(p && elmOld && d.elmNew){
				//2014.12.28 For first Redo, need to clone and cache all child nodes;
				//considering the multiple replacements in one go, Cloning the branch can only be done right here before next replacement;
				if(elmOld.childNodes.length>0 && d.elmNew.childNodes.length<=0){
					for(var i=0; i<elmOld.childNodes.length; i++){
						d.elmNew.appendChild(elmOld.childNodes[i].cloneNode(true));
					}
				}

				p.replaceChild(d.elmNew, elmOld);
				d.elmNew=elmOld;

				bDirty=true;
			}
		}
		if(bDirty) app.setDomDirty(true);
	},

	undo: function(){
		var bDirty=false;
		//2014.12.29 Note that: the reverse order may not work with any HTML tag structures;
		var j=this.items.length;
		while( j-- > 0 ){ //UNDO in reverse order;
		//for(var j in this.items){
			var d=this.items[j];
			var elmOld=nodeByPath(d.path);
			var p=elmOld ? elmOld.parentNode : null;
			if(p && elmOld && d.elmNew){
				p.replaceChild(d.elmNew, elmOld);
				d.elmNew=elmOld;
				bDirty=true;
			}
		}
		if(bDirty) app.setDomDirty(true);
	}

};

///////////////////////////////////////////////////////////

function _CCmdInsertRow(xTd, bAfter)
{
	this.td=xTd;
	this.after=bAfter;
	this.xTrNew=document.createElement('tr');

	var td=this.td;
	var tr=td ? td.parentNode : null;
	var tb=tr ? tr.parentNode : null;
	if(td && tr && tb){
		for(var i=0; i<tr.childNodes.length; ++i){
			//2014.12.31 there may be some #text nodes (e.g. \r,\n,\t, and blankspaces, etc.) in the <tr> elements;
			if(tr.childNodes[i].nodeName.toLowerCase()=='td'){
				var xTdNew=document.createElement('td'); xTdNew.innerHTML='<br />';
				this.xTrNew.appendChild(xTdNew);
			}
		}
	}
}

_CCmdInsertRow.prototype={

	redo: function(){
		var td=this.td;
		var tr=td ? td.parentNode : null;
		var tb=tr ? tr.parentNode : null;
		if(td && tr && tb){
			var trRef=tr;
			if(this.after){
				do{
					trRef=trRef.nextSibling;
				}while(trRef && trRef.nodeName.toLowerCase()!='tr');
			}
			if(trRef){
				tb.insertBefore(this.xTrNew, trRef);
			}else{
				tb.appendChild(this.xTrNew);
			}
			app.setDomDirty(true);
		}
	},

	undo: function(){
		var td=this.td;
		var tr=td ? td.parentNode : null;
		var tb=tr ? tr.parentNode : null;
		if(td && tr && tb){
			tb.removeChild(this.xTrNew);
			app.setDomDirty(true);
		}
	}

};

///////////////////////////////////////////////////////////

function _CCmdInsertColumn(xTd, bAfter)
{
	this.td=xTd;
	this.pos=xTd ? xTd.cellIndex : -1;
	this.after=bAfter;
	this.vTdNew=[];

	var td=this.td;
	var tr=td ? td.parentNode : null;
	var tb=tr ? tr.parentNode : null;
	if(td && tr && tb){
		var vTr=childNodesOf(tb, 'tr');
		for(var i=0; i<vTr.length; ++i){
			var xTdNew=document.createElement('td'); xTdNew.innerHTML='<br />';
			this.vTdNew.push(xTdNew);
		}
	}
}

_CCmdInsertColumn.prototype={

	cellAt: function(xTr, iPos){
		var xTdRes;
		if(xTr && iPos>=0){
			var vTd=childNodesOf(xTr, 'td');
			if(vTd && iPos<vTd.length){
				xTdRes=vTd[iPos];
			}
		}
		return xTdRes;
	},

	redo: function(){
		var td=this.td, after=this.after;
		var tr=td ? td.parentNode : null;
		var tb=tr ? tr.parentNode : null;
		var p=this.pos;
		if(td && tr && tb && p>=0){
			var vTr=childNodesOf(tb, 'tr');
			for(var j=0; j<vTr.length; ++j){
				var xTr=vTr[j];
				var xTd=this.vTdNew[j];
				var xTdRef=this.cellAt(xTr, this.after ? (p+1) : p);
				if(xTdRef){
					xTr.insertBefore(xTd, xTdRef);
				}else{
					xTr.appendChild(xTd);
				}
				app.setDomDirty(true);
			}
		}
	},

	undo: function(){
		var td=this.td, after=this.after;
		var tr=td ? td.parentNode : null;
		var tb=tr ? tr.parentNode : null;
		var p=this.pos;
		if(td && tr && tb && p>=0){
			var vTr=childNodesOf(tb, 'tr');
			for(var j=0; j<vTr.length; ++j){
				var xTr=vTr[j];
				var xTd=this.cellAt(xTr, this.after ? (p+1) : p);
				if(xTd){
					xTr.removeChild(xTd);
				}else{
					//malformed table;
				}
				app.setDomDirty(true);
			}
		}
	}

};

///////////////////////////////////////////////////////////

function _CCmdDeleteRows(xTb, iPos, nToDel)
{
	this.tb=xTb;
	this.pos=iPos;
	this.num=nToDel;
	this.vTrTaken=[];

	var tb=this.tb;
	if(tb && iPos>=0 && nToDel>0){
		var vTr=childNodesOf(tb, 'tr');
		for(var i=iPos; i<vTr.length; ++i){
			this.vTrTaken.push(vTr[i]);
			if(this.vTrTaken.length>=nToDel) break;
		}
	}
}

_CCmdDeleteRows.prototype={

	rowAt: function(xTb, iPos){
		var xTrRes;
		if(xTb && iPos>=0){
			var vTr=childNodesOf(xTb, 'tr');
			if(vTr && iPos<vTr.length){
				xTrRes=vTr[iPos];
			}
		}
		return xTrRes;
	},

	redo: function(){
		var tb=this.tb;
		if(tb){
			for(var j=0; j<this.vTrTaken.length; ++j){
				var xTr=this.vTrTaken[j];
				if(xTr){
					tb.removeChild(xTr);
					app.setDomDirty(true);
				}
			}
		}
	},

	undo: function(){
		var tb=this.tb;
		if(tb){
			var trRef, vTr=childNodesOf(tb, 'tr');
			if(vTr.length>0){
				if(this.pos<vTr.length){
					trRef=vTr[this.pos];
				}
			}

			if(trRef){
				for(var i=this.vTrTaken.length-1; i>=0; --i){
					var xTr=this.vTrTaken[i];
					if(xTr){
						tb.insertBefore(xTr, trRef);
						app.setDomDirty(true);
						trRef=xTr;
					}
				}
			}else{
				for(var i=0; i<this.vTrTaken.length; ++i){
					tb.appendChild(this.vTrTaken[i]);
					app.setDomDirty(true);
				}
			}
		}
	}

};

///////////////////////////////////////////////////////////

function _CCmdDeleteCols(xTb, iPos, nToDel)
{
	this.tb=xTb;
	this.pos=iPos;
	this.num=nToDel;
	this.vvTdTaken=[];

	var tb=this.tb;
	if(tb && iPos>=0 && nToDel>0){
		var vTr=childNodesOf(tb, 'tr');
		for(var j=0; j<vTr.length; ++j){
			var vTd=childNodesOf(vTr[j], 'td'), vTaken=[];
			for(var i=iPos; i<vTd.length; ++i){
				vTaken.push(vTd[i]);
				if(vTaken.length>=nToDel) break;
			}
			this.vvTdTaken.push(vTaken);
		}
	}
}

_CCmdDeleteCols.prototype={

	cellAt: function(xTr, iPos){
		var xTdRes;
		if(xTr && iPos>=0){
			var vTd=childNodesOf(xTr, 'td');
			if(vTd && iPos<vTd.length){
				xTdRes=vTd[iPos];
			}
		}
		return xTdRes;
	},

	redo: function(){
		var tb=this.tb;
		if(tb){
			for(var j=0; j<this.vvTdTaken.length; ++j){
				var vTaken=this.vvTdTaken[j];
				for(var i=0; i<vTaken.length; ++i){
					var xTd=vTaken[i];
					if(xTd){
						xTd.parentNode.removeChild(xTd);
						app.setDomDirty(true);
					}
				}
			}
		}
	},

	undo: function(){
		var tb=this.tb;
		if(tb){
			var vTr=childNodesOf(tb, 'tr');
			for(var j=0; j<this.vvTdTaken.length; ++j){
				var xTr=vTr[j];
				var xTdRef=this.cellAt(xTr, this.pos);
				var vTaken=this.vvTdTaken[j];
				for(var i=vTaken.length-1; i>=0; --i){
					var xTd=vTaken[i];
					if(xTdRef){
						xTr.insertBefore(xTd, xTdRef);
					}else{
						xTr.appendChild(xTd);
					}
					app.setDomDirty(true);
					xTdRef=xTd;
				}
			}
		}
	}

};
