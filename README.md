# nov18-news-image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/TUHIN729/nov18-news-image/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/TUHIN729/nov18-news-image/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A newspaper front page summing up Wednesday 18 November 2026 in one image: six stories from that day — Nvidia's first earnings without Jensen Huang, the US losing measles-free status, Israel electing a new Knesset speaker, Mongolia's president resigning, a 27-year sentence for the plot to kill Trump, and Germany and Norway funding Ukraine's air defences.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to the output directory. The image itself is drawn by `generate_image.py` (Python + Pillow, run at build time only) — rerun it to regenerate `entry.png` from the same six verified 18 November stories.

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
