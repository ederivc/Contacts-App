/*function getNumber(number) {
    for(let i = 1; i<number; i++){
        document.write(i)
        break
    }
}*/

function getNumber(z){
    let x = 0
    x = x+2
    document.write(x)
}

function getNumber(number)
    var table = document.getElementById("mytab1");
for (var i = 0, row; row = table.rows[i]; i++) {
   //iterate through rows
   //rows would be accessed using the "row" variable assigned in the for loop
   for (var j = 0, col; col = row.cells[j]; j++) {
     //iterate through columns
     //columns would be accessed using the "col" variable assigned in the for loop
   }  
}