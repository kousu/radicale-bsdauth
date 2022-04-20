# Contributing

## Building


```
pip install build
python -m build
```

will produce `dist/radical-bsdauth*.tar.gz` as the _sdist_ and `dist/radicale_bsdauth*.whl` as the binary distribution.


You can test the resulting build by installing and running a local copy of radicale:

```
pip install --user radicale>=3
pip install dist/radicale_bsdauth-X.Y.Zrc0*.whl
mkdir -p ~/.config/radicale   # roughly, adapt this to your needs
( echo '[auth]'; echo 'type = radical_bsdauth' ) > ~/.config/radicale/config
~/.local/bin/radicale -D
```

## Directly from the Serpent's Mouth

You can also test a new version directly off github installed directly to your live server with

```
doas pip install git+https://github.com/kousu/radicale_bsdauth@v1.0.0rc2 # pick your favourite tag / commit ID here
doas rcctl resetart radicale
```


## Publishing

To publish a new version, go to https://github.com/kousu/radicale-bsdauth/releases/new and fill in a new tag `vX.Y.Zrc0` and click Publish.
It will automatically be built and published (via [.github/workflows/publish.yml](.github/workflows/publish.yml)) to https://github.com/kousu/radicale-bsdauth/releases and https://pypi.org/project/radicale-bsdauth/.

You should make sure to tag it with the 'rc' (release candidate) part initially,
to make sure not to disrupt any users. Before fully publishingly, you can test the built version with

```
pip install --upgrade --pre radicale-bsdauth
```

As you find and squash the final bugs, you can create a series of Releases tagged with 'rc1', 'rc2', etc
and test each in turn.

When you have a version that works, re-submit it (without making any more commits!) as `vX.Y.Z`; at that point,
people running `pip install --upgrade radicale-bsdauth` will get the new version.


You do not necessarily need to _create_ a tag through the Releases page: you can use `git tag` locally
to manage your tags, and then `git push --tags` to upload them to Github, and then pick them out from the
liist on the New Release page.


### Debugging

If you need to debug the release process, you can emulate it locally with

```
git tag vX.Y.Zrc0
python -m build
```
