# Skill: Release Process

Proceso completo para publicar una nueva version de normativa.

## Prerequisitos

- uv instalado
- Acceso a PyPI (token en ~/.pypirc o TWINE_PASSWORD)
- gh CLI autenticado
- Working tree limpio (`git status` sin cambios)

## Comandos paso a paso

### 1. Verificar estado

```bash
cd $(git rev-parse --show-toplevel)
uv run pytest -v
git status
```

### 2. Determinar nueva version

- Consultar version actual: `grep __version__ src/normativa/__init__.py`
- Consultar version en pyproject: `grep "^version" pyproject.toml`
- Decidir bump segun SemVer (patch/minor/major)

### 3. Actualizar version

Editar `src/normativa/__init__.py`:
```python
__version__ = "X.Y.Z"
```

Editar `pyproject.toml`:
```toml
version = "X.Y.Z"
```

### 4. Actualizar CHANGELOG.md

Formato Keep a Changelog. Secciones: Added, Changed, Fixed, Removed.

```bash
# Ver commits desde ultimo tag
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

### 5. Commit, tag, build, publish

```bash
git add src/normativa/__init__.py pyproject.toml CHANGELOG.md
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
uv build
ls -la dist/
uv publish
git push && git push --tags
gh release create vX.Y.Z --generate-notes --title "normativa vX.Y.Z"
```

### 6. Verificar

```bash
pip install normativa==X.Y.Z --dry-run
gh release view vX.Y.Z
```

## Checklist

- [ ] Tests pasan (uv run pytest)
- [ ] Version coincide en __init__.py y pyproject.toml
- [ ] CHANGELOG.md actualizado
- [ ] Commit "release: vX.Y.Z"
- [ ] Tag vX.Y.Z creado
- [ ] Build ok (dist/ tiene .whl y .tar.gz)
- [ ] Publicado en PyPI
- [ ] Tags pushed
- [ ] GitHub release creado

## Rollback

Si algo falla despues del publish:

```bash
# Borrar tag local y remoto
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z

# Revert commit
git revert HEAD
git push
```

PyPI no permite re-publish de la misma version. Si falla: bump a X.Y.Z+1.
