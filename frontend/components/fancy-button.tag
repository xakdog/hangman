<fancy-button>
    <button class={ className }>
        <yield />
    </button>

    <style>
        .fancy-button {
            font-size: 18px;
            font-family: 'Arvo', serif;

            outline: none;
            padding: 12px 18px;
            border-radius: 4px;
            border: 2px solid black;
            background: transparent;

            transition: linear 80ms;

            user-select: none;
            -webkit-user-select: none;
            -webkit-appearance: none;
            -webkit-tap-highlight-color: rgba(0,0,0,0);
        }

        .fancy-button:active {
            transform: translate(2px, 1px);
        }

        .fancy-button_disabled {
            opacity: 0.1;
        }

        .fancy-button_disabled:active {
            transform: none;
        }
    </style>

    <script>
        this.className = "fancy-button";

        if (opts.disabled) {
            this.className += " fancy-button_disabled";
        }
    </script>
</fancy-button>
