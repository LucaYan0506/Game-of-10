/////////////////////////////////////////////////////
/////////////////VARIABLES///////////////////////////
/////////////////////////////////////////////////////
var board = new Array(13);
var row = new Array(13);
var k = 0;
var selectedCard = null;
const op = ['-','+','/','*'];

/////////////////////////////////////////////////////
/////////////////INIT FUNCTIONS//////////////////////
/////////////////////////////////////////////////////
//once the website is loaded, the code below will be run

//generate possible value
window.onload = function() {
    //get each board-item and save it into board
    document.querySelectorAll('#board .board-item').forEach(element => {
        if (k % 13 == 0){
            board[(k / 13) - 1] = row;
            row = new Array(13);
            row[0] = element;
        }else{
            row[k % 13] = element;
        }
        k++;
        })
    //save last line of the board
    board[(k / 13) - 1] = row;


    //fill board
    for (var n = 0; n < board_detail.length; n++){
        var i = Math.floor(n / 13), j = n % 13;
        board[i][j].innerHTML = board_detail[n];
    }
};

/////////////////////////////////////////////////////
/////////////////FUNCTIONS///////////////////////////
/////////////////////////////////////////////////////
//these are function that will  be called in EVENTS/INIT FUNCTIONS

//not used
function newCard(val){
    var isOp = false;
    op.forEach(x =>{
        if (val == x)
            isOp = true;
    })

    if(isOp)
        return op[Math.floor(Math.random() * op.length)];

    return Math.floor(Math.random() * 10);
}

/////////////////////////////////////////////////////
/////////////////EVENTS//////////////////////////////
/////////////////////////////////////////////////////
//these are events of different element

document.querySelectorAll('#card-container .card').forEach(el => {
    el.onclick = () => {
        if(selectedCard)
            selectedCard.style.transform = '';

        if(selectedCard == el){
            selectedCard = null;
            return;
        }

        el.style.transform = 'translate(0, -20px)';
        selectedCard = el;
    }
})

document.querySelectorAll('#board .board-item').forEach(el => {
    el.onclick = () => {
        //if no card is selected
        if(selectedCard == null){
            alert("ERROR! Please select a card");
            return;
        }

        //if this cell has already a value (this means that a card is already placed in this cell)
        if (el.innerHTML != "" && el.innerHTML != " "){
            alert("ERROR! You can't place it here");
            return;
        }

        el.innerHTML = selectedCard.innerHTML;
        selectedCard.classList.add('used');
        selectedCard.style.transform = '';
        selectedCard = null;        
    }
})










