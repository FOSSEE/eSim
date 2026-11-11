#!/bin/bash
# Drives the REAL install-eSim.sh Main block -- its tee/sed logging pipeline,
# ui_begin, the INSTALL_STEPS loop, the sticky bar, the summary and failure
# boxes -- with the twelve install steps replaced by fast stubs. Everything
# under test is the shipped code path; only the work is faked.
set -u
SRC=${SRC:?path to install-eSim.sh}

# Redirect HOME for the whole suite: --install writes $HOME/eSim-install.log,
# and a test run must not clobber the diagnostic log of a real install sitting
# on the same machine. Everything the stubs touch stays under this temp dir.
SANDBOX=$(mktemp -d)
trap 'rm -rf "$SANDBOX"' EXIT
export HOME="$SANDBOX/home"
mkdir -p "$HOME"
ROOT=$HOME/esimtest
pass=0; fail=0
ok()  { pass=$((pass+1)); printf '  ok   %s\n' "$1"; }
bad() { fail=$((fail+1)); printf '  FAIL %s\n' "$1"; }

# Build a runnable copy whose step functions are stubs. They are injected just
# before Main, so they override the real definitions above them.
mkstub() {                      # mkstub <outfile> <failing-step|"">
    local out=$1 failstep=${2:-}
    python3 - "$SRC" "$out" "$failstep" <<'PY'
import sys
src, out, failstep = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding='utf-8').read()
steps = ["preflightDisk","setupProxy","cleanLegacyEsim","createConfigFile",
         "installDependency","installQt","installKicad","copyKicadLibrary",
         "installNghdl","installSky130Pdk","installIhpPdk","installChatbot",
         "createDesktopStartScript","runToolchainDoctor"]
body = ["\n# ---- injected test stubs ----"]
for f in steps:
    if f == failstep:
        body.append('%s() { log "starting %s"; false; }' % (f, f))
    elif f == "setupProxy":
        body.append('setupProxy() { log "Installing without proxy"; }')
    elif f == "createConfigFile":
        # Reports the needrestart policy the installer settled on, so the
        # suite can assert it without inspecting the source.
        body.append('createConfigFile() { log "Writing config"; '
                    'echo "NRM=[${NEEDRESTART_MODE:-unset}]"; }')
    elif f == "installDependency":
        body.append('installDependency() { log "Updating apt index"; '
                    'echo "Get:1 http://archive.ubuntu.com noble InRelease"; '
                    'echo "Reading package lists... Done"; sleep 1; }')
    elif f == "installQt":
        body.append('installQt() { log "Installing PyQt6 (apt)"; '
                    'warn "python3-pyqt6.qsci unavailable - editor disabled"; }')
    elif f == "installNghdl":
        body.append('installNghdl() { log "Building NGHDL"; '
                    'for i in 1 2 3; do echo "  CC ngspice_$i.o"; sleep 0.4; done; }')
    else:
        body.append('%s() { log "stub %s"; sleep 0.2; }' % (f, f))
open(out, 'w', encoding='utf-8', newline='\n').write(
    s.replace("#=============================================================================\n# Main",
              "\n".join(body) +
              "\n\n#=============================================================================\n# Main", 1))
PY
    chmod +x "$out"
}

rm -rf "$ROOT"; mkdir -p "$ROOT/src" "$ROOT/library" "$ROOT/Ubuntu" "$ROOT/nghdl"
echo 2.6 > "$ROOT/VERSION"
: > "$ROOT/nghdl/nghdl-simulator-source.tar.xz"
: > "$ROOT/library/sky130_fd_pr.tar.xz"

pty() { script -qec "stty rows 40 cols 96 </dev/tty; $1" /dev/null 2>/dev/null; }

echo "== A. happy path =="
mkstub "$ROOT/Ubuntu/install-eSim.sh" ""
rm -f "$HOME/eSim-install.log"
trace=$(pty "cd $ROOT && ./Ubuntu/install-eSim.sh --install"); rc=$?
printf '%s' "$trace" | tr -d '\r' | sed 's/\x1B\[[0-9;?]*[a-zA-Z]//g' | grep -vE '^\s*$' | tail -32
echo "  --- exit $rc ---"
[ "$rc" -eq 0 ] && ok "exit 0" || bad "exit $rc"
case "$trace" in *"installed successfully"*) ok "summary box printed" ;; *) bad "no summary box" ;; esac
case "$trace" in *$'\033[?25h'*) ok "cursor restored" ;; *) bad "CURSOR LEFT HIDDEN" ;; esac
case "$trace" in *"12/12"*) ok "bar reached 12/12" ;; *) bad "bar never reached 12/12" ;; esac

echo
echo "== B. the log file =="
if [ -s "$HOME/eSim-install.log" ]; then ok "log written"; else bad "log empty/missing"; fi
if grep -q $'\033' "$HOME/eSim-install.log"; then
    bad "log contains ANSI escapes"
    grep -c $'\033' "$HOME/eSim-install.log"
else
    ok "log is ANSI-free"
fi
for want in "Updating apt index" "Building NGHDL" "CC ngspice_3.o" "installed successfully"; do
    grep -q "$want" "$HOME/eSim-install.log" && ok "log kept: $want" || bad "log LOST: $want"
done
echo "  --- log tail ---"; tail -6 "$HOME/eSim-install.log" | sed 's/^/  | /'

echo
echo "== C. failure path (installKicad dies at step 5/12) =="
mkstub "$ROOT/Ubuntu/install-eSim.sh" "installKicad"
trace=$(pty "cd $ROOT && ./Ubuntu/install-eSim.sh --install"); rc=$?
printf '%s' "$trace" | tr -d '\r' | sed 's/\x1B\[[0-9;?]*[a-zA-Z]//g' | grep -vE '^\s*$' | tail -14
echo "  --- exit $rc ---"
[ "$rc" -ne 0 ] && ok "non-zero exit on failure" || bad "failure exited 0"
case "$trace" in *"Installation failed"*) ok "failure box printed" ;; *) bad "no failure box" ;; esac
case "$trace" in *"step 5/12"*) ok "failure box names the step" ;; *) bad "step not named" ;; esac
case "$trace" in *$'\033[?25h'*) ok "cursor restored after failure" ;; *) bad "CURSOR LEFT HIDDEN ON FAILURE" ;; esac
last=$(printf '%s' "$trace" | grep -oE $'\033\\[1;[0-9]+r' | tail -1 | grep -oE '[0-9]+;[0-9]+r')
[ "$last" = "1;40r" ] && ok "scroll region restored after failure" || bad "scroll region left at [$last]"

echo
echo "== D. ESIM_NO_FANCY=1 install is escape-free =="
mkstub "$ROOT/Ubuntu/install-eSim.sh" ""
trace=$(pty "cd $ROOT && ESIM_NO_FANCY=1 ./Ubuntu/install-eSim.sh --install"); rc=$?
[ "$rc" -eq 0 ] && ok "plain-mode exit 0" || bad "plain-mode exit $rc"
if printf '%s' "$trace" | grep -q $'\033'; then bad "plain mode emitted escapes"; else ok "plain mode emitted no escapes"; fi
case "$trace" in *">>> [5/12]"*) ok "plain mode keeps >>> step format" ;; *) bad "plain step format missing" ;; esac

echo
echo "== E. banner survives the sticky bar intact =="
# The bar and the installer's own output share one terminal. When a background
# ticker also painted the bar, its stale cursor-restore overwrote whole rows
# and the banner came out a line short. Assert the full box still renders
# under --install (bar armed), not just under --dry-run (bar idle).
mkstub "$ROOT/Ubuntu/install-eSim.sh" ""
trace=$(pty "cd $ROOT && ./Ubuntu/install-eSim.sh --install")
plain=$(printf '%s' "$trace" | tr -d '\r' | sed 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\x1B[78]//g')
rows=$(printf '%s\n' "$plain" | grep -c '^│')
# 5 wordmark rows + 2 padding rows + 1 title row = 8 lines starting with │
if [ "$rows" -ge 8 ]; then ok "banner rendered all $rows framed rows"
else bad "banner lost rows under the sticky bar (got $rows, want >= 8)"; fi
printf '%s\n' "$plain" | grep -q '▄████▄' \
    && ok "wordmark top row present" || bad "WORDMARK TOP ROW EATEN"
printf '%s\n' "$plain" | grep -q '▀█▄▄█▀' \
    && ok "wordmark bottom row present" || bad "wordmark bottom row eaten"

echo
echo "== F. needrestart policy =="
# Default 'l' = list only: suppresses the blocking whiptail prompt during apt
# without restarting anything. An explicit value from the user must survive.
trace=$(pty "cd $ROOT && ./Ubuntu/install-eSim.sh --install")
case "$trace" in *"NRM=[l]"*) ok "defaults to NEEDRESTART_MODE=l" ;;
                 *)           bad "did not default to l" ;; esac
trace=$(pty "cd $ROOT && NEEDRESTART_MODE=i ./Ubuntu/install-eSim.sh --install")
case "$trace" in *"NRM=[i]"*) ok "respects a user-set NEEDRESTART_MODE" ;;
                 *)           bad "clobbered a user-set NEEDRESTART_MODE" ;; esac
# 'a' would restart services unasked -- assert we never silently choose it.
case "$(grep -c 'NEEDRESTART_MODE=a' "$SRC")" in
    0) ok "never hard-codes the auto-restart mode" ;;
    *) bad "script sets NEEDRESTART_MODE=a somewhere" ;;
esac

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
