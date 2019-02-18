// (function() {

    const guessView = new GuessAreaView();
    const guessArea = new GuessArea(guessView, {
        onPlayerWins() {
            console.log("WIN");
        },

        onPlayerFails() {
            console.log("FAIL");
        }
    });

    const startArea = new StartArea(guessArea);

    document.addEventListener('touchend', function() {
        const found = document.querySelector('.fake-mobile-input');

        found.focus();
        found.click();
    });

    guessArea.setWord('3dhubs');

    document.addEventListener('keyup', function(ev) {
        guessArea.guessLetter(ev.key.toLowerCase());
    });
//}());
