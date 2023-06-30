# Fun Freaking Friday
- Are you tired of spending all week thinking of icebreaker questions, only to have your team members (or that one team member) shit on them?
- Well, fear not, for this app contains a list of AI-generated icebreaker questions for you to use!
- In addition, you can track which questions have been asked and record everyone's answers. 
- You have the chance to rate people's answers too. Now you can get revenge on them by telling them how consistently shitty their answers are.
- You also have the chance to include a rating of your mood after the session. Now you can tell the team member how much his/her words hurt - with data!
- The app can help you visualize rating and mood as well! Graphs!

## Release
- A Windows release (.exe) is available. Non-windows users will have to build from source following the installation instructions.

## Installation
- This app is built on Python 3.11 but should run with >= Python 3.9.
- If you use pipenv, just run `pipenv install` from root directory.
    - For local development, install the dev packages as well using  `pipenv install --dev`
    - This will automatically enforce using Python 3.11. If you don't have it installed or don't want to use it, use the `requirements.txt` file.
    - Virtualenvs are encouraged!
- A Dockerfile is provided, but some additional tweaking may be needed to run the visualizations. They use the `matplotlib` library.

## Contributions
- To contribute to this project, make a PR against main.
- GitHub Actions will automatically run linters and stylers.  Those need to pass to allow merge. To run these locally first, run `./lint.sh` from root in the terminal.

## Future Enhancements
- Port over to use a real GUI
- Provide lint.sh for Windows users
- Unit tests
- Fix all the Docker stuff
- ??