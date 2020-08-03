eSim Version Change
====

It contains the documentation for the changes to be done when a new release is to be made.


# Changes for eSim version Update:

1. `master/VERSION` - Change the version number

2. `master/conf.py` - Update `release` variable

3. `master/setup.py` - Update `version` field in `setup` function

4. User Manual
    - Download eSim Manual from eSim website and add it to `library/browser/User-Manual/`.
    - Update user manual filename as `eSim_Manual_y.x.pdf` where y.x is the updated version.
    - Update path in the following line at `master/src/browser/UserManual.py` with the updated manual name:
    ```python
    file = os.path.realpath('library/browser/User-Manual/eSim_Manual_2.0.pdf')
    ```

5. `master/src/configuration/Appconfig.py` - In function `def __init__ (self)` , update the variable `self._VERSION`

6. `master/INSTALL` - Update the installer file names according to the latest version.

7. `installers/Windows/esim-setup-script.nsi` - Update the following lines in this script:
        ```nsi
        !define PRODUCT_VERSION "y.x"
        !define VERSION "a.b.c.d"

        OutFile "eSim-y.x_install.exe"
        ```

8. `master/README.md` - Update new features, OS support and other changes that were made in the new version.
