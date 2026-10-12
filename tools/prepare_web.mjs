// No npm dependencies. The public player always packages the game from origin/main.
import { readFile, mkdir, copyFile, writeFile, readdir, rm } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourceRef = 'origin/main';
const commit = execFileSync('git', ['rev-parse', `${sourceRef}^{commit}`], { cwd: root, encoding: 'utf8' }).trim();
const releaseFile = name => execFileSync('git', ['show', `${commit}:${name}`], { cwd: root });
const version = releaseFile('VERSION').toString('utf8').trim();
if (!/^\d+\.\d+\.\d+$/.test(version)) throw new Error('Invalid VERSION');
const romName = `el-cuartico-v${version}-mmc5.nes`;
const rom = releaseFile(`dist/${romName}`);
if (rom.subarray(0, 4).toString('hex') !== '4e45531a' || ((rom[6] >> 4) | (rom[7] & 240)) !== 5) {
  throw new Error('Expected an iNES MMC5 ROM');
}
if (rom.length !== 16 + rom[4] * 16384 + rom[5] * 8192) throw new Error('Invalid ROM size');
const checksum = createHash('sha256').update(rom).digest('hex');
const sums = releaseFile('dist/SHA256.txt').toString('utf8');
if (!sums.split(/\r?\n/).some(line => line.trim() === `${checksum}  ${romName}`)) {
  throw new Error('Packaged ROM does not match dist/SHA256.txt');
}
const output = path.join(root, 'build', 'web');
// Only this fixed, generated output directory is replaced; ROM releases stay in dist/.
if (output !== path.resolve(root, 'build', 'web')) throw new Error('Unexpected output directory');
await rm(output, { recursive: true, force: true });
await mkdir(path.join(output, 'roms'), { recursive: true });
for (const name of await readdir(path.join(root, 'web'))) {
  await copyFile(path.join(root, 'web', name), path.join(output, name));
}
const websiteCommit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
const revision = `${commit.slice(0, 12)}-${websiteCommit.slice(0, 12)}`;
const html = await readFile(path.join(output, 'index.html'), 'utf8');
await writeFile(path.join(output, 'index.html'), html.replaceAll('__WEB_REVISION__', revision));
await writeFile(path.join(output, 'roms', romName), rom);
await writeFile(path.join(output, 'title-screen.png'), releaseFile('docs/media/menu-footer-v0.13.1.png'));
await writeFile(path.join(output, 'LICENSE.txt'), releaseFile('LICENSE'));
await writeFile(path.join(output, 'LEEME.txt'), releaseFile('dist/LEEME.txt'));
await writeFile(path.join(output, 'roms', 'SHA256.txt'), `${checksum}  ${romName}\n`);
await writeFile(path.join(output, '.nojekyll'), '');
const repo = 'https://github.com/Reston/el-cuartico-nes';
const config = { version, rom: `roms/${romName}`, source: `${repo}/tree/${commit}`, guide: `${repo}/blob/${commit}/docs/COMO-JUGAR.md` };
await writeFile(path.join(output, 'game-config.js'), `window.CUARTICO_GAME = ${JSON.stringify(config, null, 2)};\n`);
console.log(JSON.stringify({ directory: output, version, bytes: rom.length, sha256: checksum, sourceRef, sourceCommit: commit }, null, 2));
