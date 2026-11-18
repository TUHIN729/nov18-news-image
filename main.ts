// "One World, One Day" — 18 November 2026 (Node 22, standard library only).
// The entry image is entry.png beside this file; the program copies it to
// /output/entry.png. Deterministic, no network, no other files read.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
