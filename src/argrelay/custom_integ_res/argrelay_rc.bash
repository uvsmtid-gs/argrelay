#!/usr/bin/env bash
# `argrelay` integration file: https://github.com/argrelay/argrelay

# This script is source-able by `~/.bashrc`:
#     source path/to/argrelay_dir/exe/argrelay_rc.bash

# The main purposes of this script:
# *   enable auto-completion for the commands
# *   add commands to PATH

# Normally, this script is a symlink to orig artifact from `argrelay` distrib package.
# The path where this symlink (or copy) is located is supposed to contain:
# *   `@/bin/run_argrelay_client` artifact (generated by `@/exe/bootstrap_dev_env.bash`)
# *   `@/conf/argrelay_rc_conf.bash` defining `argrelay_bind_command_basenames` env var
# When it is sourced, it re-creates symlinks for all command names listed in `@/conf/argrelay_rc_conf.bash`
# (in `argrelay_bind_command_basenames` env var) into `@/bin/run_argrelay_client`.
# Then `argrelay` auto-completion is enabled for all of them.
# When sourced in `~/.bashrc`, this config becomes available in any new Bash instance.

# Note that enabling exit on error (like `set -e` below) will exit parent Bash shell (as this one is sourced).
# Use these options with care as it prevents starting any shell in case of errors.

# Debug: Print commands before execution:
#set -x
# Debug: Print commands after reading from a script:
#set -v
# Return non-zero exit code from commands within a pipeline:
#set -o pipefail
# Exit on non-zero exit code from a command:
#set -e
# Inherit trap on ERR by sub-shells:
#set -E
# Error on undefined variables:
#set -u

# It is expected that `@/exe/argrelay_rc.bash` is sourced from the project dir.
# The dir of this script:
script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# FS_29_54_67_86 dir_structure: `@/exe/` -> `@/`:
argrelay_dir="$( dirname "${script_dir}" )"

# Test files generated by `@/exe/bootstrap_dev_env.bash` script:
test -f "${argrelay_dir}/bin/run_argrelay_server" || return 1
test -f "${argrelay_dir}/bin/run_argrelay_client" || return 1
test -f "${argrelay_dir}/conf/argrelay_rc_conf.bash" || return 1

# Load user config for env vars:
# *   argrelay_bind_command_basenames
source "${argrelay_dir}/conf/argrelay_rc_conf.bash"

# shellcheck disable=SC2154
if [[ "${#argrelay_bind_command_basenames[@]}" -lt 1 ]]
then
    # At least one command should be listed in `argrelay_bind_command_basenames`:
    return 1
fi

# Any (the first) command:
export ARGRELAY_CLIENT_COMMAND="${argrelay_bind_command_basenames[0]}"

for argrelay_command_basename in "${argrelay_bind_command_basenames[@]}"
do
    # Command line auto-completion process is largely similar to parsing command line args.
    # The difference is only in last step - either/or:
    # (A) an action is run             (based on provided parsed arg values)
    # (B) arg values are suggested     (based on provided parsed arg values)
    # Therefore, the same `@/bin/run_argrelay_client` can run both processes:
    # (A) as target command of `${argrelay_command_basename}` symlink
    # (B) as `-C` argument to Bash `complete` to configure auto-completion for `${argrelay_command_basename}`
    #
    # Enable auto-completion for `${argrelay_command_basename}` command:
    if [[ "${BASH_VERSION}" == 5* ]]
    then
        complete -o nosort -C run_argrelay_client "${argrelay_command_basename}"
    else
        # Old Bash versions do not support `nosort` option:
        complete           -C run_argrelay_client "${argrelay_command_basename}"
    fi
done

# Invoke completion programmatically:
function invoke_completion {
    # This function can be turned into generic one to invoke any
    # registered completion in Bash, but it is not straightforward, see:
    # https://brbsix.github.io/2015/11/29/accessing-tab-completion-programmatically-in-bash/
    # Instead, at least, invoke the same completion command starting `@/bin/run_argrelay_client`.
    # In other words, it always invokes `argrelay` regardless
    # whether `COMP_LINE` contains `argrelay`-configured command or completely irrelevant (like `ls`).
    # Invoke in a sub-shell to avoid setting env vars in the current shell:
    (
        export COMP_LINE="${READLINE_LINE}"
        export COMP_POINT="${READLINE_POINT}"
        # CompType.DescribeArgs = ASCII '@':
        export COMP_TYPE="94"
        # NOTE: Not useful: for any key sequence, it is only set to the last key (no use case at the moment).
        export COMP_KEY="88"

        run_argrelay_client
    )
    # Save command into history at least commented out (prefixed with `#`) to indicate it was not executed:
    # https://superuser.com/a/135654/176657
    # It is often convenient to recall what command lines used in previous queries - if not stored,
    # queries are not stored in the history (unless the command was also subsequently invoked).
    history -s "# ${READLINE_LINE}"
}

# Bind Alt+Shift+Q to `invoke_completion` function.
bind -x '"\eQ":"invoke_completion"'
# See limitation of `bind -x` (which might only be a limitation of older Bash versions):
# https://stackoverflow.com/a/4201274/441652

# Add dir with `${argrelay_bind_command_basenames}` into PATH to make them available in Bash as plain `basename`:
PATH="${argrelay_dir}/bin/:${PATH}"
export PATH

# TODO: Figure out how to push these settings on start and pop on exit (instead of override and then override again forgetting what they were initially).
# Disable exit on errors and any extra debug info for interactive shell
# (see enabling them for the duration of this script above):
#set +u
#set +E
#set +e
#set +o pipefail
#set +v
#set +x
