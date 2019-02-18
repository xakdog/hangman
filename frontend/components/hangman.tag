<hangman>
    <stage-start
        if={ stage == 'start' }
        onstartpressed={ beginGame }
        loading={ loading }
    />
    <stage-guess
        if={ stage === 'guess' }
        ondone={ onDone }
        loading={ loading }
    />

    <stage-win if={ stage === 'win' } />
    <stage-loose if={ stage === 'loose' } />

    <script>
        const API_GAME_START = '/fake-data.json'

        this.word = '';
        this.stage = 'start';

        beginGame() {
            this.stage = 'guess';
            this.update();
        }

        onDone(result) {
            if (result === 'win' || result === 'loose') {
                this.stage = result;
                this.update();
            }

            this.loadWord();
        }

        async loadWord() {
            const res = await fetch(API_GAME_START);
            const data = await res.json();

            console.log(data);
        }
    </script>
</hangman>
