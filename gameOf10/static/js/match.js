/////////////////////////////////////////////////////
/////////////////VARIABLES///////////////////////////
/////////////////////////////////////////////////////
var board = new Array(13);
var row = new Array(13);
var k = 0;
var selectedCard = null;
const op = ['-','+','/','*'];
var cardPlacedInfo = [];

/////////////////////////////////////////////////////
/////////////////INIT FUNCTIONS//////////////////////
/////////////////////////////////////////////////////
//once the website is loaded, the code below will be run
/*
const timerInterval = setInterval(() => {
    // Split the time into minutes and seconds
    let [sec, decisec] = document.querySelector('#timer b').innerHTML.split(":").map(Number);

    // Calculate the total time in seconds
    let totalDecisec = sec * 100 + decisec;

    // Decrease the total time
    totalDecisec--;

    if (totalDecisec < 0) {
        // Stop the timer when it reaches 0
        clearInterval(timerInterval);
        alert('Time out')
    } else {
        // Update the time display
        sec = Math.floor(totalDecisec / 100);
        decisec = totalDecisec % 100;

        time = `${String(sec).padStart(2, '0')}:${String(decisec).padStart(2, '0')}`;

        // Update the timer display
        document.querySelector('#timer b').innerHTML = time;
    }
}, 10); // Update every second (1000 milliseconds)
*/

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

    if (!myTurn){
        //check if it is my turn
        var refreshTurn = setInterval(() => {
            fetch('/getMyTurn/')
            .then(response => response.json())
            .then(data => {
                if(data['myTurn']){
                    clearInterval(refreshTurn);
                    location.reload();
                }
                
            })
        }, 1000);
    }else
        alert('It is your turn');

};

/////////////////////////////////////////////////////
/////////////////FUNCTIONS///////////////////////////
/////////////////////////////////////////////////////
//these are function that will  be called in EVENTS/INIT FUNCTIONS

function submitAction(){
    var redirectLink = "";
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const data = new FormData();
    data.append('action',JSON.stringify(cardPlacedInfo))
    data.append('csrfmiddlewaretoken',csrfToken)
    console.log("test")

    fetch('/submit/',{
        method: 'POST',
        body: data,
        credentials: 'same-origin',
    })
    .then(response => {
        if (response.status == 200)
            setTimeout(() => {
                location.reload();
            }, 500); 
        else
            return response.json()
    })
    .then(data => {
        if (data)
            alert(data.message)
    })
}

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
        //if is not myTurn
        if(myTurn == false){
            alert("ERROR! It is not your turn, please wait");
            return;
        }

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

        cardPlacedInfo.push({
            'row':el.dataset['row'],
            'column':el.dataset['column'],
            'val':selectedCard.innerHTML,
        })
        el.innerHTML = selectedCard.innerHTML;
        selectedCard.classList.add('used');
        selectedCard.style.transform = '';
        selectedCard = null;        
    }
})