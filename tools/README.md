# Tools

- `make_manifest.py` — regenerate `tests/url_manifest.txt`; see `make manifest`.
- `strip_image_metadata.py` — report and remove image metadata, as below.

## Stripping image metadata

Camera images carry EXIF metadata including GPS coordinates, device models,
lens and serial numbers and capture timestamps. Some PNGs embed XMP packets or
draw.io diagram source. At the time of writing 237 of the 262 published images
carried metadata and 133 carried GPS coordinates resolving to a few metres.

The tool reads its list of images from the built site, so build first:

```bash
make html PY=venv/bin/python
venv/bin/python tools/strip_image_metadata.py scan
```

`scan` only reports, and takes a few seconds: it samples the head of each JPEG
rather than fetching whole files. `clean` writes stripped copies into
`cleaned/`, mirroring the paths in the object store, and needs to download
every image in full.

```bash
venv/bin/python tools/strip_image_metadata.py clean
```

Use `venv/bin/python`: the system interpreter has neither Pillow nor the rest
of the site's dependencies. Pass asset paths to work on a few images without
building the site, `-d` to write elsewhere and `-o` for a build outside
`output/`:

```bash
venv/bin/python tools/strip_image_metadata.py scan allotment-shed/back.jpg
venv/bin/python tools/strip_image_metadata.py clean -d /tmp/cleaned
```

The exit status is 1 if any image could not be processed, with the failures on
stderr. `cleaned/` is then incomplete, so re-run before uploading.

### What is kept

Stripping is lossless: JPEGs are filtered at the segment level and the
entropy-coded data is copied verbatim, so images are never re-encoded. A
cleaned image is checked to differ from its original only in metadata before it
is written. Deliberately preserved:

- **Orientation**, re-inserted as the only EXIF tag when an image relies on it.
  27 images display sideways without it.
- **Colour**: the JFIF header, the ICC profile and Adobe's colour transform.
- **Thermal data**: the `APP1 FLIR` radiometric payload of the
  `house-insulation/TI-*.jpg` images. It records the camera serial number and
  the capture date, but no location.

### Uploading

The tool itself never authenticates — it reads the object store over public
HTTPS. Credentials are only needed to upload, which `s3cmd` does:

```bash
venv/bin/pip install s3cmd
venv/bin/s3cmd --configure
```

Answer `ams3.digitaloceanspaces.com` for the endpoint and
`%(bucket)s.ams3.digitaloceanspaces.com` for the bucket template, using a
Spaces access key pair — generated under API → Spaces Keys, not a
DigitalOcean API token. That writes `~/.s3cfg`, which belongs in the home
directory and not in this repository.

Back up the bucket before overwriting anything:

```bash
venv/bin/s3cmd sync --preserve --progress s3://jwh/ ~/spaces-backup/
venv/bin/s3cmd ls -r s3://jwh/ | wc -l
find ~/spaces-backup -type f | wc -l
```

Keep the backup local. Copying within the bucket would leave a second public
copy of the originals on the same host.

```bash
venv/bin/s3cmd sync cleaned/ s3://jwh/homepage/ --acl-public
```

Check `--acl-public` matches how the existing objects are set, or the images
will 403 once overwritten. `sync` carries object contents but not ACLs or
content types, so a restore needs the same flag:

```bash
venv/bin/s3cmd sync --preserve ~/spaces-backup/homepage/ s3://jwh/homepage/ --acl-public
```

Re-run `scan` afterwards to confirm it reports no metadata.

### Limitations

- Anonymous bucket listing is denied, so the tool only sees images the built
  site references. With credentials, `s3cmd ls -r s3://jwh/homepage/` lists
  everything; pass any unreferenced objects in as arguments.
- A local copy under `content/` is read in preference to the remote one, so
  with images in `content/images/` a scan reports those rather than what is in
  the object store.
- PDFs are left alone. They carry only `TeX`, `Word` and `Quartz` producer
  strings.
