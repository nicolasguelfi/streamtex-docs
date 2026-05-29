# Créer un projet StreamTeX en mode développeur (avec pack) — séquence robuste

Cette séquence est **idempotente** : tu peux la relancer en entier sans casse,
même si les repos sont sales, si `stx` est périmé, ou si une exécution
précédente a échoué en cours de route.

## 0. Prérequis (une fois)

```bash
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
# Assure-toi que ~/.local/bin est dans le PATH (binaire stx)
case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) export PATH="$HOME/.local/bin:$PATH";; esac
```

## 1. Variables (adapte le chemin racine)

```bash
export STX_DEV_ROOT="/chemin/vers/streamtex-dev"
WS="$HOME/streamtex-workspaces/demo-ws"   # où créer le workspace
PROJ="demo"                                # nom du projet
```

## 2. Rendre le binaire `stx` à jour (pointe sur ta source dev, éditable)

```bash
uv tool install --editable --reinstall --with "streamtex[cli]" "$STX_DEV_ROOT/streamtex"
stx --version   # sanity check — doit afficher ta version dev
```

> Couvre le cas **« stx pas à jour »** : `--reinstall` reconstruit le binaire
> depuis ta source locale. À relancer après chaque `git pull` dans `streamtex/`.

## 3. Enregistrer les sources dev (idempotent, n'exige PAS des repos propres)

```bash
stx dev register streamtex        "$STX_DEV_ROOT/streamtex"
stx dev register streamtex-claude "$STX_DEV_ROOT/streamtex-claude"
stx dev register streamtex-docs   "$STX_DEV_ROOT/streamtex-docs"
stx dev status
```

> `register` n'enregistre qu'un **chemin** (dans `~/.config/streamtex/dev.json`)
> — il ne lit ni ne modifie l'état git des repos. Couvre **« repos pas
> propres »** : peu importe qu'ils aient des modifs non commitées.

## 4. Créer le workspace + projet en **preset developer** + **--dev**

```bash
mkdir -p "$WS" && cd "$WS"
stx install --preset developer --project "$PROJ" --template project --dev
```

> - `--preset developer` : les repos dev déjà enregistrés (étape 3) sont
>   **réutilisés, jamais re-clonés par-dessus**.
> - `--dev` : lie `streamtex` (source locale éditable) dans le `pyproject.toml`
>   du projet → le venv projet ET le `stx` global pointent sur la **même**
>   source ⇒ pas d'avertissement de divergence.
> - Le projet reçoit `stx.toml` + `mypack` (pack local primaire) — prêt pour la
>   reuse architecture.

## 5. Entrer dans le projet

```bash
cd "projects/$PROJ"
```

## 6. Ajouter un pack — deux variantes

**A. Mode dev complet (pack local éditable — recommandé si tu as
`streamtex-packs`)** :

```bash
uv run stx pack add --dev "local:$STX_DEV_ROOT/streamtex-packs/streamtex-pack-design"
uv run stx pack sync && uv sync
```

→ Les modifs du pack sont visibles immédiatement (lien éditable).

**B. Pack publié depuis le monorepo git** :

```bash
uv run stx pack add "git:https://github.com/nicolasguelfi/streamtex-packs#subdirectory=streamtex-pack-design"
uv run stx pack sync && uv sync
```

## 7. (Option) Installer un kit

```bash
uv run stx kit install streamtex-pack-design:project-default
uv sync
```

## 8. Vérifier — toujours via `uv run stx` (introspection du venv projet)

```bash
uv run stx pack list
uv run stx component list
uv run stx validate
```

## 9. Lancer

```bash
stx run
```

---

## « Fonctionne dans tous les cas » — points de robustesse

| Situation | Pourquoi ça passe / quoi faire |
|-----------|-------------------------------|
| **stx périmé** | Étape 2 (`--reinstall`) le reconstruit depuis la source dev. |
| **Repos dev sales / divergés** | Étapes 3-4 utilisent `dev register`/`--dev` (chemins + édition du projet), **jamais** `stx update --locked` qui, lui, échoue sur un repo divergé. On ne touche pas à l'état git des sources. |
| **Avertissement de divergence** | N'apparaît pas ici (preset developer + `--dev` alignent les deux venvs). Si jamais : `uv run stx …` ou `stx dev link streamtex`. |
| **Install interrompue puis relancée** | `stx install` a une machine à états reprenable (`.stx-install.json`). Pour repartir de zéro : `rm "$WS/.stx-install.json"`. |
| **Le projet existe déjà** | `stx install --project` affiche « already exists — skipping ». Choisis un autre `PROJ`, ou supprime `projects/$PROJ`. |
| **`stx` introuvable après l'étape 2** | `~/.local/bin` pas dans le PATH → étape 0. |
| **Introspection montre « No components »** | Tu as utilisé le `stx` global au lieu de `uv run stx` → relance avec `uv run stx`. |

---

Voir aussi `cheatsheets/stx-cheatsheet.sh` pour les fonctions shell
(`stx-dev-setup`, `stx-new-dev`, `stx-pack-add`, …) qui automatisent ces étapes.
