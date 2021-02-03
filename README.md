<p align="center">
  <img src="/demo.jpg" width="80%"/>
</p>

## Brief

I like writing markdown. But many editors lack some features like HackMD alert areas.
So, I've written a little script which embeds alert areas into markdown files as inline html.

## How to use script

Write markdown with alert areas and save it to `in.md`. Then launch script:
```
python3 alert-styler.py in.md out.md
```

And voila!
See alert areas in `out.md`.

## Tested on

- Typora
- Hackmd
- Other editors which support embedding html

## Want to change styles?

All styles are stored as `dict` in script file. Change them as you want

## It's a dirty hack!

I know but I just wanted alert areas rendering in Typora
