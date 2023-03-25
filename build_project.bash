########################################################################################################################
# `argrelay` integration file: https://github.com/uvsmtid/argrelay

# This is a custom build script *sourced* by `bootstrap_venv.bash`.
# Python `venv` is already activated before it is sourced.

# Normally, the build scripts like this for integration project should build it and test it.

# It is fine to run tox on every start of `dev_shell` because
# this `git_deployment` (FS_66_29_28_85) is only used by `argrelay` devs:
# Build and test:
python -m tox
########################################################################################################################