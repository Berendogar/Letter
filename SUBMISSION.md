# Letter — Case Study 9

**Student:** Beren Dogar
**Repository:** https://github.com/Berendogar/Letter
**Hosted URL:** https://letter-beren-dogar.onrender.com

## Architecture

```text
Before the patch                            After the patch

Browser form POST /                         Browser form POST /
        |                                           |
        v                                           v
app.py: LAYOUT.replace("NOTE", note)        app.py: result = {recipient, sender, note}
        |                                           |
        v                                           v
jinja_env.from_string(source).render()      home.html: {{ result.note }}  (autoescaped)
        |
        v
home.html: {{ result|safe }}

Both versions: EXAMPLES in app.py -> home.html: {{ item.note }}  (autoescaped)
```

Nothing is saved. There is no database. The two recent notes are the `EXAMPLES` list in `app.py`. A note you just typed exists only on the page that comes back.

The card is the recipient, your name, and the note. Example notes go through `{{ item.note }}`, so they are text. A note you just set did not. `app.py` replaced the word `NOTE` in a layout string with the raw note, compiled that string as a template, and `home.html` inserted the HTML with `|safe`. The note was code, not data.

## Bug: server-side template injection

This is Jinja2 server-side template injection (SSTI). Because the result was inserted with `|safe`, it was also HTML injection (XSS).

To trigger it, set a card to Maya, from Devon, with one of these notes:

| Note | Card showed |
| --- | --- |
| `{{ 7*7 }}` | `49` |
| `{{ config.DESK_CODE }}` | `LETTER-8830`, a value that is only in the Flask config |
| `{{ config }}` | the whole Flask config, including `SECRET_KEY` |
| `{{ cycler.__init__.__globals__.os.popen('uname -s').read() }}` | `Linux`: a shell command ran on the server |
| `<b>thanks</b>` | bold text, real markup instead of the characters I typed |

Impact: critical. Anyone who can open the page, with no login, can read every config value and secret and run commands on the server as the app user.

### Reproduce

The hosted app is patched. To see the bug, run the starter commit:

```bash
git checkout 80f7e12
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:3000 and send one of the notes above. `git checkout main` returns to the patch.

On the hosted URL, Render's edge answers some payloads, such as ones containing `__globals__`, with a 403 before they reach the app. That block is Render's, not the fix.

## Patch

The note is no longer compiled as a template. `app.py` passes recipient, name, and note to `home.html` as plain values, and the new card uses the same markup as the example notes, so Jinja escapes all three. The fix removes `from_string` and `|safe`; it does not try to filter braces or keywords.

`{{ config.DESK_CODE }}` stays as the characters you typed, and `<b>thanks</b>` shows as text. A normal thank-you note still shows on the card, and line breaks are kept.

`pytest -q`: 5 passed.

Hosted at https://letter-beren-dogar.onrender.com. The free instance sleeps when idle.
