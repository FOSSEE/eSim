# Building eSim installation packages

## Linux
### Build dependecies
- Python 2.7
- [PyQt4](https://pypi.org/project/PyQt4/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [pyinstaller](https://www.pyinstaller.org/)
- [fpm](https://github.com/jordansissel/fpm)

### Steps for building installation packages
- Navigate to `eSim/build-scripts` directory from a terminal
- Run `./esim-build-linux.sh`
- .deb, .rpm, .sh packages will be built into `./dist` directory

## Windows
### Build dependecies
- Python 2.7
- [PyQt4](https://pypi.org/project/PyQt4/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [pyinstaller](https://www.pyinstaller.org/)
- [InnoSetup](https://github.com/jrsoftware/issrc)

### Steps for building installation package
_TODO_