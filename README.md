# Shine
Glossy, glassy theme based on [a twitter design.](https://x.com/zeealeid/status/1956781061116928462?)

![GitHub License](https://img.shields.io/github/license/blade04208/shine?style=flat-square)
 ![GitHub last commit](https://img.shields.io/github/last-commit/blade04208/shine?style=flat-square) ![Discord](https://img.shields.io/discord/1334998273437597767?style=flat-square&label=Discord) ![GitHub repo size](https://img.shields.io/github/repo-size/blade04208/shine?style=flat-square) ![Static Badge](https://img.shields.io/badge/skill-issue-red?style=flat-square)
 
![screenshot of shine](./src/thumb.png)|

Original design made by [@zeealeid](https://github.com/zeealeid)


## Installation

### Vencord

Download shine.theme.css and put it in your local themes.

If you have Vesktop, enable Native Discord Titlebar!

   
### BetterDiscord
download shine.theme.css and put it in your themes folder.

## Customization
The entire app can be recolored with nitro themes, Vencord's clienttheme plugin, or a single var: `--custom-theme-base-color`

I highly reccomend turning on send message button

## Development
deps: 
- nodejs
- npm
```
git clone https://github.com/Blade04208/shine.git
cd shine
npm i
npm start
```
add `http://localhost:5050/dev.css` to your quickcss or theme links and it should work! probably

### liquid glass
the labeled liquid glass settings in import.css require you to remake the liquid glass filter, just modify them and do a
```sh
python3 scripts/build-liquid-glass.py
```
and you should be good

# Contributing

you can contribute to either fix bugs, make faster, or make it closer-looking to the original twitpost

# Credits

Lyra Rebane - liqud glass svg