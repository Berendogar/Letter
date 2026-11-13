# Letter — Case Study 9

**Student:** Beren Dogar
**Repository:** https://github.com/Berendogar/Letter

```text
Browser form POST /
        |
        v
Flask app.py
        |
        +-- EXAMPLES in app.py     two notes, drawn by home.html
        +-- the note you just set  was pasted into a Jinja string
```

Nothing is saved. There is no database. The two recent notes are the `EXAMPLES` list. A note you just typed exists only on the page that comes back.

The card is the recipient, your name, and the note. Example notes go through `{{ item.note }}`, so they are text. A note you just set did not. `app.py` replaced the word `NOTE` in a layout string with the raw note, compiled that string as a template, and `home.html` inserted the HTML with `|safe`.

## Bug

To Maya, from Devon, note:

```text
{{ config.DESK_CODE }}
```

The card showed `LETTER-8830`. That value is only in the Flask config. `{{ 7*7 }}` showed `49`. `<b>thanks</b>` was real markup, not the characters I typed.

## Patch

The new card uses the same markup as the example notes. Recipient, name, and note are all escaped. `{{ config.DESK_CODE }}` stays as the characters you typed. A normal thank-you note still shows on the card.

`pytest -q`: 5 passed.
