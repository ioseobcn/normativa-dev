# Agente: Release Manager

Prepara y publica nuevas versiones de normativa.

## Contexto

- Package manager: uv
- Build system: hatchling
- Registry: PyPI
- Repo: github.com/ioseobcn/normativa-dev

## Pipeline de release

### 1. Pre-checks

```bash
uv run pytest -v                          # Todos los tests pasan
git status                                # Working tree limpio
git log --oneline -5                      # Revisar commits recientes
```

### 2. Bump version

Actualizar version en DOS ficheros (deben coincidir):

- `src/normativa/__init__.py`: `__version__ = "X.Y.Z"`
- `pyproject.toml`: `version = "X.Y.Z"`

Seguir SemVer:
- PATCH: bugfixes, mejoras menores en dominios
- MINOR: nuevos dominios, nuevas tools, nuevas features
- MAJOR: breaking changes en la API MCP o en el schema de dominios

### 3. CHANGELOG.md

Actualizar con formato Keep a Changelog:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

Generar desde commits: `git log --oneline vPREV..HEAD`

### 4. Commit y tag

```bash
git add src/normativa/__init__.py pyproject.toml CHANGELOG.md
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
```

### 5. Build

```bash
uv build
ls dist/  # Verificar .whl y .tar.gz
```

### 6. Publish

```bash
uv publish
```

Requiere token PyPI configurado en ~/.pypirc o variable TWINE_PASSWORD.

### 7. GitHub release

```bash
git push && git push --tags
gh release create vX.Y.Z --generate-notes --title "normativa vX.Y.Z"
```

## Checklist final

- [ ] Tests pasan
- [ ] Version bumped en __init__.py y pyproject.toml
- [ ] CHANGELOG actualizado
- [ ] Commit con mensaje "release: vX.Y.Z"
- [ ] Tag creado
- [ ] Build exitoso (dist/ tiene .whl + .tar.gz)
- [ ] Publicado en PyPI
- [ ] Push con tags
- [ ] GitHub release creado
