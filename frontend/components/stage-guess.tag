<stage-guess>
    <div class="guess-area game-area">
        <img class="game-area__logo" src="hangman-game.svg" />

        <p class="game-area__rules">
            Press keys to fill the gaps.<br>
            You have only 5 attemps.
        </p>

        <input class="fake-mobile-input" />

        <div class="game-area__word">
            <letter each={ this.opened } type="box">{ letter }</letter>
        </div>
        <div class="game-area__mistakes">
            <letter each={ this.mistaken } type="cross-out">{ letter }</letter>
        </div>
    </div>

    <script>
        this.opened = [];

        const view = {
            reset: () => {
                this.opened = [];
                this.mistaken = [];
            },

            addWordPlaces: (length) => {
                this.opened = Array(length);
                this.update();
            },

            addMistakeLetter: (letter) => {
                this.mistaken.push({ letter });
                this.update();
            },

            setWordLetter: (idx, letter) => {
                this.opened[idx] = { letter };
                this.update();
            },
        };

        const events = {
            onPlayerWins: () => setTimeout(() => opts.ondone('win'), 1000),
            onPlayerFails: () => setTimeout(() => opts.ondone('loose'), 1000),
        };

        const guess = new GuessProcess(view, events);

        guess.setWord('3dhubs');

        document.addEventListener('keyup', function(ev) {
            guess.tryLetter(ev.key.toLowerCase());
        });
    </script>
</stage-guess>
