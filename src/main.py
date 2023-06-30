from service import App


def main():
    print("=== Fun Freaking Friday App ===")
    app = App()
    playing = True
    while playing:
        playing = app.main_window()
        

if __name__ == "__main__":
    main()
