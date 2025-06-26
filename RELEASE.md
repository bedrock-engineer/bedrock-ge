# Releasing a new version of `bedrock-ge`

## 1. Update the Version Number

Follow [Semantic Versioning](https://semver.org/) (e.g., `1.0.0`, `1.1.0`, `1.1.1`):

- **Major** version: For incompatible API changes.
- **Minor** version: For new features that are backward-compatible.
- **Patch** version: For backward-compatible bug fixes.

Update the version number in:

- [`pyproject.toml`](pyproject.toml)
- [`/src/bedrock/__init__.py`](/src/bedrock_ge/__init__.py)
- Inline script dependencies of marimo notebooks in [`examples`](/examples/)

## 2. Update `uv.lock`

The version of `bedrock-ge` in the `uv.lock` file needs to be updated such that tests can run properly. Therefore run:

```bash
uv sync --all-groups --upgrade
```

## 3. PR `dev` → `main`

Open a pull request (PR) from `dev` to `main`.

This also runs the automated tests.

## 4. Commit the Changes

Commit the files that contain the updated version number and `CHANGELOG.md`:

```bash
git add .
git commit -m "Release version X.Y.Z"
```

## 5. Merge `dev` into `main`

Once everything is ready, and the PR is approved, merge `dev` into `main`. This officially brings all the changes in `dev` into the release-ready `main` branch.

## 6. Tag the Release

Create a Git tag for the new version:

```bash
git checkout main
git tag X.Y.Z
git push origin X.Y.Z
```

## 7. Build the Distribution

Create source and wheel distributions:

```bash
uv build
```

This creates a `bedrock_ge-X.Y.Z.tar.gz` file (source) and a `bedrock_ge-X.Y.Z-py3-none-any.whl` file (wheel) in the `/dist` folder.

## 8. Remove the old distribution

In order for the `uv publish` command to work properly, only one version of the distriution can be inside the `/dist` folder. Therefore delete the old source and wheel files.

## 9. Publish to PyPI

1. Set the `UV_PUBLISH_TOKEN` environment variable. Copy from `.env`.
2. Publish the new version to PyPI (Python Package Index):

```bash
set UV_PUBLISH_TOKEN=pypi-blablabla
uv publish
```

## 10. Verify the Release

Check that the new version is available on PyPI:  
<https://pypi.org/project/bedrock-ge/>

Install the new Python package version in a clean environment to verify it works:

```bash
uv run --with bedrock-ge --no-project -- python -c "import bedrock_ge; print(f'bedrock-ge version: {bedrock_ge.__version__}')"
```

## 11. Create a GitHub Release

Create a new release based on the tag: [github.com/bedrock-engineer/bedrock-ge/releases](https://github.com/bedrock-engineer/bedrock-ge/releases).
