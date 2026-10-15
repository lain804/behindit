# behindit

Find the account behind an Instagram or TikTok share link.

Requires Python 3.13+ and Git.

## Install

Choose either method to make `behindit` available from any directory.

### [pip](https://pip.pypa.io/en/stable/cli/pip_install/)

```sh
python -m pip install --user git+https://github.com/lain804/behindit.git
```

Ensure Python's user scripts directory is on your `PATH` (pip displays its location if needed).

### [uv](https://docs.astral.sh/uv/concepts/tools/)

```sh
uv tool install git+https://github.com/lain804/behindit.git
uv tool update-shell
```

Restart your terminal after updating `PATH`.

## Usage

```sh
behindit "<share-url>"
```
