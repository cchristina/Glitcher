"use strict";


let matrixSize = 128;

let cellSize = 8; 

let cellMatrix = [];
let neighborDict = {};


let repDict = { 0:'_', 1:'█'}





function populateBoard(){  


    let matrix = [] 


    for (let i = 0; i < matrixSize ; i++) {
        let cellRow = [];

        for (let j = 0; j < matrixSize ; j++){
            let cellVal=0;
            // let cellVal = j%2;
            
            if (Math.floor(Math.random() * 11) > 6){
                cellVal = 1 ;
                // let cellVal = (j-1)%2;

            }
            
            cellRow.push(cellVal);
        }    
        matrix.push(cellRow);
    }   

    return matrix;

}


function populateOneD(){

    let tempCells = []

    for (let i = 0; i < matrixSize; i++){

        tempCells.push(Math.floor(Math.random() * 2));


    }


    return tempCells;
}



function oneDRuleMaker(left, center, right, output){

    // list_output = [int(i) for i in str(output)]

        let listOutput = []
        let sOut = output.toString();

        for (let i = 0; i < sOut.length; i++){

            listOutput.push(sOut[i]);
        }


    if (left && center && right){ //000
        return listOutput[0]

    }else if (left && center && !right ){ //001
        return listOutput[1]

    }else if (left && !center && right) { //010
      return listOutput[2]

    }else if (left && !center && !right ){ //011
        return listOutput[3]
 
    }else if (!left &&center && right){ //100
        return listOutput[4]
    
    }else if (!left && center && !right){ //101
        return listOutput[5]

    } else if (!left && !center && right){ //110
        return listOutput[6]

    }else if (!left && !center && !right){
        return listOutput[7]
    }

}





function oneDNextRow(row, rules){

    let newRow = []

    for (let i=0; i<row.length; i++){
        if (i==0 || i==row.length-1){
            newRow.push(row[i]);
        }
        else{

            newRow.push(oneDNextRow(row[i-1], row[i]), row[i+1], rules);

        }
    }

    return newRow;
}



function addRows(matrix, row, rules){

    rules = rules.toString(2);
    
    matrix.push(row);
    for (let i = 1; i < matrixSize; i++){
        matrix.push(oneDNextRow(matrix[i-1], rules));
    }


}




 



    


function flipCell(x, y){



    // console.log("PRE: " + cellMatrix[x][y])

    if (cellMatrix[x][y]==0){
    
        cellMatrix[x][y]=1;
    }    
    else{

        cellMatrix[x][y]=0;
    }


    // console.log("POST: " + cellMatrix[x][y])


    
}


function getCell(x,y){

    return cellMatrix[x][y];
}



function generateNeighborDictionary(neighborhood){


    let neibDict = {}
    let size = matrixSize

    for (let i= 0; i < matrixSize; i++) {
        for (let j = 0; j < matrixSize; j++){

            let neighborList = []
 
            for (let w=i-1; w < i+2 ; w++){
                for (let q=j-1; q < j+2; q++){

                    if (w!=i || q!=j ){

                        try{

                            if (neighborhood[w][q] != undefined){

                                neighborList.push(neighborhood[w][q]);
                                   
                            }
                        }catch(err){

                            neighborList.push(Math.random() * 2);

                        }
                        
                    }
                }

            }


            let neighborKey = [i,j];  

            neibDict[neighborKey] = neighborList;

        // console.log(neibDict[neighborKey], neighborList)
    }



}

// console.log(neibDict)
return neibDict;

}





function gameOfLifeRound(neighborhood) {

    let newNeighborhood = []

    neighborDict = generateNeighborDictionary(neighborhood);
    // console.log(neighborDict)

    for (let i = 0; i < matrixSize ; i++) {

        let newRow = [];

    for (let j = 0; j < matrixSize; j++) {

        // let neighborCount = neighborDict[[i,j]].reduce((acc, val) => 
        // {
        //     return acc + val;
        // });

        let neighborCount = 0;
        let countKey = [i,j]

        for (let i =0; i<neighborDict[countKey].length; i++) {

            neighborCount+=neighborDict[countKey][i];
        }

        let cell = neighborhood[i][j];

        if (cell ==1 ) {

            if (neighborCount==2 || neighborCount == 3) {
                newRow.push(1); 

            }
            else {
                newRow.push(0);           
            }
        }
        else if(cell==0 && neighborCount==3) {
            newRow.push(1);
        }
        else{
            newRow.push(0);
        }
    }  

    newNeighborhood.push(newRow);

    }

    return newNeighborhood;    
}


function printRep(matrix){
    for (let i = 0; i < matrix.length; i++){
        for (let j=0; j< matrix.length; j++){

          process.stdout.write(repDict[cellMatrix[i][j]]);
        }

        process.stdout.write('\n');
        
    }
    console.log('\n\n');
}







    




function displayRects(img){



    // cellMatrix = gameOfLifeRound(cellMatrix);

    for (let j = 0; j < cellMatrix.length-9; j++){

        ctx.beginPath();
        ctx.strokeStyle="#cccccc";
        ctx.moveTo(j,0);
        ctx.lineTo(j, cellMatrix.length);
        ctx.stroke();

        for (let k = 0; k<cellMatrix.length-9; k++){

            if (cellMatrix[j+1][k+1]==1){

                ctx.beginPath();
                ctx.lineWidth=".3";
                ctx.strokeStyle="#cccccc";
                ctx.fillStyle = "#4010aa";
                // ctx.globalAlpha = 0.9;
                ctx.drawImage(img, j*cellSize, k*cellSize, cellSize, cellSize, j*cellSize-cellSize,k*cellSize, cellSize, cellSize);
                ctx.restore();

                // ctx.rect(j*cellSize,k*cellSize, cellSize, cellSize);
                ctx.stroke();

            }
        }  
    }
}



function displayRects1D(img){



    // cellMatrix = gameOfLifeRound(cellMatrix);

    for (let j = 0; j < cellMatrix.length; j++){

        ctx.beginPath();
        ctx.strokeStyle="#cccccc";
        ctx.moveTo(j,0);
        ctx.lineTo(j, cellMatrix.length);
        ctx.stroke();

        for (let k = 0; k<cellMatrix.length; k++){

            if (cellMatrix[j+1][k+1]==1){

                ctx.beginPath();
                ctx.lineWidth=".3";
                ctx.strokeStyle="#cccccc";
                ctx.fillStyle = "#4010aa";
                // ctx.globalAlpha = 0.9;
                ctx.drawImage(img, j*cellSize, k*cellSize, cellSize, cellSize, j*cellSize-cellSize,k*cellSize, cellSize, cellSize);
                ctx.restore();

                // ctx.rect(j*cellSize,k*cellSize, cellSize, cellSize);
                ctx.stroke();

            }
        }  
    }
}



    function changeCellsWithCursor(canvas, event) {

        var boundingRect = canvas.getBoundingClientRect();
        var x = Math.floor((event.clientX - boundingRect.left)/cellSize) +2; //+1;
        var y = Math.floor((event.clientY - boundingRect.top)/cellSize)+1;
        // var x = Math.floor((event.offsetX)/cellSize)+1;
        // var y = Math.floor((event.offsetY)/cellSize);

        let slot = y*matrixSize+x

        var eType = event.type

        if (eType == "click"){
                
                flipCell(x,y);
                displayRects(overlayImg)
             }


        if (mouseDown  && !justChanged.includes(slot)) {
                

                    // flipCell(x,y);

                    if (!event.shiftKey){
                      cellMatrix[x][y] = 1;  
                    }else{

                        cellMatrix[x][y] = 0; 
                    }
                    
                    justChanged.push(slot);
                    displayRects(overlayImg)




        }

    }


function oneDBoard(firstRow, rule){

    let prevRow = firstRow;
    console.log(firstRow);
    console.log(prevRow);
    for (let i = 0; i < matrixSize ; i++){

        cellMatrix.push(prevRow);
        prevRow = oneDNextRow(prevRow, rule);


    }




}
// cellMatrix = populateBoard();



// var c = document.getElementById("myCanvas");
// var ctx = c.getContext("2d");
    




 


