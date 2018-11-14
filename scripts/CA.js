"use strict";


let matrixSize = 64;

let cellMatrix = [];
let neighborDict = {};


let repDict = { 0:'_', 1:'█'}





function populateBoard(){  

    let matrix = [] 


    for (let i = 0; i < matrixSize ; i++) {
        let cellRow = [];

        for (let j = 0; j < matrixSize ; j++){
            let cellVal=0;
            
            if (Math.floor(Math.random() * 11) > 6){
                cellVal = 1 ;
            }
            
            cellRow.push(cellVal);
        }    
        matrix.push(cellRow);
    }

    return matrix;

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






cellMatrix = populateBoard();

var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
    


    




function display_rects(img){

    cellMatrix = gameOfLifeRound(cellMatrix);

    for (let j = 0; j < cellMatrix.length; j++){

        ctx.beginPath();
        ctx.strokeStyle="#cccccc";
        ctx.moveTo(j,0);
        ctx.lineTo(j, cellMatrix.length);
        ctx.stroke();

        for (let k = 0; k<cellMatrix.length; k++){

            if (cellMatrix[j][k]==1){

                ctx.beginPath();
                ctx.lineWidth=".3";
                ctx.strokeStyle="#cccccc";
                ctx.fillStyle = "#4010aa";
                // ctx.globalAlpha = 0.9;
                ctx.drawImage(img, j*16, k*16, 16, 16, j*16-16,k*16, 16, 16);
                ctx.restore();

                // ctx.rect(j*16,k*16, 16, 16);
                ctx.stroke();

            }
        }  
    }
}







 


