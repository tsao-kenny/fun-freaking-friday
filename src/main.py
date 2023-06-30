"""
Fun Freaking Friday
v0.01 - 20230623
Initial conception
"""


from service import App


def main() -> None:
    """Main entrypoint"""
    print("=== Fun Freaking Friday App ===")
    app = App()
    while True:
        app.main_window()


if __name__ == "__main__":
    main()
