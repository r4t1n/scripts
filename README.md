# scripts

## convert-casaos-apps-to-latest.py

Script to convert installed CasaOS apps' docker image version to "latest"

Be aware that using the "latest" tag may introduce some issues, as specified [in this issue](https://github.com/IceWhaleTech/CasaOS-AppStore/issues/167), so use this script at your own discretion

### Downloading

```
curl -sSL https://raw.githubusercontent.com/r4t1n/scripts/main/convert-casaos-apps-to-latest.py -o convert-casaos-apps-to-latest.py
```

or

```
wget -O convert-casaos-apps-to-latest.py https://raw.githubusercontent.com/r4t1n/scripts/main/convert-casaos-apps-to-latest.py
```

### Usage

```
usage: convert-casaos-apps-to-latest.py [-h] [--path PATH] [--restore]

Script to convert installed CasaOS apps' docker image version to "latest"

options:
  -h, --help   show this help message and exit
  --path PATH  Path to the CasaOS apps folder (default: /var/lib/casaos/apps)
  --restore    Restore the original docker image version
```

## generate-minecraft-whitelist.py

Script to generate a Minecraft whitelist.json from usernames

### Usage

The usernames should be stored in a text file with a single username per line, example:

```
test
testtest
testtesttest
testtesttesttest
```

```
usage: generate-minecraft-whitelist.py <filename>
```