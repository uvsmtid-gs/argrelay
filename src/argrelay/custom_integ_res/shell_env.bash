#!/usr/bin/env bash
# `argrelay` integration file: https://github.com/argrelay/argrelay
# It is configured via `@/conf/shell_env.conf.bash`.

# This script is source-able by `~/.bashrc`:
#     source path/to/argrelay_dir/exe/shell_env.bash

# The main purposes of this script:
# *   enable auto-completion for the commands configured via `argrelay_bind_command_basenames`
# *   add the commands to PATH

# Normally, this script is a symlink to orig artifact from `argrelay` distrib package.
# The path where this symlink (or copy) is located is supposed to contain:
# *   `@/exe/run_argrelay_client` artifact (generated by `@/exe/bootstrap_env.bash`)
# *   `@/conf/shell_env.conf.bash` defining `argrelay_bind_command_basenames` env var
# The symlinks for all command names are created by `@/exe/bootstrap_env.bash` and
# point to `@/exe/run_argrelay_client`.

# Note that enabling exit on error (like `set -e` below) will exit parent Bash shell (as this one is sourced).
# Use these options with care as it prevents starting any shell in case of errors.

# Define with `s` in value to debug:
if [[ "${ARGRELAY_DEBUG-}" == *s* ]]
then
    set -x
    set -v
fi

if [[ -n "${argrelay_rc_old_opts+x}" ]] ; then exit 1 ; fi

# Save `set`-able options to restore them at the end of this source-able script:
# https://unix.stackexchange.com/a/383581/23886
# See `@/exe/bootstrap_env.bash` regarding `history`:
argrelay_rc_old_opts="$( set +o | grep -v "[[:space:]]history$" )"
case "${-}" in
    *e*) argrelay_rc_old_opts="${argrelay_rc_old_opts}; set -e" ;;
      *) argrelay_rc_old_opts="${argrelay_rc_old_opts}; set +e" ;;
esac

# Debug: Print commands before execution:
#set -x
# Debug: Print commands after reading from a script:
#set -v
# Return non-zero exit code from commands within a pipeline:
set -o pipefail
# Exit on non-zero exit code from a command:
set -e
# Inherit trap on ERR by sub-shells:
set -E
# Error on undefined variables:
set -u

# TODO: This is a stop gap workaround (to allow FS_57_36_37_48 multiple clients coexistence):
#       Prefix all shared vars (e.g. `argrelay_dir`) set here with `argrelay_rc` and unset them on exit.
#       With multiple clients, sourcing the second `@/exe/shell_env.bash` reset shared env vars used by the first.
#       TODO_27_61_22_18: Long term solution is to make these vars local (not shared).
argrelay_rc_script_source="${BASH_SOURCE[0]}"
# It is expected that `@/exe/shell_env.bash` is sourced from the project dir.
# The dir of this script:
argrelay_rc_script_dir="$( cd -- "$( dirname -- "${argrelay_rc_script_source}" )" &> /dev/null && pwd )"
# FS_29_54_67_86 dir_structure: `@/exe/` -> `@/`:
argrelay_rc_argrelay_dir="$( dirname "${argrelay_rc_script_dir}" )"

# Test files generated by `@/exe/bootstrap_env.bash` script:
test -f "${argrelay_rc_argrelay_dir}/exe/run_argrelay_server" || return 1
test -f "${argrelay_rc_argrelay_dir}/exe/run_argrelay_client" || return 1
test -f "${argrelay_rc_argrelay_dir}/conf/shell_env.conf.bash" || return 1

# Load user config for env vars:
# *   argrelay_bind_command_basenames
source "${argrelay_rc_argrelay_dir}/conf/shell_env.conf.bash"

# shellcheck disable=SC2154
if [[ "${#argrelay_bind_command_basenames[@]}" -lt 1 ]]
then
    # At least one command should be listed in `argrelay_bind_command_basenames`:
    return 1
fi

# FS_57_36_37_48 multiple clients coexistence: this maps each symlink basename to its client path
# so that `Alt+Shift+Q` can use `argrelay_basename_to_client_path_map` to select correct client path:
declare -A argrelay_basename_to_client_path_map

# Any (the first) command:
export ARGRELAY_CLIENT_COMMAND="${argrelay_bind_command_basenames[0]}"

for argrelay_command_basename in "${argrelay_bind_command_basenames[@]}"
do
    # Command line auto-completion process is largely similar to parsing command line args.
    # The difference is only in last step - either/or:
    # (A) an action is run             (based on provided parsed arg values)
    # (B) arg values are suggested     (based on provided parsed arg values)
    # Therefore, the same `@/exe/run_argrelay_client` can run both processes:
    # (A) as target command of `${argrelay_command_basename}` symlink
    # (B) as `-C` argument to Bash `complete` to configure auto-completion for `${argrelay_command_basename}`
    #
    # Enable auto-completion for `${argrelay_command_basename}` command:
    if [[ "${BASH_VERSION}" == 5* ]]
    then
        complete -o nosort -C "${argrelay_rc_argrelay_dir}/exe/run_argrelay_client" "${argrelay_command_basename}"
    else
        # Old Bash versions do not support `nosort` option:
        complete           -C "${argrelay_rc_argrelay_dir}/exe/run_argrelay_client" "${argrelay_command_basename}"
    fi

    argrelay_basename_to_client_path_map["${argrelay_command_basename}"]="${argrelay_rc_argrelay_dir}/exe/run_argrelay_client"
done

# Invoke completion programmatically:
function invoke_completion {
    # This function can be turned into generic one to invoke any
    # registered completion in Bash, but it is not straightforward, see:
    # https://brbsix.github.io/2015/11/29/accessing-tab-completion-programmatically-in-bash/
    # Instead, at least, invoke the same completion command starting `@/exe/run_argrelay_client`.
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

        local argrelay_command_basename
        # Split into words (not expecting multi-word command names):
        # shellcheck disable=SC2206
        local command_components=( ${COMP_LINE} )
        local command_name="${command_components[0]}"
        argrelay_command_basename="$( basename "${command_name}" )"
        if [[ -n "${argrelay_basename_to_client_path_map["${argrelay_command_basename}"]+x}" ]]
        then
            # FS_57_36_37_48 multiple clients coexistence:
            # The symlink basename is found, use correct client path:
            "${argrelay_basename_to_client_path_map["${argrelay_command_basename}"]}"
        else
            local basename_color="\e[41m"
            local reset_color="\e[0m"
            echo -e "WARN: unknown \`argrelay\` client path for command: ${basename_color}${argrelay_command_basename}${reset_color}" 1>&2
        fi
    )
    # Save command into history at least commented out (prefixed with `#`) to indicate it was not executed:
    # https://superuser.com/a/135654/176657
    # It is often convenient to recall what command lines used in previous queries - if not stored,
    # queries are not stored in the history (unless the command was also subsequently invoked).
    # TODO_24_22_11_49: avoid removing last history command:
    #       The following command to append (commented out) command line to the history
    #       removes the last command in the history. Why?
    #       See output `history -p '!-1'` at this point - it is not equal the truly last command,
    #       it points to the command before the last, so the command replaces the truly last command in the history.
    history -s "# ${READLINE_LINE}"
}

# Bind Alt+Shift+Q to `invoke_completion` function.
bind -x '"\eQ":"invoke_completion"'
# See limitation of `bind -x` (which might only be a limitation of older Bash versions):
# https://stackoverflow.com/a/4201274/441652

# Add dir with `${argrelay_bind_command_basenames}` into PATH to make them available in Bash as plain `basename`:
PATH="${argrelay_rc_argrelay_dir}/bin/:${PATH}"
export PATH

eval "${argrelay_rc_old_opts}"
unset argrelay_rc_old_opts

unset argrelay_rc_script_source
unset argrelay_rc_script_dir
unset argrelay_rc_argrelay_dir
