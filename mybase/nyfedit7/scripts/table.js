
/////////////////////////////////////////////////////////////////////
// Essential scripts for myBase Desktop v7.x
// Copyright 2015 Wjj Software. All rights Reserved.
// Website: www.wjjsoft.com  Contact: info@wjjsoft.com
/////////////////////////////////////////////////////////////////////
// This code is property of Wjj Software (WJJSOFT). You may not use it
// for any commercial purpose without preceding consent from authors.
/////////////////////////////////////////////////////////////////////

function curTable()
{
	//2014.8.5 look at both the startContainer and endContainer;
	var xTable=null, xRng=getSelRange();
	if(xRng){
		var t=seekOuterElementByName(xRng.startContainer, 'table');
		if(t){
			xTable=t;
		}else{
			t=seekOuterElementByName(xRng.endContainer, 'table');
			if(t){
				xTable=t;
			}
		}
	}
	return xTable;
}

function focusOnTable()
{
	return curTable() ? true : false;
}

function firstCellSelected()
{
	var xTd;
	var xSel = document.getSelection();
	if(xSel){
		var xElm = xSel.getRangeAt(0).startContainer;
		xTd=seekOuterElementByName(xElm, 'td');
	}
	return xTd;
}

function lastCellSelected()
{
	var xTd;
	var xSel = document.getSelection();
	if(xSel){
		var xElm = xSel.getRangeAt(0).endContainer;
		xTd=seekOuterElementByName(xElm, 'td');
	}
	return xTd;
}

function posOfFirstCellSelected()
{
	var xPos = {iRow : -1, iCol : -1};
	var xTd=firstCellSelected();
	if(xTd){
		xPos.iRow = xTd.parentNode.rowIndex;
		xPos.iCol = xTd.cellIndex;
		//app.log('pos of first TD: row='+xPos.iRow+', col='+xPos.iCol);
	}
	return xPos;
}

function posOfLastCellSelected()
{
	var xPos = {iRow : -1, iCol : -1};
	var xTd=lastCellSelected();
	if(xTd){
		xPos.iRow = xTd.parentNode.rowIndex;
		xPos.iCol = xTd.cellIndex;
		//app.log('pos of last TD: row='+xPos.iRow+', col='+xPos.iCol);
	}
	return xPos;
}

function tableCssUtil(k, v)
{
	var sRes, xElmTbl = curTable();
	if(xElmTbl && k){
		if(v===undefined){
			return cssUtil(xElmTbl, k);
		}else{
			g_xUndoStack.beginMacro('css of table');
			cssUtil(xElmTbl, k, v);
			g_xUndoStack.endMacro();
			return true;
		}
	}
}

function columnCssUtil(k, v)
{
	var xElmTbl = curTable();
	if(xElmTbl && xElmTbl.rows && xElmTbl.rows.length && k){
		var nCols=0, nRows=xElmTbl.rows.length;
		if(nRows>0){
			nCols=xElmTbl.rows[0].cells.length;
		}
		if(nCols>0){
			var xTd1=firstCellSelected(), xTd2=lastCellSelected();
			var xTr=xTd1 ? xTd1.parentNode : null;
			var xTb=xTr ? xTr.parentNode : null;
			if(xTd1 && xTd2 && xTr && xTb){

				var xPos1 = posOfFirstCellSelected();
				var xPos2 = posOfLastCellSelected();

				var iRow1 = xPos1.iRow, iRow2 = xPos2.iRow;
				var iCol1 = xPos1.iCol, iCol2 = xPos2.iCol;

				var nSel=iRow2-iRow1+1; //2015.6.12 for any rows;
				if(nSel>0){

					//2015.6.11 enabled to handle multiple columns if selected;
					var _is_col_selected=function(c){
						if(iRow2-iRow1==0 && c>=iCol1 && c<=iCol2) return true;
						if(iRow2-iRow1==1 && (c>=iCol1 || c<=iCol2)) return true;
						if(iRow2-iRow1>1) return true; //two or more rows selected, that's to say, all columns selected;
						return false;
					};

					if(v!==undefined){

						g_xUndoStack.beginMacro('css of columns');

						//2015.6.18 forcedly set the attribute;
						cssUtil(xElmTbl, 'table-layout', 'fixed');
						cssUtil(xElmTbl, 'word-break', 'break-all');

						for(var iRow=0; iRow<nRows; ++iRow){
							for(var iCol=0; iCol<nCols; ++iCol){
								if(_is_col_selected(iCol)){
									var xTd = xElmTbl.rows[iRow].cells[iCol];
									if(xTd){
										cssUtil(xTd, k, v);
									}
								}
							}
						}

						g_xUndoStack.endMacro();
						return true;

					}else{

						for(var iRow=0; iRow<nRows; ++iRow){
							for(var iCol=0; iCol<nCols; ++iCol){
								if(_is_col_selected(iCol)){
									var xTd = xElmTbl.rows[iRow].cells[iCol];
									if(xTd){
										var sRes=cssUtil(xTd, k);
										if(sRes) return sRes; //2015.6.17 returns the first non-empty value;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

function cellCssUtil(k, v)
{
	var xElmTbl = curTable();
	if(xElmTbl && xElmTbl.rows && xElmTbl.rows.length && k){
		var nCols=0, nRows=xElmTbl.rows.length;
		if(nRows>0){
			nCols=xElmTbl.rows[0].cells.length;
		}
		if(nCols>0){
			var xTd1=firstCellSelected(), xTd2=lastCellSelected();
			var xTr=xTd1 ? xTd1.parentNode : null;
			var xTb=xTr ? xTr.parentNode : null;
			if(xTd1 && xTd2 && xTr && xTb){

				var xPos1 = posOfFirstCellSelected();
				var xPos2 = posOfLastCellSelected();

				var iRow1 = xPos1.iRow, iRow2 = xPos2.iRow;
				var iCol1 = xPos1.iCol, iCol2 = xPos2.iCol;

				var nSel=iRow2-iRow1+1; //2015.6.12 for any rows;
				if(nSel>0){

					var _is_cell_selected=function(r, c){
						if(r<iRow1) return false;
						if(r>iRow2) return false;
						if(r==iRow1 && c<iCol1) return false;
						if(r==iRow2 && c>iCol2) return false;
						return true;
					};

					if(v!==undefined){

						g_xUndoStack.beginMacro('css of columns');

						//2015.6.18 forcedly set the attribute;
						//cssUtil(xElmTbl, 'table-layout', 'fixed');
						//cssUtil(xElmTbl, 'word-break', 'break-all');

						for(var iRow=iRow1; iRow<nRows; ++iRow){
							for(var iCol=0; iCol<nCols; ++iCol){
								if(_is_cell_selected(iRow, iCol)){
									var xTd = xElmTbl.rows[iRow].cells[iCol];
									if(xTd){
										cssUtil(xTd, k, v);
									}
								}
							}
						}

						g_xUndoStack.endMacro();
						return true;

					}else{

						for(var iRow=0; iRow<nRows; ++iRow){
							for(var iCol=0; iCol<nCols; ++iCol){
								if(_is_cell_selected(iCol)){
									var xTd = xElmTbl.rows[iRow].cells[iCol];
									if(xTd){
										var sRes=cssUtil(xTd, k);
										if(sRes) return sRes; //2015.6.17 returns the first non-empty value;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

var sDefCellTxt = "<br />"; //<br /> gives normal height for newly inserted cells;

function insertRowBefore()
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var xTd=firstCellSelected();
		if(xTd && xTd.parentNode && xTd.parentNode.nodeName.toLowerCase()=='tr'){
			g_xUndoStack.beginMacro('Insert table row before');
			g_xUndoStack.pushMacro(new _CCmdInsertRow(xTd, false));
			g_xUndoStack.endMacro();
			bSucc = true;
		}
	}
	return bSucc;
}

function insertRowAfter()
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var xTd=lastCellSelected();
		if(xTd && xTd.parentNode && xTd.parentNode.nodeName.toLowerCase()=='tr'){
			g_xUndoStack.beginMacro('Insert table row after');
			g_xUndoStack.pushMacro(new _CCmdInsertRow(xTd, true));
			g_xUndoStack.endMacro();
			bSucc = true;
		}
	}
	return bSucc;
}

function insertColumnBefore()
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var xTd=firstCellSelected();
		if(xTd && xTd.parentNode && xTd.parentNode.nodeName.toLowerCase()=='tr'){
			g_xUndoStack.beginMacro('Insert table column before');
			g_xUndoStack.pushMacro(new _CCmdInsertColumn(xTd, false));
			g_xUndoStack.endMacro();
			bSucc = true;
		}
	}
	return bSucc;
}

function insertColumnAfter()
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var xTd=lastCellSelected();
		if(xTd && xTd.parentNode && xTd.parentNode.nodeName.toLowerCase()=='tr'){
			g_xUndoStack.beginMacro('Insert table column after');
			g_xUndoStack.pushMacro(new _CCmdInsertColumn(xTd, true));
			g_xUndoStack.endMacro();
			bSucc = true;
		}
	}
	return bSucc;
}

function deleteRow()
{
	var nDel=0, xElmTbl = curTable();
	if(xElmTbl){
		var nRows = xElmTbl.rows.length;
		if(nRows>0){

			var xTd=firstCellSelected();
			var xTr=xTd ? xTd.parentNode : null;
			if(xTd && xTr){
				var xPos1 = posOfFirstCellSelected();
				var xPos2 = posOfLastCellSelected();

				var iRow1 = xPos1.iRow, iRow2 = xPos2.iRow;
				if(iRow1>iRow2){
					var x=iRow1; iRow1=iRow2; iRow2=x; //swap;
				}

				var nToDel=iRow2-iRow1+1;
				if(nToDel>0){
					if(nToDel>=nRows){
						var p=xElmTbl.parentNode, iPos=posOfNode(xElmTbl);
						g_xUndoStack.beginMacro('Delete table');
						g_xUndoStack.pushMacro(new _CCmdRemoveElm(p, xElmTbl, iPos));
						g_xUndoStack.endMacro();
					}else{
						g_xUndoStack.beginMacro('Delete table rows');
						g_xUndoStack.pushMacro(new _CCmdDeleteRows(xTr.parentNode, iRow1, nToDel));
						g_xUndoStack.endMacro();
					}
				}
			}
		}
	}
	return nDel>0;
}

function deleteColumn()
{
	var nDel=0, xElmTbl = curTable();
	if(xElmTbl && xElmTbl.rows && xElmTbl.rows.length){
		var nCols=(xElmTbl.rows.length>0) ? xElmTbl.rows[0].cells.length : 0;
		if(nCols>0){

			var xTd1=firstCellSelected(), xTd2=lastCellSelected();
			var xTr=xTd1 ? xTd1.parentNode : null;
			var xTb=xTr ? xTr.parentNode : null;
			if(xTd1 && xTd2 && xTr && xTb){

				var xPos1 = posOfFirstCellSelected();
				var xPos2 = posOfLastCellSelected();

				var iRow1 = xPos1.iRow, iRow2 = xPos2.iRow;
				var iCol1 = xPos1.iCol, iCol2 = xPos2.iCol;

				if(iRow2-iRow1==0){

					var nToDel=iCol2-iCol1+1;
					g_xUndoStack.beginMacro('Delete table columns');
					g_xUndoStack.pushMacro(new _CCmdDeleteCols(xTr.parentNode, iCol1, nToDel));
					g_xUndoStack.endMacro();

				}else if(iRow2-iRow1==1){

					if(iCol1<=iCol2){

						deleteTable(); //columns overlapped;

					}else{

						g_xUndoStack.beginMacro('Delete table columns');
						g_xUndoStack.pushMacro(new _CCmdDeleteCols(xTr.parentNode, iCol1, nCols-iCol1));
						g_xUndoStack.pushMacro(new _CCmdDeleteCols(xTr.parentNode, 0, iCol2+1));
						g_xUndoStack.endMacro();

					}

				}else if(iRow2-iRow1>1){

					deleteTable(); //two or more rows selected, that's to say, all columns selected;

				}
			}
		}
	}
	return nDel>0;
}

function deleteTable()
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var p=xElmTbl.parentNode, iPos=posOfNode(xElmTbl);
		g_xUndoStack.beginMacro('Delete table');
		g_xUndoStack.pushMacro(new _CCmdRemoveElm(p, xElmTbl, iPos));
		g_xUndoStack.endMacro();
		bSucc=true;
	}
	return bSucc;
}

function widenTable(n) //to-remove
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var sWid=xElmTbl.getAttribute('width')||'100';
		if(sWid){
			var w=parseFloat(sWid);
			if(w>0 && w<10000){

				if(n>-1 && n<1){
					//n incidates a percent number;
					w+=w*n;
				}else{
					//n incidates a number in pixels;
					w+=n;
				}

				//xElmTbl.setAttribute('width', ''+Math.floor(w));

				g_xUndoStack.beginMacro('Set table width');
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElmTbl, 'width', ''+Math.floor(w)));
				g_xUndoStack.endMacro();

				bSucc=true;

			}
		}
	}
	return bSucc;
}

/*function setColWidth(w) //to-remove
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl && xElmTbl.rows && xElmTbl.rows.length){
		var nCols=0, nRows=xElmTbl.rows.length;
		if(nRows>0){
			nCols=xElmTbl.rows[0].cells.length;
		}
		if(nCols>0){
			var xTd1=firstCellSelected(), xTd2=lastCellSelected();
			var xTr=xTd1 ? xTd1.parentNode : null;
			var xTb=xTr ? xTr.parentNode : null;
			if(xTd1 && xTd2 && xTr && xTb){

				var xPos1 = posOfFirstCellSelected();
				var xPos2 = posOfLastCellSelected();

				var iRow1 = xPos1.iRow, iRow2 = xPos2.iRow;
				var iCol1 = xPos1.iCol, iCol2 = xPos2.iCol;

				var nSel=iRow2-iRow1+1; //2015.6.12 for any rows;
				if(nSel>0){

					var _is_col_selected=function(c){
						if(iRow2-iRow1==0 && c>=iCol1 && c<=iCol2) return true;
						if(iRow2-iRow1==1 && (c>=iCol1 || c<=iCol2)) return true;
						if(iRow2-iRow1>1) return true; //two or more rows selected, that's to say, all columns selected;
						return false;
					};

					//2015.6.11 need to calculate the table width according to existing <td>s,
					//so the table element can be enlarged or shrinked appropriately, 
					//especially when the table is previously initialized with a fixed width number;

					var nWidTbl=0;
					for(var iCol=0; iCol<nCols; ++iCol){
						var xTd=xElmTbl.rows[0].cells[iCol];
						//if(iCol>=iCol1 && iCol<=iCol2){
						if(_is_col_selected(iCol)){
							if(w>0) nWidTbl+=w;
						}else{
							if(xTd){
								nWidTbl+=xTd.offsetWidth;
							}
						}
					}

					g_xUndoStack.beginMacro('Set column width');

					cssUtil(xElmTbl, 'word-break', 'break-all');

					//2015.6.11 enabled to handle multiple columns if selected;
					for(var iRow=0; iRow<nRows; ++iRow){
						for(var iCol=0; iCol<nCols; ++iCol){
							//if(iCol>=iCol1 && iCol<=iCol2){
							if(_is_col_selected(iCol)){
								var xTd = xElmTbl.rows[iRow].cells[iCol];
								if(xTd){
									var sWidth = (w > 0 ? Math.floor(w)+'px' : '');
									cssUtil(xTd, 'width', sWidth);
								}
							}
						}
					}

					//2015.6.11 adjust the table width accordingly;
					//g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElmTbl, 'width', ''+nWidTbl));

					//2015.6.11 prefer using CSS than HTML attributes;
					g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElmTbl, 'width', ''));
					cssUtil(xElmTbl, 'width', ''+nWidTbl+'px');

					g_xUndoStack.endMacro();

					bSucc=true;
				}
			}
		}
	}
	return bSucc;
}*/

/*function setTableWidth(w) //to-remove
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){

		g_xUndoStack.beginMacro('Set table width');

		if(!w || w=='0' || w===0) w=''; else w+='px';

		//2015.6.11 adjust the table width accordingly;
		//g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElmTbl, 'width', ''+w));

		//2015.6.11 prefer using CSS than HTML attributes;
		g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElmTbl, 'width', ''));
		cssUtil(xElmTbl, 'width', ''+w);

		g_xUndoStack.endMacro();

		bSucc=true;
	}
	return bSucc;
}*/

/*function setRowHeight(h) //to-remove
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl){
		var xPos = posOfLastCellSelected();

		if(xPos.iRow < xElmTbl.rows.length){
			var xTd = xElmTbl.rows[xPos.iRow].cells[xPos.iCol];
			var xTr = xTd ? xTd.parentNode : null;
			if(xTr){
				g_xUndoStack.beginMacro('Set row height');

				var sHeight = (h > 0 ? Math.floor(h)+'px' : '');
				g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xTr, 'height', sHeight));
				//cssUtil(xElmTbl, 'word-break', h > 0 ? '' : 'break-all');

				g_xUndoStack.endMacro();
			}
		}
	}
	return bSucc;
}*/

/*function setTableBackColor(sColor, iRange) //to-remove
{
	var bSucc = false, xElmTbl = curTable();
	if(xElmTbl && xElmTbl.rows && xElmTbl.rows.length){

		if(iRange==0){ //for <table>

			g_xUndoStack.beginMacro('Set background color for <table>');

			g_xUndoStack.pushMacro(new _CCmdChgElmAttr(xElmTbl, 'bgcolor', ''));
			cssUtil(xElmTbl, 'background-color', sColor||'');

			g_xUndoStack.endMacro();

			bSucc=true;

		}else if(iRange==1){ //for selected <td> cells

			var nCols=0, nRows=xElmTbl.rows.length;
			if(nRows>0){
				nCols=xElmTbl.rows[0].cells.length;
			}
			if(nCols>0){

				var xTd1=firstCellSelected(), xTd2=lastCellSelected();
				var xTr=xTd1 ? xTd1.parentNode : null;
				var xTb=xTr ? xTr.parentNode : null;
				if(xTd1 && xTd2 && xTr && xTb){

					var xPos1 = posOfFirstCellSelected();
					var xPos2 = posOfLastCellSelected();

					var iRow1 = xPos1.iRow, iRow2 = xPos2.iRow;
					var iCol1 = xPos1.iCol, iCol2 = xPos2.iCol;

					var _is_cell_selected=function(r, c){
						if(r<iRow1) return false;
						if(r>iRow2) return false;
						if(r==iRow1 && c<iCol1) return false;
						if(r==iRow2 && c>iCol2) return false;
						return true;
					};

					var nSel=iRow2-iRow1+1; //2015.6.12 for any rows;
					if(nSel>0){

						g_xUndoStack.beginMacro('Set background color for <td>');

						for(var iRow=iRow1; iRow<nRows; ++iRow){
							for(var iCol=0; iCol<nCols; ++iCol){
								if(_is_cell_selected(iRow, iCol)){
									var xTd = xElmTbl.rows[iRow].cells[iCol];
									if(xTd){
										cssUtil(xTd, 'background-color', sColor||'');
									}
								}
							}
						}

						g_xUndoStack.endMacro();

						bSucc=true;

					}
				}
			}
		}

	}
	return bSucc;
}*/

function canMergeDown()
{
	var bCan = false;
	if(focusOnTable()){
		var xElmTbl = curTable();
		var xPos = posOfLastCellSelected();
		if(xPos.iRow >= 0 && xPos.iRow < xElmTbl.rows.length - 1 && xPos.iCol >= 0){
			var xCell = xElmTbl.rows[xPos.iRow].cells[xPos.iCol];
			var xSiblingCell = xElmTbl.rows[xPos.iRow + xCell.rowSpan].cells[xPos.iCol];
			if(xCell && xSiblingCell && xSiblingCell.style.display != 'none'){
				if(xCell.colSpan == xSiblingCell.colSpan){
					bCan = true;
				}
			}
		}
	}
	return bCan;
}

function mergeDown()
{
	var bSucc = false;
	if(focusOnTable() && canMergeDown()){
		var xElmTbl = curTable();
		var xPos = posOfLastCellSelected();
		if(xPos.iRow >= 0 && xPos.iRow < xElmTbl.rows.length && xPos.iCol >= 0){

			var xCell = xElmTbl.rows[xPos.iRow].cells[xPos.iCol];
			var xSiblingCell = xElmTbl.rows[xPos.iRow + xCell.rowSpan].cells[xPos.iCol];
			if(xCell && xSiblingCell){
				xCell.rowSpan += xSiblingCell.rowSpan;

				xSiblingCell.colSpan = 1;
				xSiblingCell.rowSpan = 1;
				xSiblingCell.style.display = 'none';
			}
		}
	}
	return bSucc;
}

function canMergeRight()
{
	var bCan = false;
	if(focusOnTable()){
		var xElmTbl = curTable();
		var xPos = posOfLastCellSelected();
		if(xPos.iCol >= 0 && xPos.iCol < xElmTbl.rows[xPos.iRow].cells.length - 1 && xPos.iRow >= 0){
			var xCell = xElmTbl.rows[xPos.iRow].cells[xPos.iCol];
			var xSiblingCell = xElmTbl.rows[xPos.iRow].cells[xPos.iCol + xCell.colSpan];
			if(xCell && xSiblingCell && xSiblingCell.style.display != 'none'){
				if(xCell.rowSpan == xSiblingCell.rowSpan){
					bCan = true;
				}
			}
		}
	}
	return bCan;
}

function mergeRight()
{
	var bSucc = false;
	if(focusOnTable() && canMergeRight()){
		var xElmTbl = curTable();
		var xPos = posOfLastCellSelected();
		if(xPos.iCol >= 0 && xPos.iCol < xElmTbl.rows[xPos.iRow].cells.length && xPos.iRow >= 0){

			var xCell = xElmTbl.rows[xPos.iRow].cells[xPos.iCol];
			var xSiblingCell = xElmTbl.rows[xPos.iRow].cells[xPos.iCol + xCell.colSpan];
			if(xCell && xSiblingCell){

				xCell.colSpan += xSiblingCell.colSpan;

				xSiblingCell.colSpan = 1;
				xSiblingCell.rowSpan = 1;
				xSiblingCell.style.display = 'none';
			}
		}
	}
	return bSucc;
}

function getCurTableCellsText()
{
	var vCellsText = [];
	if(focusOnTable()){
		var xElmTbl = curTable();
		var nRowCount = xElmTbl.rows.length;
		for(var row = 0; row < nRowCount; row++){
			var vRowCells = [];
			var nColCount = xElmTbl.rows[row].cells.length;
			for(var col = 0; col < nColCount; col++){
				vRowCells.push(xElmTbl.rows[row].cells[col].innerHTML);
			}
			vCellsText.push(vRowCells);
		}
	}
	return vCellsText;
}
