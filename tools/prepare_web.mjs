// No npm dependencies. Builds a small static site from the packaged release.
import { readFile, mkdir, copyFile, writeFile, readdir, rm } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const version = (await readFile(path.join(root, 'VERSION'), 'utf8')).trim();
if (!/^\d+\.\d+\.\d+$/.test(version)) throw new Error('Invalid VERSION');
const romName = `el-cuartico-v${version}-mmc5.nes`;
const rom = await readFile(path.join(root, 'dist', romName));
if (rom.subarray(0, 4).toString('hex') !== '4e45531a' || ((rom[6] >> 4) | (rom[7] & 240)) !== 5) {
  throw new Error('Expected an iNES MMC5 ROM');
}
if (rom.length !== 16 + rom[4] * 16384 + rom[5] * 8192) throw new Error('Invalid ROM size');
const checksum = createHash('sha256').update(rom).digest('hex');
const sums = await readFile(path.join(root, 'dist', 'SHA256.txt'), 'utf8');
if (!sums.split(/\r?\n/).some(line => line.trim() === `${checksum}  ${romName}`)) {
  throw new Error('Packaged ROM does not match dist/SHA256.txt');
}
const commit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
const output = path.join(root, 'build', 'web');
// Only this fixed, generated output directory is replaced; ROM releases stay in dist/.
if (output !== path.resolve(root, 'build', 'web')) throw new Error('Unexpected output directory');
await rm(output, { recursive: true, force: true });
await mkdir(path.join(output, 'roms'), { recursive: true });
for (const name of await readdir(path.join(root, 'web'))) {
  await copyFile(path.join(root, 'web', name), path.join(output, name));
}
await copyFile(path.join(root, 'dist', romName), path.join(output, 'roms', romName));
await copyFile(path.join(root, 'docs', 'media', 'aventura-menu-v0.14.0.png'), path.join(output, 'title-screen.png'));
await copyFile(path.join(root, 'LICENSE'), path.join(output, 'LICENSE.txt'));
await copyFile(path.join(root, 'dist', 'LEEME.txt'), path.join(output, 'LEEME.txt'));
await writeFile(path.join(output, 'roms', 'SHA256.txt'), `${checksum}  ${romName}\n`);
await writeFile(path.join(output, '.nojekyll'), '');
const repo = 'https://github.com/Reston/el-cuartico-nes';
const config = { version, rom: `roms/${romName}`, source: `${repo}/tree/${commit}`, guide: `${repo}/blob/${commit}/docs/AVENTURA.md` };
await writeFile(path.join(output, 'game-config.js'), `window.CUARTICO_GAME = ${JSON.stringify(config, null, 2)};\n`);
console.log(JSON.stringify({ directory: output, version, bytes: rom.length, sha256: checksum, sourceCommit: commit }, null, 2));
