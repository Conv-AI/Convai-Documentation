# Writing standards

Voice, tone, terminology, version tracking, deprecation, and examples. Product names come from the
subject. Synchronized values (versions, package URLs) are GitBook variables, never literals (CV-24):
how to write one is in `variables.md`.

## Voice and tone

- Write directly and concretely, in active voice and present tense, in American English.
- Second person for tasks: "Add your API key." In tutorials, collaborative first-person plural: "We
  will add the component", not "You will learn how to add": the tutorial is a shared activity, not a
  lesson.
- Short sentences, one claim per sentence.
- Explain a term at its first use, or link to its concept page.
- Format class names, methods, fields, enums, file paths, asset paths, package names, console
  messages, and literal values as `inline code` everywhere: prose, table cells, list items, and step
  bodies (CV-18).
- Write `##` headings the way a reader would phrase the question: `Configure the API key` answers
  "how do I set my API key?", where `API key setup` or `Common issues` answer nothing.
- Do not let "it" or "this" refer back across paragraphs: an assistant quoting one section cannot
  resolve them.

Refer to Convai's backend as "Convai": "streams audio to Convai", "Convai responds", "sent to Convai".
Never "Convai cloud", "cloud", "cloud AI", "cloud backend", "cloud pipeline", "cloud-powered",
"Convai's servers", or "Convai's cloud".

Avoid:

- Marketing language: "powerful", "seamless", "robust", "cutting-edge".
- Setup promises: "up and running in minutes", "just one API key".
- Filler: "In this guide, we will explore...".
- Hedging: "you may want to", "you could try".
- Dismissive words: "simply", "just", "easy".
- Vague labels: "Overview", "More information", "Miscellaneous", and "click here" links.

## Version tracking

Every SDK page states the SDK version it applies to with the version variable it is given, in its
prerequisites or a reference page's lead; a page you revise gains it if missing (CV-90). Given none,
state none. A version-dependent page sets `last_reviewed` to the version verified against (CV-35).

If the version given does not match the source files, stop and report the mismatch instead of guessing.

## Renamed names

When a release renames or removes a name, a live page uses only the new name, with no "formerly" or
"renamed from" hint. The old name appears only on a historical page (the subject's `historical_pages`:
release notes, the changelog, migration guides), whose entry states the old and the new name once.

## Doc comments and callers

What a doc comment says is written only as far as the code shows it at the commit used; where the two
disagree, the code wins (CV-53, CV-54). What a function's body does is shown by its code whether or not
its caller was found, so a name the code defines may be named with what its body shows. What triggers
it is stated only from code: a call site, a registration, or a message the code itself emits. A value
or trigger that only a comment gives is not written. No caller found is an open question for the owner
("no caller found for `<name>`"), never a sentence on the page: no page says a name is unused,
unreachable or never raised. A release unit says only what its diff shows, so it calls a name
"unchanged" only when the diff shows it.

## Deprecated content

A deprecated API, component, or workflow gets a `{% hint style="warning" %}` at the top of its page:
what is deprecated, what replaces it, and from which SDK version (CV-46). Point inbound links at the
replacement page. Keep the page for at least one major SDK version, then remove it.

```md
{% hint style="warning" %}
**Deprecated in SDK 4.0.** `ConvaiLegacyAudioManager` is replaced by `ConvaiAudioManager`. See [Configure audio](../guides/configure-audio.md).
{% endhint %}
```

## Examples

Every feature page includes examples unless it is purely conceptual or a short reference entry. Each
example has a scenario name, a one-sentence context, concrete setup (Inspector configuration or code),
and the expected runtime outcome. Order: a minimal working example, a common production-style example,
an optional advanced variation.

Primary domain: learning and training simulations, with scenarios such as industrial safety drills,
medical training, military simulation, corporate onboarding, and procedural assessment. Other domains
are allowed when they fit the feature better; describe broad applicability as "training simulations,
interactive experiences, and games". Write "in-scene", never "game-world".
