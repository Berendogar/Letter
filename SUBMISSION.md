# Letter — Case Study 9

**Student:** Beren Dogar
**Repository:** https://github.com/Berendogar/Letter
**Hosted URL:** https://letter-beren-dogar.onrender.com

## Architecture

```text
Browser --POST /--> app.py --> home.html

Before: note pasted into a Jinja string, rendered, shown with |safe
After:  note passed as a value, shown with {{ result.note }} (escaped)
```

Nothing is stored. There is no database. The two recent notes are the `EXAMPLES` list in `app.py`. A note you set exists only on the page that comes back.

The card has three fields: recipient, sender, and note. Example notes were always escaped. A note you set was not: `app.py` put it into a layout string, ran that string as a Jinja template, and `home.html` showed the result with `|safe`.

## Bug

Server-side template injection (SSTI), plus HTML injection from `|safe`. To trigger it, set a card with one of these notes:

| Note | Card showed |
| --- | --- |
| `{{ 7*7 }}` | `49` |
| `{{ config }}` | the Flask config, including `SECRET_KEY` and `DESK_CODE` |
| `{{ cycler.__init__.__globals__.os.popen('uname -s').read() }}` | `Linux`, so a command ran on the server |
| `<b>thanks</b>` | bold text |

Impact: critical. Anyone, without logging in, can read the app's secrets and run commands on the server.

The hosted app is patched. To reproduce, run the starter commit locally: `git checkout 80f7e12`, `pip install -r requirements.txt`, `python app.py`.

## Patch

The note is no longer run as a template. The card uses the same escaped markup as the example notes, so every field shows as plain text. Normal notes and line breaks still work.

`pytest -q`: 5 passed.
