#!/bin/bash
#=============================================================================
#          FILE: install-eSim.sh
#
#         USAGE: ./install-eSim.sh --install
#                ./install-eSim.sh --uninstall
#                ./install-eSim.sh --dry-run     (preview profile + actions)
#
#   DESCRIPTION: Unified installer for the eSim EDA Suite on Ubuntu.
#                ONE script, version-aware via detect_profile(). Replaces the
#                old per-version install-eSim-scripts/install-eSim-XX.04.sh set
#                that drifted out of sync (only 24.04 was maintained).
#
#                Supported: Ubuntu 23.04 / 24.04 / 25.04 / 26.04
#                Target app: current master (PyQt6 + QScintilla code editor,
#                            kicadLibrary as dir-or-tarball, KiCad 8/9).
#
#                Idempotent: safe to re-run. --install cleans eSim-owned bits
#                first, so reinstall over ANY prior eSim version is clean.
#
#       AUTHORS: Fahim Khan, Rahul Paknikar, Saurabh Bansode, Sumanto Kar,
#                Partha Singha Roy, Jayanth Tatineni, Anshul Verma,
#                Shiva Krishna Sangati, Harsha Narayana P
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: June 2026 — unified version-profile rewrite
#=============================================================================

# NOTE: `set -e`/`set -E` + an ERR trap are enabled only inside --install
# (see Main). We deliberately do NOT use `set -u`/`pipefail` globally: `set -u`
# breaks `source <venv>/bin/activate`, and `pipefail` would abort harmless
# `ls | grep` detections when grep matches nothing. All profile vars are
# explicitly initialised below instead.

#-----------------------------------------------------------------------------
# Globals
#-----------------------------------------------------------------------------
config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=""        # resolved by resolve_esim_home()
ESIM_VERSION=""     # read from $eSim_Home/VERSION once the root is known
PROFILE_SUMMARY=""  # one-line profile description, filled by detect_profile

# The install sequence as "<function>:<label shown to the user>".
#
# ONE list drives both --install and the --dry-run plan, so the preview can
# never claim a different set of steps from the one that actually runs, and
# the progress bar's denominator is never hand-maintained. Steps run as plain
# function calls in the current shell -- no subshell, no backgrounding, no
# redirection -- which is what keeps `source <venv>/bin/activate`, `die`, and
# every interactive prompt behaving exactly as they did before.
INSTALL_STEPS=(
    "cleanLegacyEsim:Clearing artifacts of older eSim installs"
    "createConfigFile:Writing eSim configuration"
    "installDependency:Installing system packages and virtualenv"
    "installQt:Installing PyQt6 and QScintilla"
    "installKicad:Installing KiCad"
    "copyKicadLibrary:Installing the eSim symbol library"
    "installNghdl:Building NGHDL and ngspice"
    "installSky130Pdk:Installing the SKY130 PDK"
    "installIhpPdk:Installing the IHP Open PDK"
    "installChatbot:Installing the eSim AI Assistant"
    "createDesktopStartScript:Creating the launcher and desktop entry"
    "runToolchainDoctor:Verifying the simulation toolchain"
)

# Profile vars (filled by detect_profile)
UBUNTU_VER=""
KICAD_SOURCE=""     # ppa | universe
KICAD_PPA=""
KICAD_MIN_MAJOR=""
QT_PKGS="python3-pyqt6 python3-pyqt6.qtsvg pyqt6-dev-tools"
QSCI_PKG="python3-pyqt6.qsci"

# Third-party Python deps installed with pip (everything heavy comes from apt).
# ONE place to bump; installPythonDeps just loops over this array. Keep IN SYNC
# with the pinned block in windows/requirements-windows.txt -- both OSes must
# install the same versions, and windows/tests/test_packaging_pins.py fails if
# the two lists drift.
#
# These are external tools the maker/Makerchip flows shell out to, not
# libraries the app imports, so each carries an UPPER bound: an unannounced new
# major otherwise changes a CLI under an installer nobody rebuilt to test it.
# pyhdlparser has no PyPI release and its old `tarball/master` URL was both a
# moving ref and a stale branch name (upstream renamed master -> main; GitHub
# serves master only via a legacy redirect), so it is pinned to a commit --
# same idiom as ICARUS_REF in nghdl/install-nghdl.sh.
PYHDLPARSER_REF="e1153ace8ca1e25f9fb53350c41058ef8eb8dacf"
PIP_PINS=(
    "watchdog>=3.0"
    "https://github.com/hdl/pyhdlparser/tarball/$PYHDLPARSER_REF"
    "sandpiper-saas>=1.1.0,<2"
    "volare>=0.20.6,<0.21"      # 0.x: the MINOR is the breaking unit
)

# Local models the optional eSim AI Assistant uses. Keep IN SYNC with
# REQUIRED_MODELS in src/chatbot/chatbot_thread.py -- the chat window downloads
# any missing one on its first start, which is the surprise installChatbot
# avoids; Ubuntu/tests/test_chatbot_step.py fails if the two lists drift.
CHATBOT_MODELS=("qwen2.5:3b" "nomic-embed-text")

#-----------------------------------------------------------------------------
# Terminal UI
#-----------------------------------------------------------------------------
# Presentation only: this section prints, it never decides what gets installed.
# It is deliberately written to be inert under failure, because it runs inside
# the `set -e` / `set -E` / `trap ... ERR` region that --install turns on:
#
#   * every helper ends in `return 0`, so a cosmetic hiccup can never abort a
#     healthy install;
#   * no arithmetic in statement position -- `(( i++ ))` evaluates to 0 and so
#     RETURNS 1 on the first increment, which under `set -e` would kill the
#     installer. Assignments (`x=$((x+1))`) carry no such trap;
#   * no install step is ever backgrounded, subshelled, or has its output
#     hidden. That is what keeps `source <venv>/bin/activate`, `die`'s exit,
#     the `read -rp` prompts and sudo's password prompt behaving exactly as
#     they did before this block existed;
#   * every read is `${x:-}`, so the block is safe under `set -u` too
#     (bootstrap.sh runs `set -euo pipefail` and carries the detection half).
#
# Three levels, chosen by ui_detect:
#   2 full   UTF-8 + colour TTY   box drawing, block bars, braille spinner
#   1 basic  colour TTY, no UTF-8 ASCII art, same layout
#   0 plain  no TTY / NO_COLOR / TERM=dumb / ESIM_NO_FANCY=1
# Level 0 reproduces the output this installer had before the UI was added,
# which is what makes ESIM_NO_FANCY=1 a complete kill switch.
#
# TTY detection probes /dev/tty instead of `[ -t 1 ]`: --install reassigns
# stdout to a `tee` pipe and under `curl | bash` stdin is the download pipe, so
# both usual tests report "not a terminal" on a perfectly normal interactive
# install. Terminal SIZE has the same problem -- `tput cols` silently falls
# back to terminfo's 80 columns when stdout is not a tty -- so the size is read
# with `stty size < /dev/tty`.
#
# The progress bar is pinned to the last line of the window with a DECSTBM
# scroll region, the same mechanism apt's own Dpkg::Progress-Fancy uses, so
# apt/make output scrolls normally in the region above it. It is written to
# /dev/tty, never to stdout, so it cannot leak into $HOME/eSim-install.log.
#-----------------------------------------------------------------------------

UI_LEVEL=0             # 0 plain | 1 basic | 2 full
UI_TTY=""              # /dev/tty once we know we have one
UI_ROWS=24
UI_COLS=80
UI_STICKY=0            # is the scroll region currently armed?
UI_SPIN=0              # spinner frame, advanced on each repaint
UI_STEP=0
UI_TOTAL=0
UI_LABEL=""
UI_T0=0
UI_STEP_T0=0

# --- capability detection ---------------------------------------------------
ui_detect() {
    UI_LEVEL=0

    # An explicit opt-out always wins. NO_COLOR is the cross-tool convention
    # (no-color.org); honour it rather than inventing an eSim-only variable.
    [ -n "${ESIM_NO_FANCY:-}" ] && return 0
    [ -n "${NO_COLOR:-}" ]      && return 0
    case "${TERM:-dumb}" in dumb|"") return 0 ;; esac

    # Writable controlling terminal? The one test that survives both the tee
    # pipe and `curl | bash`.
    { : > /dev/tty; } 2>/dev/null || return 0
    UI_TTY=/dev/tty

    # ...but openable is not the same as usable. A process can hold a
    # controlling terminal that reports a 1x1 (or unreadable) window -- seen
    # under WSL, and under any harness that inherits a pts without a real
    # window behind it. Painting a bottom-pinned bar onto that is worse than
    # printing nothing, so an implausible size demotes us to plain output.
    ui_measure || { UI_TTY=""; return 0; }

    local ncolors=0
    ncolors=$(tput colors 2>/dev/null) || ncolors=0
    [ "${ncolors:-0}" -ge 8 ] 2>/dev/null || return 0
    UI_LEVEL=1

    # Box drawing and braille only render as intended under a UTF-8 charmap;
    # under LANG=C they arrive as mojibake, which reads as broken rather than
    # fancy. `locale charmap` is authoritative; the variables are the fallback
    # for the rare image with no locale binary.
    local charmap=""
    charmap=$(locale charmap 2>/dev/null) || charmap=""
    case "${charmap}:${LC_ALL:-}:${LC_CTYPE:-}:${LANG:-}" in
        *UTF-8*|*utf8*|*UTF8*|*utf-8*) UI_LEVEL=2 ;;
    esac
    return 0
}

# Terminal size, read from the terminal itself (see header note on tput cols).
# Returns non-zero when no plausible size is available, which ui_detect reads
# as "there is no usable terminal here". Callers that only want to refresh the
# numbers (the WINCH trap) must swallow that with `|| true`.
ui_measure() {
    [ -n "$UI_TTY" ] || return 1
    local size="" r c
    size=$(stty size < "$UI_TTY" 2>/dev/null) || return 1
    case "$size" in
        *[0-9]*' '*[0-9]*) r=${size%% *}; c=${size##* } ;;
        *) return 1 ;;
    esac
    # A window too small to spare two rows for the bar, or narrower than the
    # step rule, is treated as no terminal at all rather than being clamped
    # up to a fictional 80x24.
    [ "${r:-0}" -ge 10 ] 2>/dev/null || return 1
    [ "${c:-0}" -ge 40 ] 2>/dev/null || return 1
    UI_ROWS=$r
    UI_COLS=$c
    # Very wide terminals: keep the layout readable instead of stretching a
    # rule across 200 columns.
    [ "$UI_COLS" -gt 96 ] && UI_COLS=96
    return 0
}

# --- palette and glyphs -----------------------------------------------------
# eSim's brand gold, sampled from images/esim_text.png (the official wordmark):
# #F0B030 body, #FFE65F highlight, #B07020 shade. NOT the #53D7FF app-theme
# accent -- that is the dark theme's UI colour, whereas the logo and wordmark
# a user actually recognises are metallic gold.
#
# C_BRAND_ROW carries one shade per wordmark row, bright at the top and deep
# at the bottom, which reproduces the gradient of the printed logo. Truecolor
# when the terminal advertises it, nearest xterm-256 cube entries otherwise,
# plain bold yellow at level 1.
ui_palette() {
    C_RESET=''; C_DIM=''; C_BOLD=''; C_ACCENT=''; C_OK=''; C_WARN=''; C_ERR=''
    C_BRAND_ROW=('' '' '' '' '')

    if [ "$UI_LEVEL" -ge 1 ]; then
        C_RESET=$'\033[0m'; C_DIM=$'\033[2m'; C_BOLD=$'\033[1m'
        C_ACCENT=$'\033[33m'; C_OK=$'\033[32m'; C_WARN=$'\033[33m'; C_ERR=$'\033[31m'
        C_BRAND_ROW=($'\033[1;33m' $'\033[1;33m' $'\033[33m' $'\033[33m' $'\033[33m')
        local ncolors=0
        ncolors=$(tput colors 2>/dev/null) || ncolors=0
        if [ "${ncolors:-0}" -ge 256 ] 2>/dev/null; then
            C_ACCENT=$'\033[38;5;214m'; C_OK=$'\033[38;5;114m'
            C_WARN=$'\033[38;5;208m';   C_ERR=$'\033[38;5;203m'
            C_BRAND_ROW=($'\033[38;5;221m' $'\033[38;5;221m' $'\033[38;5;214m' \
                         $'\033[38;5;172m' $'\033[38;5;130m')
        fi
        case "${COLORTERM:-}" in
            truecolor|24bit)
                C_ACCENT=$'\033[38;2;240;160;48m'; C_OK=$'\033[38;2;126;211;133m'
                C_WARN=$'\033[38;2;255;140;26m';   C_ERR=$'\033[38;2;235;110;110m'
                C_BRAND_ROW=($'\033[38;2;255;230;95m'  $'\033[38;2;251;208;74m' \
                             $'\033[38;2;240;176;48m'  $'\033[38;2;216;148;40m' \
                             $'\033[38;2;176;112;32m')
                ;;
        esac
    fi

    if [ "$UI_LEVEL" -ge 2 ]; then
        G_RULE='─'; G_HEAVY='━'; G_V='│'
        G_TL='╭'; G_TR='╮'; G_BL='╰'; G_BR='╯'; G_LT='├'; G_RT='┤'
        G_FULL='█'; G_EMPTY='░'; G_CAPL='▐'; G_CAPR='▌'
        G_OK='✔'; G_WARN='▲'; G_ERR='✖'; G_ARROW='▸'; G_DOT='·'; G_CLOCK='◷'
        UI_FRAMES='⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏'
    else
        G_RULE='-'; G_HEAVY='='; G_V='|'
        G_TL='+'; G_TR='+'; G_BL='+'; G_BR='+'; G_LT='+'; G_RT='+'
        G_FULL='#'; G_EMPTY='.'; G_CAPL='['; G_CAPR=']'
        G_OK='ok'; G_WARN='!'; G_ERR='x'; G_ARROW='>'; G_DOT='-'; G_CLOCK='T'
        UI_FRAMES='- \ | /'
    fi
    return 0
}

# Repeat $2 exactly $1 times. Pure bash on purpose: a `tr`-based repeat mangles
# the multi-byte glyphs above, and this is called several times per redraw.
ui_rep() {
    local n=${1:-0} ch=${2:-} s=''
    [ "$n" -gt 0 ] 2>/dev/null || return 0
    printf -v s '%*s' "$n" ''
    printf '%s' "${s// /$ch}"
    return 0
}

ui_hms() {
    local s=${1:-0}
    if [ "$s" -ge 3600 ] 2>/dev/null; then
        printf '%dh%02dm' $((s / 3600)) $(((s % 3600) / 60))
    else
        printf '%dm%02ds' $((s / 60)) $((s % 60))
    fi
    return 0
}

# Strip CSI sequences so ${#...} measures PRINTED width -- without this every
# coloured row is padded short by the length of its own escape codes. Each
# iteration consumes at least one character, so it always terminates even on a
# malformed sequence.
ui_visible() {
    local s="${1:-}" out='' head
    while [ -n "$s" ]; do
        head=${s%%$'\033'*}
        out="$out$head"
        s=${s#"$head"}
        [ -n "$s" ] || break
        s=${s#$'\033'}
        s=${s#[}
        case "$s" in
            *m*) s=${s#*m} ;;
            *)   s='' ;;
        esac
    done
    printf '%s' "$out"
    return 0
}

# --- banner -----------------------------------------------------------------
# The wordmark is drawn with half-block glyphs (▀ ▄ █), which put TWO vertical
# pixels in every character cell. That doubled resolution is the whole point:
# a whole-block grid can only manage crude capitals, so the old banner spelled
# a blocky "ESIM", while the product -- and images/esim_text.png, its official
# wordmark -- is "eSim", with a lowercase e, a capital S, a dotted i and a
# lowercase m. 28 columns wide, 5 rows tall, 10 pixel rows.
UI_WORDMARK=(
    '        ▄████▄  ██          '
    '        ██                  '
    '▄█▀▀█▄   ████   ██  ████████'
    '██▀▀▀▀      ██  ██  ██ ██ ██'
    '▀█▄▄█▀  ▀████▀  ██  ██ ██ ██'
)
UI_WORDMARK_W=28

ui_banner() {
    local ver="${1:-}" sub="${2:-}"
    # Wordmark (28) + indent (2) + gutter (3) = 33 columns before any label,
    # so below 72 there is no usable room for one: print the plain header
    # rather than a box with its right border shoved off screen.
    if [ "$UI_LEVEL" -lt 2 ] || [ "$UI_COLS" -lt 72 ]; then
        echo
        echo "=== eSim EDA Suite $ver -- FOSSEE, IIT Bombay ==="
        [ -n "$sub" ] && echo "    $sub"
        echo
        return 0
    fi

    # Clip the labels to what is left beside the wordmark. They are the only
    # variable-length text in the banner, so this is what keeps it rectangular.
    local lmax=$((UI_COLS - 2 - UI_WORDMARK_W - 5))
    [ "${#sub}" -gt "$lmax" ] && sub="${sub:0:$((lmax - 1))}…"
    [ "${#ver}" -gt "$lmax" ] && ver="${ver:0:$((lmax - 1))}…"

    # Label for each wordmark row; blank rows give the mark room to breathe.
    local labels=(
        ""
        "${C_BOLD}eSim EDA Suite${C_RESET}  ${C_DIM}$ver${C_RESET}"
        "${C_DIM}FOSSEE $G_DOT IIT Bombay${C_RESET}"
        ""
        "${C_DIM}$sub${C_RESET}"
    )

    local w=$((UI_COLS - 2)) i
    printf '\n%s%s%s%s%s\n' "$C_ACCENT" "$G_TL" "$(ui_rep "$w" "$G_RULE")" "$G_TR" "$C_RESET"
    ui_boxline "$C_ACCENT" ""
    for i in 0 1 2 3 4; do
        ui_boxline "$C_ACCENT" \
            "  ${C_BRAND_ROW[$i]}${UI_WORDMARK[$i]}${C_RESET}   ${labels[$i]}"
    done
    ui_boxline "$C_ACCENT" ""
    printf '%s%s%s%s%s\n' "$C_ACCENT" "$G_BL" "$(ui_rep "$w" "$G_RULE")" "$G_BR" "$C_RESET"
    return 0
}

# --- step framing -----------------------------------------------------------
ui_plan() {                       # ui_plan <total-steps>
    UI_TOTAL=${1:-1}
    UI_T0=$SECONDS
    return 0
}

ui_step() {                       # ui_step "Installing KiCad"
    ui_step_close
    UI_STEP=$((UI_STEP + 1))
    UI_LABEL="${1:-}"
    UI_STEP_T0=$SECONDS

    if [ "$UI_LEVEL" -lt 1 ]; then
        printf '\n>>> [%d/%d] %s\n' "$UI_STEP" "$UI_TOTAL" "$UI_LABEL"
        return 0
    fi

    local pct=$((UI_STEP * 100 / UI_TOTAL)) fill
    fill=$((UI_COLS - ${#UI_LABEL} - 18))
    [ "$fill" -lt 3 ] && fill=3
    printf '\n%s%s%s [%02d/%02d] %s%s%s %s%s%s %s%3d%%%s\n' \
        "$C_ACCENT" "$G_HEAVY$G_HEAVY$G_HEAVY" "$C_RESET" \
        "$UI_STEP" "$UI_TOTAL" "$C_BOLD" "$UI_LABEL" "$C_RESET" \
        "$C_ACCENT" "$(ui_rep "$fill" "$G_HEAVY")" "$C_RESET" \
        "$C_DIM" "$pct" "$C_RESET"

    # Re-assert the scroll region at step boundaries only. apt's needrestart
    # prompt and any debconf/whiptail dialog reset it to the full window when
    # they exit; re-arming here heals that. Doing it on every 1 Hz repaint
    # instead would fight such a dialog while it is still on screen.
    ui_bar_arm
    ui_bar_draw
    return 0
}

# Result line for the step that just finished (no-op before the first step).
ui_step_close() {
    [ "$UI_STEP" -gt 0 ] || return 0
    local d=$((SECONDS - UI_STEP_T0))
    if [ "$UI_LEVEL" -lt 1 ]; then
        printf '    done (%s)\n' "$(ui_hms "$d")"
    else
        printf '  %s%s%s %s%s %s %s%s\n' \
            "$C_OK" "$G_OK" "$C_RESET" "$C_DIM" "$UI_LABEL" "$G_DOT" "$(ui_hms "$d")" "$C_RESET"
    fi
    return 0
}

# --- message helpers --------------------------------------------------------
# Both repaint the bar afterwards. That is the ONLY thing that keeps its clock
# and spinner moving -- see the note on ui_bar_render about why nothing repaints
# it concurrently -- so the bar advances whenever the install says something.
ui_log() {
    if [ "$UI_LEVEL" -lt 1 ]; then
        echo -e "\n>>> $*"
    else
        printf '  %s%s%s %s\n' "$C_ACCENT" "$G_ARROW" "$C_RESET" "$*"
    fi
    ui_bar_draw
    return 0
}

ui_warn() {
    if [ "$UI_LEVEL" -lt 1 ]; then
        echo -e "[WARN] $*" >&2
    else
        printf '  %s%s %s%s\n' "$C_WARN" "$G_WARN" "$*" "$C_RESET" >&2
    fi
    ui_bar_draw
    return 0
}

# --- sticky bottom progress bar ---------------------------------------------
ui_bar_arm() {
    [ "$UI_LEVEL" -ge 2 ] || return 0
    [ -n "$UI_TTY" ]      || return 0
    [ "${ESIM_UI_STICKY:-1}" = 0 ] && return 0
    [ "$UI_ROWS" -ge 10 ] || return 0          # too short to spare two rows

    # DECSTBM moves the cursor to home, and whether the two newlines scrolled
    # the window depends on where the cursor already was -- so rather than
    # trying to restore the old position, park deterministically on the last
    # row of the new region. Output then appends there and scrolls inside it.
    {
        printf '\n\n'
        printf '\033[1;%dr' $((UI_ROWS - 2))
        printf '\033[%d;1H' $((UI_ROWS - 2))
        printf '\033[?25l'
    } > "$UI_TTY" 2>/dev/null && UI_STICKY=1
    return 0
}

ui_bar_disarm() {
    [ "$UI_STICKY" = 1 ] || return 0
    UI_STICKY=0
    {
        printf '\033[1;%dr' "$UI_ROWS"            # restore full-window scrolling
        printf '\033[%d;1H\033[2K' $((UI_ROWS - 1))
        printf '\033[%d;1H\033[2K' "$UI_ROWS"
        printf '\033[%d;1H' $((UI_ROWS - 1))
        printf '\033[?25h'
    } > "$UI_TTY" 2>/dev/null || true
    return 0
}

ui_bar_draw() {
    [ "$UI_STICKY" = 1 ] || return 0
    UI_SPIN=$((UI_SPIN + 1))
    ui_bar_render "$UI_STEP" "$UI_TOTAL" "$UI_T0" "$UI_LABEL"
    return 0
}

# The actual paint.
#
# Nothing repaints this concurrently, and that is deliberate. An earlier
# version ran a 1 Hz ticker in a background subshell so the clock kept moving
# through a long quiet step. It corrupted the display: the cursor save/restore
# this function needs (DECSC/DECRC, ESC 7 / ESC 8) is a SINGLE terminal-wide
# slot, so the ticker would save the cursor, the installer's own output would
# move it, and the ticker's restore then dropped the next line on top of an
# already-drawn row -- eating a banner row on nearly every run.
#
# A background writer cannot be made safe against an output stream it does not
# own, so the bar is now painted only from the main shell (ui_step, ui_log,
# ui_warn, SIGWINCH). apt's own Dpkg::Progress-Fancy works the same way. The
# cost is that the clock advances when the install says something rather than
# once a second; the benefit is that the screen is never corrupted.
ui_bar_render() {
    local step=${1:-0} total=${2:-1} t0=${3:-0} label="${4:-}"
    local frame="" pct=0 elapsed=$((SECONDS - t0))
    local frames=($UI_FRAMES)
    frame=${frames[UI_SPIN % ${#frames[@]}]}
    [ "${total:-0}" -gt 0 ] 2>/dev/null && pct=$((step * 100 / total))

    local right left width fill rest bar
    printf -v right '%s %s' "$G_CLOCK" "$(ui_hms "$elapsed")"
    printf -v left  '%s %d/%d %s' "${frame:- }" "$step" "$total" "$label"

    width=$((UI_COLS - ${#left} - ${#right} - 12))
    [ "$width" -lt 8 ]  && width=8
    [ "$width" -gt 30 ] && width=30
    fill=$((pct * width / 100))
    rest=$((width - fill))
    printf -v bar '%s%s%s%s%s%s%s%s' \
        "$C_ACCENT" "$G_CAPL" "$(ui_rep "$fill" "$G_FULL")" \
        "$C_DIM" "$(ui_rep "$rest" "$G_EMPTY")" \
        "$C_RESET$C_ACCENT" "$G_CAPR" "$C_RESET"

    {
        printf '\0337'                                       # DECSC: save cursor
        printf '\033[%d;1H\033[2K' $((UI_ROWS - 1))
        printf '%s%s%s' "$C_DIM" "$(ui_rep "$UI_COLS" "$G_RULE")" "$C_RESET"
        printf '\033[%d;1H\033[2K' "$UI_ROWS"
        printf ' %s%s%s %s %s%3d%%%s  %s%s%s' \
            "$C_ACCENT" "$left" "$C_RESET" "$bar" \
            "$C_BOLD" "$pct" "$C_RESET" "$C_DIM" "$right" "$C_RESET"
        printf '\0338'                                       # DECRC: restore
    } > "$UI_TTY" 2>/dev/null || true
    return 0
}

# --- result boxes -----------------------------------------------------------
ui_box() {                        # ui_box <colour> <glyph> <title> [key val]...
    local col="${1:-}" glyph="${2:-}" title="${3:-}"; shift 3
    local w=$((UI_COLS - 2)) k v

    if [ "$UI_LEVEL" -lt 2 ]; then
        echo
        echo "=== $title ==="
        while [ "$#" -ge 2 ]; do printf '  %-12s %s\n' "$1" "$2"; shift 2; done
        echo
        return 0
    fi

    printf '\n%s%s%s%s%s\n' "$col" "$G_TL" "$(ui_rep "$w" "$G_RULE")" "$G_TR" "$C_RESET"
    ui_boxline "$col" "  ${col}${glyph}${C_RESET}  ${C_BOLD}${title}${C_RESET}"
    if [ "$#" -ge 2 ]; then
        printf '%s%s%s%s%s\n' "$col" "$G_LT" "$(ui_rep "$w" "$G_RULE")" "$G_RT" "$C_RESET"
        while [ "$#" -ge 2 ]; do
            k="$1"; v="$2"; shift 2
            ui_boxrow "$col" "$k" "$v"
        done
    fi
    printf '%s%s%s%s%s\n' "$col" "$G_BL" "$(ui_rep "$w" "$G_RULE")" "$G_BR" "$C_RESET"
    return 0
}

# One key/value row, wrapped onto continuation rows when the value is wider
# than the box. Wrapping rather than truncating because most values here are
# paths and package lists, where the tail is the informative part -- and
# letting a long value simply run past the frame (the previous behaviour) blew
# the right border off on any terminal narrower than the content.
ui_boxrow() {
    local col="${1:-}" key="${2:-}" val="${3:-}"
    local kw=11 vmax line
    vmax=$((UI_COLS - 2 - 2 - kw - 1))
    [ "$vmax" -lt 8 ] && vmax=8

    if [ -z "$val" ]; then
        ui_boxline "$col" "$(printf '  %s%-*s%s' "$C_DIM" "$kw" "$key" "$C_RESET")"
        return 0
    fi

    while [ -n "$val" ]; do
        if [ "${#val}" -le "$vmax" ]; then
            line=$val; val=''
        else
            line=${val:0:$vmax}
            # Prefer a word boundary; if the chunk holds no space we hard-split
            # rather than loop forever on one very long token.
            case "$line" in *' '*) line=${line% *} ;; esac
            val=${val:${#line}}; val=${val# }
        fi
        ui_boxline "$col" "$(printf '  %s%-*s%s %s' "$C_DIM" "$kw" "$key" "$C_RESET" "$line")"
        key=''
    done
    return 0
}

ui_boxline() {
    local col="${1:-}" text="${2:-}" bare pad
    bare=$(ui_visible "$text")
    pad=$((UI_COLS - 2 - ${#bare}))
    [ "$pad" -lt 0 ] && pad=0
    printf '%s%s%s%s%s%s%s\n' \
        "$col" "$G_V" "$C_RESET" "$text" "$(ui_rep "$pad" ' ')" "$col$G_V" "$C_RESET"
    return 0
}

# --- lifecycle --------------------------------------------------------------
# Armed by --install only. Restores the terminal on EVERY exit path (normal
# end, `die`, the ERR trap, Ctrl-C, SIGTERM): a hidden cursor or a stale scroll
# region left behind after an abort is a genuinely user-hostile bug, and is the
# main reason this block is trap-heavy.
ui_begin() {
    trap 'ui_end'           EXIT
    trap 'ui_end; exit 130' INT
    trap 'ui_end; exit 143' TERM
    # `|| true`: ui_measure reports failure by exit status, and an unguarded
    # non-zero inside a trap handler would trip the installer's ERR trap.
    trap 'ui_measure || true; ui_bar_arm; ui_bar_draw' WINCH
    ui_bar_arm
    return 0
}

# Idempotent, and must never call `exit`: EXIT traps preserve the script's
# status only as long as they do not set one of their own.
ui_end() {
    ui_bar_disarm
    return 0
}

#-----------------------------------------------------------------------------
# Helpers
#-----------------------------------------------------------------------------
# log/warn keep their old signatures and call sites; only the rendering moved
# into the UI block above, which falls back to the original ">>> "/"[WARN] "
# prefixes at level 0.
log()  { ui_log "$@"; }
warn() { ui_warn "$@"; }

# die() and error_exit() hand the terminal back BEFORE reporting, so the
# report lands on a clean screen rather than inside the scroll region that is
# about to be torn down. ui_end is idempotent and safe to call before
# ui_begin, so this works during the pre-flight phase too.
die() {
    ui_end
    ui_box "${C_ERR:-}" "${G_ERR:-x}" "Installation aborted" \
        "Reason" "$(printf '%s' "$*" | head -n 1)"
    printf '%s\n\n' "$*" >&2
    exit 1
}

# ERR trap for --install. Naming the step that failed is the point: the old
# text ("Kindly resolve the above error(s)") left the user scrolling a
# 40-minute log with no idea which phase had died.
error_exit() {
    ui_end
    ui_box "${C_ERR:-}" "${G_ERR:-x}" "Installation failed" \
        "Failed at" "step ${UI_STEP:-?}/${UI_TOTAL:-?} ${UI_LABEL:-(pre-flight)}" \
        "Full log"  "$HOME/eSim-install.log" \
        "Retry"     "./install-eSim.sh --install  (safe: keeps what installed)"
}

# Locate the eSim root (the dir holding VERSION + src/ + library/). Works when
# run from the repo root, from Ubuntu/, or from an extracted release zip root.
resolve_esim_home() {
    local d
    for d in "$(pwd)" \
             "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" \
             "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; do
        if [ -f "$d/VERSION" ] && [ -d "$d/src" ] && [ -d "$d/library" ]; then
            eSim_Home="$d"
            return 0
        fi
    done
    die "Cannot locate the eSim root (need VERSION + src/ + library/).
       cd into the top-level eSim directory and run ./install-eSim.sh again."
}

# Fail fast on insufficient disk BEFORE any apt work, with a message that
# says exactly how much to free. A fresh install needs roughly (measured on
# real 24.04/26.04 installs):
#   /      ~3.5 GB  apt payloads (KiCad ~0.5 GB, GHDL+LLVM ~0.7 GB, Qt/python/
#                   build tools, deb download cache) + SKY130 PDK ~0.7 GB
#   $HOME  ~1.5 GB  eSim tree + venv + nghdl build scratch (~1 GB peak)
# On a RE-install most of that is already on disk, so low space only warns.
# Without this check the install used to run for 20 minutes and then quietly
# skip the simulator build — see installNghdl(), which is now fatal instead.
preflightDisk() {
    if [ -n "${ESIM_SKIP_DISK_CHECK:-}" ]; then
        warn "ESIM_SKIP_DISK_CHECK set — skipping the disk-space preflight."
        return 0
    fi

    local root_fs home_fs free_root free_home short=""
    root_fs=$(df -Pk /       | awk 'NR==2 {print $1}')
    home_fs=$(df -Pk "$HOME" | awk 'NR==2 {print $1}')
    free_root=$(df -Pk /       | awk 'NR==2 {print $4}')
    free_home=$(df -Pk "$HOME" | awk 'NR==2 {print $4}')
    # df failed or gave nothing parseable — don't block the install on it.
    [ -n "$free_root" ] && [ -n "$free_home" ] || return 0

    if [ "$root_fs" = "$home_fs" ]; then
        [ "$free_home" -lt 5000000 ] && short="$((free_home / 1024)) MB free \
on $HOME — a fresh install needs ~5 GB (apt packages + PDKs + simulator build)"
    else
        [ "$free_root" -lt 3500000 ] && short="$((free_root / 1024)) MB free \
on / — apt packages + PDKs need ~3.5 GB"
        [ -z "$short" ] && [ "$free_home" -lt 1500000 ] && \
            short="$((free_home / 1024)) MB free on $HOME — the simulator \
build needs ~1.5 GB"
    fi
    [ -z "$short" ] && return 0

    if [ -f "$config_dir/$config_file" ]; then
        warn "Low disk space: $short."
        warn "Continuing because an existing eSim install was found (re-installs"
        warn "reuse most of it), but watch for out-of-space failures below."
        return 0
    fi
    die "Not enough disk space: $short.
       Free up space and re-run ./install-eSim.sh --install.
       (ESIM_SKIP_DISK_CHECK=1 bypasses this check.)"
}

# Set per-version profile variables. Single source of truth for what differs
# between Ubuntu releases.
detect_profile() {
    if [ ! -r /etc/os-release ]; then
        die "/etc/os-release not readable — cannot detect Ubuntu version."
    fi
    UBUNTU_VER=$(grep '^VERSION_ID=' /etc/os-release | cut -d '"' -f 2)

    case "$UBUNTU_VER" in
        23.04)
            # Lunar is EOL; best-effort. KiCad 9 PPA may not publish for lunar,
            # installKicad falls back to universe automatically.
            KICAD_SOURCE="ppa"; KICAD_PPA="kicad/kicad-9.0-releases"; KICAD_MIN_MAJOR=7
            warn "Ubuntu 23.04 is end-of-life. Support is best-effort."
            ;;
        24.04)
            KICAD_SOURCE="ppa"; KICAD_PPA="kicad/kicad-9.0-releases"; KICAD_MIN_MAJOR=9
            ;;
        25.04)
            # KiCad 9 PPA is unreliable on plucky; universe ships KiCad 8.
            KICAD_SOURCE="universe"; KICAD_MIN_MAJOR=8
            ;;
        26.04)
            KICAD_SOURCE="universe"; KICAD_MIN_MAJOR=9
            ;;
        22.04)
            die "Ubuntu 22.04 LTS is not supported.
       Its apt repositories ship Verilator 4 and KiCad 6, but this eSim needs
       Verilator 5 and KiCad >= 7 (PyQt6 GUI, Verilator-5 NgVeri build, and the
       KiCad-9 custom netlister). Please use Ubuntu 24.04 LTS or 26.04 LTS."
            ;;
        *)
            die "Unsupported Ubuntu version: $UBUNTU_VER
       Supported: 23.04, 24.04, 25.04, 26.04 (24.04 LTS / 26.04 LTS recommended)"
            ;;
    esac

    # Deliberately silent: the resolved profile is surfaced by the caller --
    # in the banner subtitle for --install, in the plan box for --dry-run --
    # so that it reads as part of the header instead of as a stray log line
    # printed before the header exists.
    PROFILE_SUMMARY="Ubuntu $UBUNTU_VER $G_DOT KiCad $KICAD_MIN_MAJOR+ via $KICAD_SOURCE"
}

#-----------------------------------------------------------------------------
# Install steps
#-----------------------------------------------------------------------------
createConfigFile() {
    log "Writing $config_dir/$config_file"
    mkdir -p "$config_dir"
    rm -f "$config_dir/$config_file"
    {
        echo "[eSim]"
        echo "eSim_HOME = $eSim_Home"
        echo "LICENSE = %(eSim_HOME)s/LICENSE"
        echo "KicadLib = %(eSim_HOME)s/library/kicadLibrary"
        echo "IMAGES = %(eSim_HOME)s/images"
        echo "VERSION = %(eSim_HOME)s/VERSION"
        echo "MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json"
    } >> "$config_dir/$config_file"
}

# Sweep artifacts of OLD eSim releases (2.x and earlier) so installing on
# top of any prior eSim just works. Each install step below already cleans
# and regenerates its own bits (config, venv, launcher, symbols, ngspice,
# SKY130); this handles only what old releases left OUTSIDE those paths.
# Everything touched here is eSim-owned — user files (old extracted eSim
# directories, zips) are reported, never deleted.
cleanLegacyEsim() {
    log "Checking for artifacts of an older eSim install"

    # Legacy-format symbol libs: this eSim ships only .kicad_sym. The install
    # rsync never deletes, so stale eSim_*.lib from old releases would linger
    # in /usr/share forever (uninstall already removes them).
    sudo rm -f /usr/share/kicad/symbols/eSim_*.lib 2>/dev/null || true

    # Old eSim's KiCad PPA entries (kicad-6.0 era). On a newer/upgraded
    # Ubuntu those PPAs publish no Release file, which makes every
    # `apt-get update` below fail hard. installKicad re-adds the right
    # source for this Ubuntu version, so dropping them is always safe.
    if ls /etc/apt/sources.list.d/kicad* &>/dev/null; then
        warn "Removing old KiCad apt sources left by a previous eSim:"
        ls /etc/apt/sources.list.d/kicad* | sed 's/^/       /'
        sudo rm -f /etc/apt/sources.list.d/kicad*
    fi

    # Old nghdl (eSim <= 2.5) compiled GHDL from source into /usr/local —
    # typically the mcode backend. /usr/local/bin shadows /usr/bin in PATH,
    # so it would hijack the apt ghdl-llvm/gcc this installer sets up and
    # break VHDL co-simulation (mcode cannot link the nghdl socket server).
    if [ -x /usr/local/bin/ghdl ]; then
        warn "Found /usr/local/bin/ghdl: $(/usr/local/bin/ghdl --version 2>/dev/null | head -n 1)"
        warn "It shadows the GHDL this installer sets up (old eSim/nghdl builds put it there)."
        read -rp "Remove the /usr/local GHDL? (y/n): " g
        if [[ "$g" =~ ^[Yy] ]]; then
            sudo rm -rf /usr/local/bin/ghdl /usr/local/bin/ghdl1-* \
                        /usr/local/lib/ghdl /usr/local/include/ghdl*
            log "/usr/local GHDL removed"
        else
            warn "Keeping it — VHDL co-simulation will likely use THIS ghdl (PATH order) and fail."
        fi
    fi

    # Old standalone nghdl GUI launcher; nghdl is embedded in eSim now and
    # the tree it pointed at is usually gone. (Uninstall removes it too.)
    sudo rm -f /usr/local/bin/nghdl 2>/dev/null || true

    # Purely informational — old trees that are no longer referenced once
    # this install repoints the launcher and ~/.esim/config.ini. Dirs only
    # (the glob would otherwise flag the user's freshly-downloaded release
    # .zip/.sha256), and never the tree we are installing FROM: the release
    # zip extracts to eSim-2.x/, so $eSim_Home itself matches the glob —
    # telling the user their live install is "safe to delete" broke installs.
    local d
    for d in "$HOME/ngspice-nghdl" "$HOME"/eSim-2.* "$HOME"/Downloads/eSim-2.*; do
        [ -d "$d" ] || continue
        [ "$(realpath "$d" 2>/dev/null)" = "$(realpath "$eSim_Home" 2>/dev/null)" ] && continue
        warn "Old eSim-era directory found: $d (unused after this install — safe to delete)"
    done
    return 0
}

installDependency() {
    log "Updating apt index"
    set +e; trap "" ERR
    sudo apt-get update
    set -e; trap error_exit ERR

    log "Installing base system packages"
    sudo apt-get install -y \
        python3-full python3-venv python3-virtualenv python3-pip \
        xterm xz-utils unzip rsync git build-essential \
        python3-psutil python3-setuptools \
        python3-matplotlib python3-numpy python3-scipy

    log "Creating virtualenv (with system site-packages so apt Qt is visible)"
    rm -rf "$config_dir/env"
    if command -v virtualenv &>/dev/null; then
        virtualenv --system-site-packages "$config_dir/env"
    else
        python3 -m venv --system-site-packages "$config_dir/env"
    fi
    # shellcheck disable=SC1091
    source "$config_dir/env/bin/activate"
    pip install --upgrade pip

    # eSim-specific pure-python deps not packaged in apt. Heavy/native deps
    # (PyQt6, matplotlib, numpy, scipy) come from apt above to stay mutually
    # consistent — pinning them via pip here is what made the old scripts fragile.
    log "Installing eSim Python deps (watchdog, hdlparse, sandpiper, volare)"
    # Each is optional at runtime -- eSim degrades gracefully when one is
    # absent -- so a failure warns and the install continues. watchdog used to
    # be installed WITHOUT a `|| warn`, which under `set +e` meant a failure
    # scrolled past silently; the loop gives every pin the same warning.
    set +e; trap "" ERR
    for spec in "${PIP_PINS[@]}"; do
        pip install "$spec" || warn "pip install '$spec' failed"
    done
    set -e; trap error_exit ERR
}

installQt() {
    log "Installing PyQt6 + QScintilla (apt)"
    sudo apt-get install -y $QT_PKGS
    sudo apt-get install -y "$QSCI_PKG" \
        || warn "$QSCI_PKG unavailable on this release — code editor will be disabled"

    # Verify the GUI toolkit actually imports inside the venv.
    # shellcheck disable=SC1091
    source "$config_dir/env/bin/activate"
    python3 -c "import PyQt6.QtWidgets" 2>/dev/null \
        || warn "PyQt6 import failed — eSim GUI will not start"
    python3 -c "import PyQt6.QtSvg" 2>/dev/null \
        || warn "PyQt6.QtSvg import failed — eSim GUI will not start (install python3-pyqt6.qtsvg)"
    python3 -c "import PyQt6.Qsci" 2>/dev/null \
        || warn "PyQt6.Qsci import failed — the code editor will be unavailable"
}

installKicad() {
    log "Installing KiCad (target major >= $KICAD_MIN_MAJOR)"

    if dpkg -s kicad &>/dev/null; then
        local cur
        cur=$(dpkg-query -W -f='${Version}' kicad | grep -oP '^\d+')
        if [ "${cur:-0}" -ge "$KICAD_MIN_MAJOR" ]; then
            log "KiCad $cur already installed (>= $KICAD_MIN_MAJOR) — keeping it"
            return 0
        fi
        warn "KiCad $cur installed but older than target major $KICAD_MIN_MAJOR"
        read -rp "Remove it and install KiCad >= $KICAD_MIN_MAJOR? (y/n): " r
        [[ "$r" =~ ^[Yy] ]] || die "Keeping existing KiCad $cur; aborting install."
        sudo apt-get remove --purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
        sudo apt-get autoremove -y
    fi

    sudo apt-get install -y software-properties-common

    if [ "$KICAD_SOURCE" = "ppa" ]; then
        if ! grep -rq "$KICAD_PPA" /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null; then
            log "Adding PPA ppa:$KICAD_PPA"
            set +e; trap "" ERR
            sudo add-apt-repository -y "ppa:$KICAD_PPA"
            local ppa_rc=$?
            set -e; trap error_exit ERR
            if [ $ppa_rc -ne 0 ]; then
                warn "KiCad PPA add failed (release may be unsupported) — falling back to universe"
                sudo add-apt-repository -y universe
            fi
        fi
    else
        sudo add-apt-repository -y universe
    fi

    sudo apt-get update
    sudo apt-get install -y --no-install-recommends \
        kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates

    local newmajor
    newmajor=$(dpkg-query -W -f='${Version}' kicad 2>/dev/null | grep -oP '^\d+')
    if [ "${newmajor:-0}" -ge "$KICAD_MIN_MAJOR" ]; then
        log "KiCad $newmajor installed"
    else
        warn "Installed KiCad major ${newmajor:-unknown} is below target $KICAD_MIN_MAJOR (eSim may still work)"
    fi
}

copyKicadLibrary() {
    log "Installing eSim KiCad symbol library"

    local libdir
    if [ -d "$eSim_Home/library/kicadLibrary" ]; then
        libdir="$eSim_Home/library/kicadLibrary"
    elif [ -f "$eSim_Home/library/kicadLibrary.tar.xz" ]; then
        tar -xJf "$eSim_Home/library/kicadLibrary.tar.xz" -C "$eSim_Home/library"
        libdir="$eSim_Home/library/kicadLibrary"
    else
        warn "No kicadLibrary (dir or tarball) found — skipping symbol library"
        return 0
    fi

    # The 3 libraries eSim rewrites at runtime when users build HDL models.
    local gen_libs=(eSim_Ngveri eSim_NgVeriCosim eSim_Nghdl) g

    # --- Static libraries are copied to an eSim-owned directory. They never
    #     share KiCad's system library directory, so their registrations can
    #     use stable absolute paths and uninstall never affects KiCad files.
    local staticdir="$config_dir/kicad_static"
    mkdir -p "$staticdir"
    rsync -a --delete \
        --exclude='eSim_Ngveri.kicad_sym' \
        --exclude='eSim_NgVeriCosim.kicad_sym' \
        --exclude='eSim_Nghdl.kicad_sym' \
        "$libdir/eSim-symbols/" "$staticdir/"

    # --- Generated libs: live in the user's own ~/.esim/kicad_symbols so the
    #     app never needs write access to /usr/share. Seed each ONCE ( -n ) —
    #     a reinstall must not clobber a user's accumulated models.
    local gendir="$config_dir/kicad_symbols"
    mkdir -p "$gendir"
    for g in "${gen_libs[@]}"; do
        cp -n "$libdir/eSim-symbols/$g.kicad_sym" "$gendir/" 2>/dev/null || true
    done

    # Seed sym-lib-table into the KiCad per-user config dir that actually exists
    # (do NOT hard-code 6.0 — the old scripts did and broke under KiCad 8/9).
    local cfg="$HOME/.config/kicad" ver
    ver=$(ls "$cfg" 2>/dev/null | grep -E '^[0-9]+\.[0-9]+$' | sort -V | tail -n 1)
    if [ -z "$ver" ]; then
        local major
        major=$(dpkg-query -W -f='${Version}' kicad 2>/dev/null | grep -oP '^\d+')
        ver="${major:-9}.0"
    fi
    mkdir -p "$cfg/$ver"
    log "Using KiCad config dir: $cfg/$ver"

    # Rewrite eSim library URIs to their owned absolute paths on a temporary
    # copy of the template (never modify the file inside $libdir).
    local tmptable
    tmptable=$(mktemp)
    cp "$libdir/template/sym-lib-table" "$tmptable"
    for g in "${gen_libs[@]}"; do
        sed -i "s|\${KICAD6_SYMBOL_DIR}/$g.kicad_sym|$gendir/$g.kicad_sym|g" \
            "$tmptable"
    done
    sed -i "s|\${KICAD6_SYMBOL_DIR}/eSim_|$staticdir/eSim_|g" "$tmptable"
    sed -i "s|@ESIM_STATIC_SYMBOL_DIR@|$staticdir|g" "$tmptable"
    cp "$tmptable" "$cfg/$ver/sym-lib-table" 2>/dev/null \
        || warn "sym-lib-table copy failed (eSim registers libs at runtime anyway)"
    rm -f "$tmptable"

    log "Static eSim symbols -> $staticdir"
    log "Generated symbols   -> $gendir (user-writable)"

    # The extracted copy is only needed during install.
    [ -f "$eSim_Home/library/kicadLibrary.tar.xz" ] && rm -rf "$libdir"
    return 0
}

installNghdl() {
    log "Installing NGHDL (GHDL/Verilator co-simulation)"

    # Release ships nghdl as nghdl.zip; dev repo ships it as a nghdl/ dir.
    if [ -f "$eSim_Home/nghdl.zip" ] && [ ! -d "$eSim_Home/nghdl" ]; then
        unzip -o "$eSim_Home/nghdl.zip" -d "$eSim_Home" >/dev/null
    fi

    # NGHDL is NOT optional: it is the only step that provides ngspice (no
    # apt line in this script installs a simulator), so an eSim without it
    # launches and draws schematics but cannot simulate ANYTHING. It used to
    # be treated as a skippable extra — which shipped exactly that broken
    # install, with a success banner and exit 0. Fail loudly instead.
    local nd="$eSim_Home/nghdl"
    if [ ! -d "$nd" ]; then
        die "nghdl not found (no nghdl/ dir, no nghdl.zip) in $eSim_Home.
       NGHDL provides ngspice itself — without it eSim cannot simulate.
       The download/zip is incomplete; re-download and re-run."
    fi
    if [ ! -f "$nd/nghdl-simulator-source.tar.xz" ]; then
        die "nghdl/nghdl-simulator-source.tar.xz missing from $eSim_Home.
       NGHDL provides ngspice itself — without it eSim cannot simulate.
       The download/zip is incomplete; re-download and re-run."
    fi

    chmod +x "$nd/install-nghdl.sh" 2>/dev/null || true

    # Run without the ERR trap so a failure reaches the clear message below
    # instead of the generic abort text.
    set +e; trap "" ERR
    ( cd "$nd" && ./install-nghdl.sh --install )
    local rc=$?
    set -e; trap error_exit ERR

    if [ $rc -eq 0 ]; then
        log "NGHDL installed"
    else
        die "NGHDL install failed (exit $rc).
       NGHDL provides ngspice — without it eSim cannot run any simulation,
       so this install is aborted rather than shipped broken. Fix the error
       above (usually disk space or network), then re-run
       ./install-eSim.sh --install — re-running is safe and keeps everything
       already installed."
    fi
}

installSky130Pdk() {
    log "Installing SKY130 PDK"
    local t="$eSim_Home/library/sky130_fd_pr.tar.xz"
    if [ ! -f "$t" ]; then
        warn "library/sky130_fd_pr.tar.xz missing — skipping SKY130 PDK"
        return 0
    fi
    sudo rm -rf /usr/share/local/sky130_fd_pr
    rm -rf "$eSim_Home/library/sky130_fd_pr"
    tar -xJf "$t" -C "$eSim_Home/library"
    # The pinned upstream PDK snapshot has one malformed Spectre-style
    # `include` line.  Ngspice treats it as a current source and refuses to
    # parse every sky130.lib corner, even for circuits that do not instantiate
    # that native 5 V device.  The shared helper applies only the exact known
    # repair and rejects unknown/incomplete PDK revisions.
    python3 "$eSim_Home/src/configuration/Sky130Prepare.py" \
        "$eSim_Home/library/sky130_fd_pr" \
        || die "SKY130 PDK validation/repair failed"
    sudo mkdir -p /usr/share/local
    sudo mv "$eSim_Home/library/sky130_fd_pr" /usr/share/local/
    sudo chown -R "$USER:$USER" /usr/share/local/sky130_fd_pr
}

installIhpPdk() {
    local script="$eSim_Home/ihp/ihp-install-script.sh"
    [ -f "$script" ] || { warn "IHP install script not found — skipping"; return 0; }

    read -rp "Install IHP Open PDK for analog IC design? (y/n): " ans
    if [[ ! "$ans" =~ ^[Yy] ]]; then
        log "Skipping IHP Open PDK"
        return 0
    fi
    chmod +x "$script"
    set +e; trap "" ERR
    ( cd "$eSim_Home/ihp" && ./ihp-install-script.sh --install )
    set -e; trap error_exit ERR
}

installChatbot() {
    read -rp "Install the eSim AI Assistant (downloads Ollama and ~2.2 GB of local AI models)? (y/n): " ans
    if [[ ! "$ans" =~ ^[Yy] ]]; then
        log "Skipping the eSim AI Assistant"
        return 0
    fi
    # Best-effort throughout: the assistant is optional, so a failed download
    # warns and eSim's own install carries on. eSim starts without it and
    # simply hides the assistant.
    set +e; trap "" ERR

    log "Installing the AI Assistant's Python packages"
    # shellcheck disable=SC1091
    source "$config_dir/env/bin/activate"
    # One guarded install per requirements-copilot.txt entry, like PIP_PINS:
    # a failure names its package and never stops the rest.
    local spec
    while read -r spec; do
        pip install "$spec" \
            || warn "pip install '$spec' failed -- eSim hides the assistant without it"
    done < <(grep -vE '^[[:space:]]*(#|$)' "$eSim_Home/requirements-copilot.txt")
    # Microphone input; the venv sees apt packages (--system-site-packages).
    sudo apt-get install -y python3-pyaudio \
        || warn "python3-pyaudio unavailable -- voice input will be disabled"

    if ! command -v ollama >/dev/null 2>&1; then
        log "Installing Ollama (official installer from ollama.com)"
        # zstd: Ollama ships a .tar.zst and its installer aborts without it.
        sudo apt-get install -y curl zstd
        curl -fsSL https://ollama.com/install.sh | sh
    fi
    if ! command -v ollama >/dev/null 2>&1; then
        warn "Ollama could not be installed -- get it from https://ollama.com; the assistant starts once it is present"
        set -e; trap error_exit ERR
        return 0
    fi

    # Ollama's installer starts a systemd service. Without systemd
    # (containers, WSL) nothing is serving yet, so run a temporary server just
    # for the downloads; the assistant starts its own when eSim needs one.
    local server="" model
    if ! ollama list >/dev/null 2>&1; then
        ollama serve >/dev/null 2>&1 &
        server=$!
        for _ in 1 2 3 4 5 6 7 8 9 10; do
            ollama list >/dev/null 2>&1 && break
            sleep 1
        done
    fi
    for model in "${CHATBOT_MODELS[@]}"; do
        log "Downloading AI model $model"
        ollama pull "$model" \
            || warn "Could not download $model -- the assistant fetches it on first start"
    done
    [ -n "$server" ] && kill "$server" 2>/dev/null
    set -e; trap error_exit ERR
    return 0
}

createDesktopStartScript() {
    log "Creating launcher (esim) + desktop entry"

    # The application anchors all resources to __file__ (configuration.paths),
    # so the launcher no longer needs to cd into src/frontEnd or source the
    # venv — invoking the venv's python directly is equivalent and quoting-safe.
    #
    # Default to software OpenGL (llvmpipe). Inside VirtualBox / headless / broken
    # -GPU-driver setups Mesa's hardware path fails with
    #   libEGL warning: failed to get driver name for fd -1
    #   MESA: error: ZINK: failed to choose pdev / egl: failed to create dri2 screen
    # eSim is a Qt Widgets + matplotlib app that needs no GPU, so forcing the
    # software path is free on real hardware and removes those errors in VMs.
    # All three vars are defaulted-not-forced (`:=`), so a user can still override.
    {
        echo '#!/bin/bash'
        echo ': "${LIBGL_ALWAYS_SOFTWARE:=1}"; export LIBGL_ALWAYS_SOFTWARE'
        echo ': "${QT_OPENGL:=software}"; export QT_OPENGL'
        echo ': "${EGL_LOG_LEVEL:=fatal}"; export EGL_LOG_LEVEL'
        printf 'exec "%s/env/bin/python3" "%s/src/frontEnd/Application.py" "$@"\n' \
            "$config_dir" "$eSim_Home"
    } > esim-start.sh
    sudo chmod 755 esim-start.sh
    sudo cp -p esim-start.sh /usr/bin/esim
    rm -f esim-start.sh

    cat > esim.desktop << EOF
[Desktop Entry]
Version=1.0
Name=eSim
Comment=EDA Tool
GenericName=eSim
Keywords=eda-tools
Exec=esim %u
Terminal=true
X-MultipleArgs=false
Type=Application
Icon=$config_dir/logo.png
Categories=Development;
StartupNotify=true
EOF
    sudo chmod 755 esim.desktop
    sudo cp -p esim.desktop /usr/share/applications/
    mkdir -p "$HOME/Desktop"
    cp -p esim.desktop "$HOME/Desktop/"

    set +e; trap "" ERR
    gio set "$HOME/Desktop/esim.desktop" "metadata::trusted" true
    chmod a+x "$HOME/Desktop/esim.desktop"
    rm -f esim.desktop
    set -e; trap error_exit ERR

    cp -p "$eSim_Home/images/logo.png" "$config_dir" 2>/dev/null || true
}

#-----------------------------------------------------------------------------
# Uninstall (version-agnostic, idempotent, best-effort throughout)
#-----------------------------------------------------------------------------
uninstall_eSim() {
    log "Removing eSim application files"
    # ~/.esim now also holds the generated KiCad symbol libs (kicad_symbols/),
    # so this one removal covers them too.
    sudo rm -rf "$HOME/.esim" "$HOME/Desktop/esim.desktop" \
                /usr/bin/esim /usr/share/applications/esim.desktop

    log "Removing KiCad (any version) + eSim symbols"
    sudo apt-get purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates 2>/dev/null || true
    sudo apt-get autoremove -y 2>/dev/null || true
    # Remove ONLY eSim's own files. /usr/share/kicad belongs to the kicad apt
    # package (purged above); never rm -rf the whole dir — that nuked KiCad's
    # standard libraries. Generated symbol libs now live under ~/.esim and are
    # already cleared by the "$HOME/.esim" removal at the top of this function.
    sudo rm -f /usr/share/kicad/symbols/eSim_*.kicad_sym \
               /usr/share/kicad/symbols/eSim_*.lib 2>/dev/null || true
    # Drop the now-empty dirs our mkdir -p created; --ignore-fail-on-non-empty
    # keeps this a no-op if KiCad (or anything else) still owns files there.
    sudo rmdir --ignore-fail-on-non-empty /usr/share/kicad/symbols \
               /usr/share/kicad 2>/dev/null || true
    sudo rm -f /etc/apt/sources.list.d/kicad* 2>/dev/null || true

    # Deleting the library FILES above leaves their REGISTRATIONS behind: every
    # eSim_* row eSim added to ~/.config/kicad/<ver>/sym-lib-table still points
    # at a path that no longer exists, and a KiCad the user reinstalls later
    # then reports a missing library on every schematic. Unregister them with
    # the same helper the Windows uninstaller runs. NOT sudo: the table is per
    # user, and under sudo $HOME would be root's.
    if [ -f "$eSim_Home/windows/uninstall_cleanup.py" ] && command -v python3 >/dev/null 2>&1; then
        python3 "$eSim_Home/windows/uninstall_cleanup.py" \
                --esim-root "$eSim_Home" --purge-user-data || true
    fi

    log "Removing SKY130 PDK"
    sudo rm -rf /usr/share/local/sky130_fd_pr

    log "Removing NGHDL"
    if [ -f "$eSim_Home/nghdl/install-nghdl.sh" ]; then
        ( cd "$eSim_Home/nghdl" && chmod +x install-nghdl.sh && ./install-nghdl.sh --uninstall ) || true
    else
        # nghdl never extracted, or release form — remove known artifacts.
        sudo rm -rf "$HOME/nghdl-simulator" "$HOME/.nghdl" \
                    /usr/local/bin/nghdl /usr/bin/ngspice 2>/dev/null || true
    fi

    log "Removing IHP Open PDK (if present)"
    if [ -f "$eSim_Home/ihp/ihp-install-script.sh" ]; then
        ( cd "$eSim_Home/ihp" && chmod +x ihp-install-script.sh && ./ihp-install-script.sh --uninstall ) || true
    fi

    # Clear runtime-generated NGHDL/NgVeri model XML so a later reinstall is clean.
    rm -rf "$eSim_Home"/library/modelParamXML/Nghdl/* \
           "$eSim_Home"/library/modelParamXML/Ngveri/* 2>/dev/null || true

    log "eSim uninstalled."
    log "Ollama and its models are kept (other applications may use them);"
    log "remove them with Ollama's own uninstall steps if no longer needed."
}

#-----------------------------------------------------------------------------
# Post-install self-check: the same toolchain doctor the app ships
# (Help menu / `esim --doctor`). Non-fatal: a red row here is exactly the
# actionable report we want the user to see, not an abort.
#-----------------------------------------------------------------------------
runToolchainDoctor() {
    log "Running the simulation-toolchain doctor (esim --doctor)"
    set +e; trap "" ERR
    "$config_dir/env/bin/python3" "$eSim_Home/src/frontEnd/Application.py" --doctor
    local rc=$?
    set -e; trap error_exit ERR
    if [ $rc -ne 0 ]; then
        warn "Toolchain doctor reported missing pieces (see report above)."
        warn "eSim will run; the affected flows will explain what to fix."
    fi
}

#-----------------------------------------------------------------------------
# Proxy prompt (optional)
#-----------------------------------------------------------------------------
setupProxy() {
    read -rp "Is your internet connection behind a proxy? (y/n): " getProxy
    if [[ "$getProxy" =~ ^[Yy] ]]; then
        read -rp  "Proxy hostname: " proxyHostname
        read -rp  "Proxy port: "     proxyPort
        read -rp  "Username: "       proxyUser
        read -rsp "Password: "       proxyPass; echo
        local url="http://$proxyUser:$proxyPass@$proxyHostname:$proxyPort"
        export http_proxy="$url" https_proxy="$url" ftp_proxy="$url"
        export HTTP_PROXY="$url" HTTPS_PROXY="$url" FTP_PROXY="$url"
        log "Proxy configured"
    else
        log "Installing without proxy"
    fi
}

#-----------------------------------------------------------------------------
# Dry-run preview
#-----------------------------------------------------------------------------
print_plan() {
    local nghdl kicadlib sky130
    nghdl=$( [ -d "$eSim_Home/nghdl" ] && echo "nghdl/ dir" \
             || { [ -f "$eSim_Home/nghdl.zip" ] && echo "nghdl.zip" || echo "MISSING"; } )
    kicadlib=$( [ -d "$eSim_Home/library/kicadLibrary" ] && echo "dir" \
             || { [ -f "$eSim_Home/library/kicadLibrary.tar.xz" ] && echo "tarball" || echo "MISSING"; } )
    sky130=$( [ -f "$eSim_Home/library/sky130_fd_pr.tar.xz" ] && echo "present" || echo "MISSING" )

    ui_banner "v$ESIM_VERSION" "install plan $G_DOT dry run, nothing is changed"
    ui_box "${C_ACCENT:-}" "${G_ARROW:->}" "What --install would do" \
        "eSim root"  "$eSim_Home" \
        "Profile"    "$PROFILE_SUMMARY${KICAD_PPA:+ [ppa:$KICAD_PPA]}" \
        "Qt"         "$QT_PKGS $QSCI_PKG" \
        "Virtualenv" "$config_dir/env (--system-site-packages)" \
        "nghdl"      "$nghdl" \
        "kicadLib"   "$kicadlib" \
        "sky130 PDK" "$sky130" \
        "AI Assistant" "optional prompt: Ollama + ${CHATBOT_MODELS[*]}" \
        "Symbols"    "14 static -> /usr/share/kicad/symbols (root)" \
        ""           "3 generated -> $config_dir/kicad_symbols (user)" \
        "Log"        "$HOME/eSim-install.log"

    local i=0 s
    printf '  %sSteps%s\n' "${C_BOLD:-}" "${C_RESET:-}"
    for s in "${INSTALL_STEPS[@]}"; do
        i=$((i + 1))
        printf '    %s%02d%s %s\n' "${C_DIM:-}" "$i" "${C_RESET:-}" "${s#*:}"
    done
    echo
    return 0
}

#=============================================================================
# Main
#=============================================================================
if [ "$#" -ne 1 ]; then
    echo "USAGE:"
    echo "  ./install-eSim.sh --install"
    echo "  ./install-eSim.sh --uninstall"
    echo "  ./install-eSim.sh --dry-run"
    exit 1
fi
option="$1"

ui_detect
ui_palette
resolve_esim_home
ESIM_VERSION=$(cat "$eSim_Home/VERSION" 2>/dev/null) || ESIM_VERSION="?"
detect_profile

case "$option" in
    --dry-run)
        print_plan
        ;;

    --install)
        # Tee everything to a log so a failed install is fully diagnosable
        # (handy when iterating on fresh VMs).
        #
        # The nested sed strips ANSI on the way to DISK ONLY: the terminal
        # still gets colour, while eSim-install.log stays plain text a user
        # can paste into a bug report. Without it, every colour code in this
        # script would end up in the log as literal ^[[38;5;117m noise.
        # Two expressions: CSI sequences (colour, cursor, erase) and the
        # two-character forms (ESC 7 / ESC 8 save+restore). The latter are
        # only ever written to /dev/tty today; stripping them anyway means a
        # future change cannot quietly start seasoning the log with them.
        exec > >(tee >(sed -u 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\x1B[()#][A-Za-z0-9]//g; s/\x1B[78=>]//g; s/\r$//' \
                        > "$HOME/eSim-install.log")) 2>&1
        set -e; set -E; trap error_exit ERR

        # Ubuntu 24.04+ ships needrestart, whose apt hook opens a whiptail
        # dialog ("Which services should be restarted?") part-way through an
        # install and then BLOCKS on a keypress -- so an unattended install
        # silently stalls, looking hung, for as long as nobody is watching.
        #
        # Mode 'l' (list) suppresses the prompt and restarts NOTHING; it only
        # prints what would need a restart. Deliberately not 'a' (automatic):
        # restarting a user's running services without asking is not a
        # decision an EDA installer gets to make. Respect an existing value so
        # anyone who has already chosen a policy keeps it.
        export NEEDRESTART_MODE="${NEEDRESTART_MODE:-l}"

        ui_begin
        ui_plan "${#INSTALL_STEPS[@]}"
        ui_banner "v$ESIM_VERSION" "$PROFILE_SUMMARY"
        log "Logging to $HOME/eSim-install.log"

        # Pre-flight runs OUTSIDE the numbered steps: both of these talk to
        # the user, and neither installs anything.
        preflightDisk
        setupProxy

        for _entry in "${INSTALL_STEPS[@]}"; do
            ui_step "${_entry#*:}"
            "${_entry%%:*}"
        done
        ui_step_close

        ui_end
        ui_box "${C_OK:-}" "${G_OK:-ok}" "eSim $ESIM_VERSION installed successfully" \
            "Launch"   "esim   (or the desktop icon)" \
            "Location" "$eSim_Home" \
            "Config"   "$config_dir/$config_file" \
            "Log"      "$HOME/eSim-install.log" \
            "Took"     "$(ui_hms $((SECONDS - UI_T0)))"
        ;;

    --uninstall)
        ui_banner "v$ESIM_VERSION" "uninstall $G_DOT $PROFILE_SUMMARY"
        read -rp "This removes eSim, KiCad, NGHDL, SKY130 PDK and their models. Continue? (y/n): " c
        if [[ "$c" =~ ^[Yy] ]]; then
            uninstall_eSim
            ui_box "${C_OK:-}" "${G_OK:-ok}" "eSim removed" \
                "Kept" "your projects and any hand-edited files outside ~/.esim"
        else
            log "Uninstall cancelled."
        fi
        ;;

    *)
        echo "Invalid argument: $option"
        echo "Usage: $0 --install | --uninstall | --dry-run"
        exit 1
        ;;
esac
