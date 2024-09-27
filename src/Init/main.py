def main() -> None:
    from ..App.App import App, AudioWrapper
    
    App.init_game()
    AudioWrapper.init_audio()
    App.run()


if __name__ == "__main__":
    main()
