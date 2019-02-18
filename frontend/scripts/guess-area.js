const MAX_MISTAKES = 5;
const ALLOWED_LETTERS = /^[0-9A-Za-z]$/;

class GuessProcess {
    constructor(view, events) {
        this.word = null;
        this.gaps = 0;
        this.mistakes = 0;
        this.showed = {};
        this.faults = {};

        this.view = view;
        this.events = events;
    }

    setWord(word) {
        this.word = word;
        this.gaps = word.length;
        this.mistakes = 0;
        this.showed = {};
        this.faults = {};

        this.view.reset();
        this.view.addWordPlaces(word.length);
    }

    tryLetter(letter) {
        if (!letter.match(ALLOWED_LETTERS)) {
            return;
        }

        if (this.gaps === 0) {
            return;
        }

        if (this.mistakes >= MAX_MISTAKES) {
            return;
        }

        if (this.word.includes(letter)) {
            this.showLetter(letter);
        } else {
            this.showMistake(letter);
        }
    }

    showLetter(letter) {
        if (letter in this.showed) {
            return;
        }

        this.showed[letter] = true;

        for (let i=0; i < this.word.length; ++i) {
            if (letter === this.word[i]) {
                this.gaps -= 1;
                this.view.setWordLetter(i, letter);
            }
        }

        if (this.gaps === 0 && this.events.onPlayerWins) {
            this.events.onPlayerWins();
        }
    }

    showMistake(letter) {
        if (letter in this.faults) {
            return;
        }

        this.mistakes += 1;
        this.faults[letter] = true;
        this.view.addMistakeLetter(letter);

        if (this.mistakes >= MAX_MISTAKES && this.events.onPlayerFails) {
            this.events.onPlayerFails();
        }
    }
}
