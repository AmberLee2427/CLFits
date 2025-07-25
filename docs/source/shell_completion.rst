Shell Completion
================

`clfits` uses `Typer` to provide shell completion support. This allows you to press the ``Tab`` key to autocomplete commands, options, and even file paths.

Installation
------------

To enable shell completion, you need to run a command that installs a small script into your shell's configuration file.

First, make sure `clfits` is installed. Then, run the appropriate command for your shell.

.. code-block:: bash

   # For bash, add this to ~/.bashrc or ~/.bash_profile
   eval "$(_CLFITS_COMPLETE=bash_source clfits)"

   # For zsh, add this to ~/.zshrc
   eval "$(_CLFITS_COMPLETE=zsh_source clfits)"

   # For fish, add this to ~/.config/fish/completions/clfits.fish
   eval "$(_CLFITS_COMPLETE=fish_source clfits)"

After adding the line, **restart your shell** for the changes to take effect.

Usage
-----

Once installed, you can start typing a `clfits` command and press ``Tab`` to see available completions.

.. code-block:: bash

   # Type 'clfits v' and press Tab
   $ clfits view <Tab>
   # It will suggest 'view'

   # Type 'clfits view my_image.fits --h' and press Tab
   $ clfits view my_image.fits --hdu <Tab>
   # It will complete to '--hdu' 