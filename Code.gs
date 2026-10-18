function isOverlap(in1,in2,classname){
  if(in1 == "" || in2 == "") return false
  return Checkoverlap(in1,classname) || Checkoverlap(in2,classname)
}

function debug(){
  Checkoverlap(3010)
}


function Checkoverlap(input,classnum) {
  if(classnum == "") return false
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var r = ss.getRange("C2:D500")
  var classes =ss.getRange("A2:A500")
  const numRows = r.getNumRows();
  const numCols = r.getNumColumns();
  for (let i = 1; i <= numRows; i++) {
    const val1 = r.getCell(i, 1).getValue()
    const val2 = r.getCell(i, 2).getValue()
    if(val1 == "#VALUE!" ) continue
    const c = classes.getCell(i,1).getValue()
    if(c == classnum && ((input == val1) || (input == val2))){
      // if the sane - ignore
      continue
    }
    if(9999 - Math.max(val1,val2) <= 100 && Math.min(val1,val2) < 100){
      // crossing the boundry
      if( (input >= Math.max(val1,val2) && input <= 9999 ) || 
          ( input <= Math.min(val1,val2) )
      ) {
        return true
        } 
      } else {        
          // normal case
        if(input >= Math.min(val1,val2) && input <= Math.max(val1,val2)){
          return true
        }
      }  
  }
  return false
}

function setTimeStamp(e){
    const currentDate = new Date();
    e.source.getActiveSheet().getRange(e.range.getRow(),11).setValue(currentDate);
}


function onEdit(e){
  
  const row = e.range.getRow();
  const col = e.range.getColumn();
  console.log(row)
  console.log(col)
  if (col == 2 && row > 1 ){
    setTimeStamp(e)
  }
}
