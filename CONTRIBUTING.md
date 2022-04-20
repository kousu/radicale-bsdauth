# Contributing

## Building


```
pip install build
python -m build
```

will produce `dist/radical_bsdauth*.tar.gz` as the _sdist_ and `dist/radicale_bsdauth*.whl` as the binary distribution.


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


### Publishing

(this is mostly a note to self)

To publish a new version, use

```
git tag vX.Y.Zrc0
python -m build
```

The 'rc' part makes sure it won't accidentally be used before it's ready: you *cannot replace files on https://pypi.org* so be careful with your tagging.


When you are happy with it, do a final real tag:

```
git tag vX.Y.Zrc0
git push --tags
```


( TODO:  upload to pypi )
