# Plus One — working rules for Claude

Read `HANDOFF.md` first: product, research, architecture, history, links and to-dos.

- Main work is `demo/demo2_tpl.html` (single-file vanilla JS). Edit the template, then `python3 demo/build.py` → `demo/dist/plusone-demo.html`.
- Style: black / white / grey only; Inter Tight headings, Inter body; titles centred (Chats title is the exception, left-aligned); 393×852 frame; minimal and premium; every element must be functional. English UI.
- Interactions: add `data-act="name"` to an element and a matching `else if(a==='name')` branch in the click dispatcher; state lives in the global `state` object, then call `render()`.
- Check pages with Playwright screenshots (`demo/tests/`) before publishing.
- Never put a Ticketmaster API key (or any key) in the repo or in a published page. Before publishing, `grep` the built file for keys.
- The owner writes in Chinese; reply in Chinese, keep UI copy in English.
