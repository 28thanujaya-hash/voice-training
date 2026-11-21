# How the user likes links shown

Applies to every reply in the Voice Training project (and is a good default everywhere).

## Rules

1. **Always give the direct link to the exact page,** never just a path like "Settings → API tokens".
   - Good: [Modal API tokens](https://modal.com/settings/tokens)
   - Bad: "Go to Settings / User settings → API token"
2. **Short, tappable, named links:** the link text says what the page is. No raw URLs in the text.
   - Good: [GitHub secrets for voice-training](https://github.com/28thanujaya-hash/voice-training/settings/secrets/actions/new)
   - Bad: https://github.com/28thanujaya-hash/voice-training/settings/secrets/actions/new
3. **Link to the deepest page that exists.** For adding a secret, link the "new secret" page itself, not the repo or the settings home.
4. **If no direct address exists** (the page is only reachable by clicking inside an app), link the app's page you can reach and then give the exact clicks in one short line.
   - Example: [Saturn Cloud app](https://app.community.saturnenterprise.io), then click your username → User Profile → Access Keys → New Token.
5. **Every page mentioned gets its link,** including claude.ai pages (artifacts) and GitHub runs or files when the user needs to open them.
6. **Don't repeat a link the app already shows** as a card (published artifacts, cited web results).
7. **Phone first:** one link per line when there are several; keep the surrounding text short.

## Frequently used links

- [GitHub secrets for voice-training (new)](https://github.com/28thanujaya-hash/voice-training/settings/secrets/actions/new)
- [voice-training repo](https://github.com/28thanujaya-hash/voice-training)
- [voice-training Actions runs](https://github.com/28thanujaya-hash/voice-training/actions)
- [Modal API tokens](https://modal.com/settings/tokens)
- [Groq API keys](https://console.groq.com/keys)
- [Kaggle: your notebooks](https://www.kaggle.com/code)
- [Google Colab](https://colab.research.google.com)
