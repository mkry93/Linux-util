# Usage

```bash
./ytplay
```

Expected Inputs:

- A plain search query, for example `rain sounds`.
- A `quoted search query` followed by mpv options and an optional search count.
- A direct URL, for example `https://www.youtube.com/watch?v=...`.

## Examples

### Search by text
```bash
rain sounds
```

searches and plays the result in `mpv`.

### Search with mpv option and search count
```bash
"rain sounds" --no-video 2
```

searches YouTube using `ytsearch2`, and passes `--no-video` to `mpv`.

### Play a direct URL
```bash
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Input rules

- Text without `--` is treated as the search query.
- Arguments starting with `--` are passed to `mpv`.
- A standalone number sets the `ytsearch` count.
- Quoted text is used as a single search phrase.
- use quotes when having a number or `--` in the query 

## Requirements

- `bash`
- `yad`
- `mpv`
