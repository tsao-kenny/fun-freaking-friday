from service import App


def main() -> None:
    print("=== Fun Freaking Friday App ===")
    app = App()
    while True:
        _ = app.main_window()


if __name__ == "__main__":
    main()
