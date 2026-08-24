# eSim 2.5 Installation Issues on Ubuntu 25.04

## FOSSEE Semester Long Internship — Autumn 2026

### Screening Task 4 — eSim Upgradation

---

## 1. Objective

The objective of this task is to investigate the problems encountered while installing eSim 2.5 on Ubuntu 25.04, identify the root causes of the problems, and fix the issues wherever possible.

The investigation focuses on the eSim installation scripts, particularly the Bash-based installer and its dependency installation process.

---

## 2. Test Environment

| Component           | Details             |
| ------------------- | ------------------- |
| Operating System    | Ubuntu 25.04        |
| Architecture        | x86_64              |
| Virtualization      | VirtualBox          |
| eSim Version        | 2.5                 |
| Shell               | Bash                |
| Installation method | eSim Bash installer |

The testing is being performed inside an Ubuntu 25.04 virtual machine.

---

# 3. Initial Installation Attempt

The eSim 2.5 package was downloaded and extracted according to the installation instructions provided with eSim.

The provided installation procedure is:

```bash
unzip eSim-2.5.zip
cd eSim-2.5
chmod +x install-eSim.sh
./install-eSim.sh --install
```

The first installation attempt was performed without modifying the installer in order to reproduce the original problems.

---

# 4. Issue 1 — Ubuntu 25.04 Version Detection Failure

## 4.1 Description

The original eSim 2.5 installer does not proceed with the installation on Ubuntu 25.04.

The installer produces the following output:

```text
Detected Ubuntu Version:
Unsupported Ubuntu version: 25.04 ()
```

The installation terminates before the dependency installation stage is reached.

---

## 4.2 Investigation

The relevant code in `install-eSim.sh` is:

```bash
get_ubuntu_version() {
    VERSION_ID=$(grep "^VERSION_ID" /etc/os-release | cut -d '"' -f 2)
    FULL_VERSION=$(lsb_release -d | grep -oP '\d+\.\d+\.\d+')
    echo "Detected Ubuntu Version: $FULL_VERSION"
}
```

The installer obtains `VERSION_ID` from `/etc/os-release`.

However, `FULL_VERSION` is obtained by extracting a version matching the following regular expression:

```text
\d+\.\d+\.\d+
```

This pattern expects three numerical components, for example:

```text
22.04.4
```

Ubuntu 25.04 reports its release as:

```text
25.04
```

Therefore, the regular expression does not match the Ubuntu 25.04 version and `FULL_VERSION` becomes empty.

This explains the output:

```text
Detected Ubuntu Version:
```

---

## 4.3 Additional Problem

The installer also contains a version-selection `case` statement that explicitly handles only Ubuntu 22.04, 23.04 and 24.04:

```bash
case $VERSION_ID in
    "22.04")
        ...
        ;;
    "23.04")
        ...
        ;;
    "24.04")
        ...
        ;;
    *)
        echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
        exit 1
        ;;
esac
```

Ubuntu 25.04 is not included.

Therefore, even if the `FULL_VERSION` detection problem is corrected, Ubuntu 25.04 still needs to be handled by the installer.

---

## 4.4 Current Status

**Investigated — Fix under development**

The root cause of the version parsing problem has been identified.

A possible improvement is to obtain the release version directly using:

```bash
lsb_release -rs
```

instead of parsing the human-readable description using a three-component regular expression.

The appropriate installation script/path for Ubuntu 25.04 still needs to be determined before considering the complete issue fixed.

---

# 5. Issue 2 — Bash Syntax Error in the `installers` Branch

## 5.1 Description

After checking out the `installers` branch as specified in the FOSSEE submission procedure, the repository has a different installer structure.

The Ubuntu installer is located at:

```text
Ubuntu/install-eSim.sh
```

When attempting to run:

```bash
./install-eSim.sh --install
```

from the `Ubuntu` directory, Bash reports:

```text
./install-eSim.sh: line 70: syntax error near unexpected token `}'
./install-eSim.sh: line 70: `}'
```

The installer therefore fails before the installation process can begin.

---

## 5.2 Reproduction

From the repository's `installers` branch:

```bash
cd ~/eSim/Ubuntu
./install-eSim.sh --install
```

Observed output:

```text
./install-eSim.sh: line 70: syntax error near unexpected token `}'
./install-eSim.sh: line 70: `}'
```

---

## 5.3 Investigation Status

The exact cause of the syntax error has not yet been determined.

The next investigation step is to inspect the source around line 70 and perform a Bash syntax check using:

```bash
nl -ba install-eSim.sh | sed -n '50,80p'
```

and:

```bash
bash -n install-eSim.sh
```

The working tree will also be checked to determine whether the syntax error is present in the original branch or was introduced by local modifications.

---

## 5.4 Current Status

**Reproduced — Root cause under investigation**

No changes have been made to the installer for this issue yet.

---

# 6. Methodology

For each installation problem, the following procedure is being followed:

1. Reproduce the issue on Ubuntu 25.04.
2. Record the exact error message.
3. Inspect the relevant installer code.
4. Determine the root cause.
5. Develop a minimal fix where possible.
6. Test the modification.
7. Record the result.
8. Continue the installation to identify subsequent problems.
9. Document both fixed and unresolved issues.

Temporary modifications may be used during investigation to allow the installer to proceed to subsequent stages, as permitted by the task instructions.

---

# 7. Issue Status Summary

| Issue   | Description                              | Status       |
| ------- | ---------------------------------------- | ------------ |
| Issue 1 | Ubuntu 25.04 version detection failure   | Investigated |
| Issue 2 | Bash syntax error in `installers` branch | Reproduced   |

Additional dependency issues will be added as they are encountered during the installation.

---

# 8. Planned Investigation

The next steps are:

* Investigate the Bash syntax error in `Ubuntu/install-eSim.sh`.
* Determine the correct Ubuntu 25.04 installation path.
* Continue the installation after fixing/blocking the initial errors.
* Identify dependency problems such as Python, LLVM, KiCad, NGHDL, NgVeri and other components where encountered.
* Fix important installation-blocking issues.
* Re-test the complete installation from a clean Ubuntu 25.04 environment.
* Update this report with the exact commands, errors, fixes and test results.

---

## 9. Conclusion

The initial investigation shows that eSim 2.5 has compatibility problems when its installer is used with Ubuntu 25.04.

The first problem is related to Ubuntu version detection in the original eSim 2.5 installer. A second problem was encountered after switching to the `installers` branch: the Ubuntu installer currently terminates with a Bash syntax error.

Further investigation and testing are required to determine the complete set of installation issues and implement reliable fixes.
