eSim Version Change
====

Following are the changes to be done when a new release of eSim is to be made:

1. `master/VERSION` - Change the version number

2. `master/conf.py` - Update `version` and `release` variables

3. `master/setup.py` - Update `version` field in `setup` function

4. User Manual
    - Manual name convention is `eSim_Manual_y.x.pdf` where y.x is the updated version.
    - Update path in the following line at `master/src/browser/UserManual.py` with the updated manual name:
    
        ```python
        manual = 'library/browser/User-Manual/eSim_Manual_y.x.pdf'
        ```

5. `master/src/configuration/Appconfig.py` - In function `def __init__ (self)` , update the variable `self._VERSION`

6. `master/INSTALL` - Update the installer file names according to the latest version.

7. `installers/Windows/esim-setup-script.nsi` - Update the following lines in this script:

    ```nsi
    !define PRODUCT_VERSION "y.x"
    !define VERSION "a.b.c.d"
    
    OutFile "eSim-y.x_installer.exe"
    ```

8. `master/README.md` - Update new features, OS support and other changes that were made in the new version.
