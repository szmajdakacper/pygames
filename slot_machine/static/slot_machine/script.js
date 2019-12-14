window.onload = function () {
    //Hidden for every sensitive field until animation is running
    info_text = document.getElementById('info_text');
    info_text.style.visibility = 'hidden';
    balance = document.getElementById('balance');
    balance_value = balance.value;
    balance.value = '---';
    squares = document.getElementsByClassName('square');
    for (let square of squares) {
        square.style.visibility = 'hidden';
    }
    //chceck if animation in every row is ended
    row0 = document.querySelector('#board_row0');
    roll_row0 = row0.querySelector('#roll');
    roll_row0.addEventListener("animationend", function () {
        afterAnimation(row0);
    }, false);
    row1 = document.querySelector('#board_row1');
    roll_row1 = row1.querySelector('#roll');
    roll_row1.addEventListener("animationend", function () {
        afterAnimation(row1);
        info_text.style.visibility = 'visible';
        balance.value = balance_value;
    }, false);
    row2 = document.querySelector('#board_row2');
    roll_row2 = row2.querySelector('#roll');
    roll_row2.addEventListener("animationend", function () {
        afterAnimation(row2);
    }, false);
}
function afterAnimation(row) {
    rolls = row.getElementsByClassName('roll');
    for (let roll of rolls) {
        roll.style.background = 'white';
    }
    squares = row.getElementsByClassName('square');
    for (let square of squares) {
        square.style.visibility = 'visible';
        var img = square.innerHTML;
        square.innerHTML = "<img src='/static/slot_machine/img/" + img + ".png'>";
    }
}