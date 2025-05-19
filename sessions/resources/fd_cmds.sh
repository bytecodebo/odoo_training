#!/usr/bin/env sh

# Fuente https://github.com/sharkdp/fd
# Alternativa a find

#Ubuntu

apt install fd-find # run fdfind

# Link

ln -s $(which fdfind) ~/.local/bin/fd

# Debian
apt-get install fd-find

# Link

ln -s $(which fdfind) ~/.local/bin/fd

# eliminar y excluir archivos

fd -t f -p ./**/i18n/* -e po -E 'es.po' -E 'es_BO.po' -tf -X rm
fd -t d -p ./**/l10n -E 'l10n_bo' -E 'l10n_multilang' -tf -X rm -r
find . -type f -iname '*.png' -exec du -ch {} + | grep total$

fd -p ./**/models/* -e py -X du -ch {} | grep total$
fd -e zip -x unzip
fd -p ./**/description/* -X du -ch {} | grep total$
sudo fd -t f -p ./**/description/* -E 'icon.png' -E 'icon.svg' -tf -X rm
sudo fd -t d -p ./**/images/* -tf -X rm -r


> fd -H -E .git …

> fd -E /mnt/external-drive …

# Deleting files
# You can use fd to remove all files and directories that are matched by your search pattern. If you only want to remove files, you can use the --exec-batch/-X option to call rm. For example, to recursively remove all .DS_Store files, run:

> fd -H '^\.DS_Store$' -tf -X rm
# If you are unsure, always call fd without -X rm first. Alternatively, use rms "interactive" option:

> fd -H '^\.DS_Store$' -tf -X rm -i

Usage: fd [OPTIONS] [pattern] [path]...

Arguments:
  [pattern]  the search pattern (a regular expression, unless '--glob' is used; optional)
  [path]...  the root directories for the filesystem search (optional)

Options:
  -H, --hidden                     Search hidden files and directories
  -I, --no-ignore                  Do not respect .(git|fd)ignore files
  -s, --case-sensitive             Case-sensitive search (default: smart case)
  -i, --ignore-case                Case-insensitive search (default: smart case)
  -g, --glob                       Glob-based search (default: regular expression)
  -a, --absolute-path              Show absolute instead of relative paths
  -l, --list-details               Use a long listing format with file metadata
  -L, --follow                     Follow symbolic links
  -p, --full-path                  Search full abs. path (default: filename only)
  -d, --max-depth <depth>          Set maximum search depth (default: none)
  -E, --exclude <pattern>          Exclude entries that match the given glob pattern
  -t, --type <filetype>            Filter by type: file (f), directory (d/dir), symlink (l),
                                   executable (x), empty (e), socket (s), pipe (p), char-device
                                   (c), block-device (b)
  -e, --extension <ext>            Filter by file extension
  -S, --size <size>                Limit results based on the size of files
      --changed-within <date|dur>  Filter by file modification time (newer than)
      --changed-before <date|dur>  Filter by file modification time (older than)
  -o, --owner <user:group>         Filter by owning user and/or group
      --format <fmt>               Print results according to template
  -x, --exec <cmd>...              Execute a command for each search result
  -X, --exec-batch <cmd>...        Execute a command with all search results at once
  -c, --color <when>               When to use colors [default: auto] [possible values: auto,
                                   always, never]
      --hyperlink[=<when>]         Add hyperlinks to output paths [default: never] [possible
                                   values: auto, always, never]
  -h, --help                       Print help (see more with '--help')
  -V, --version                    Print version

> fd '^[A-Z][0-9]+$'

# https://docs.rs/regex/latest/regex/#syntax

