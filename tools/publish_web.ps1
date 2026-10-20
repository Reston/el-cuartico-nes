# Publish the game from origin/main and browser player to the dedicated gh-pages branch.
# Requires Node.js, Git, and push access to origin. No token is stored in this script.
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $projectRoot
try {
    $changes = git status --porcelain
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git status.' }
    if ($changes) { throw 'Commit your source changes before publishing, so the source links match the release.' }
    $remoteUrl = git remote get-url origin
    if ($LASTEXITCODE -ne 0 -or $remoteUrl -notmatch 'github\.com[:/]Reston/el-cuartico-nes(?:\.git)?$') {
        throw 'Expected origin to be Reston/el-cuartico-nes on GitHub.'
    }
    $sourceCommit = git rev-parse HEAD
    # Publish corresponding source before making its ROM available on Pages.
    git push origin HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Could not publish the source branch.' }
    git fetch origin main
    if ($LASTEXITCODE -ne 0) { throw 'Could not fetch the main game release.' }
    node (Join-Path $PSScriptRoot 'prepare_web.mjs')
    if ($LASTEXITCODE -ne 0) { throw 'Web packaging failed.' }
    $version = (git show origin/main:VERSION).Trim()
    $buildDirectory = [IO.Path]::GetFullPath((Join-Path $projectRoot 'build'))
    $releaseDirectory = [IO.Path]::GetFullPath((Join-Path $buildDirectory ('pages-release-' + [Guid]::NewGuid().ToString('N'))))
    if (-not $releaseDirectory.StartsWith($buildDirectory + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Release checkout must stay inside build/.'
    }
    New-Item -ItemType Directory -Path $releaseDirectory | Out-Null
    $authorName = git config user.name
    $authorEmail = git config user.email
    git -C $releaseDirectory init -b gh-pages
    git -C $releaseDirectory config user.name $authorName
    git -C $releaseDirectory config user.email $authorEmail
    git -C $releaseDirectory remote add origin $remoteUrl
    $pagesRef = git ls-remote --heads origin gh-pages
    if ($LASTEXITCODE -ne 0) { throw 'Cannot check the existing Pages branch.' }
    if ($pagesRef) {
        git -C $releaseDirectory fetch origin gh-pages
        if ($LASTEXITCODE -ne 0) { throw 'Cannot fetch the existing Pages branch.' }
        git -C $releaseDirectory switch -C gh-pages FETCH_HEAD
        if ($LASTEXITCODE -ne 0) { throw 'Cannot open the existing Pages branch.' }
        # Replace only tracked generated files in the verified isolated release checkout.
        git -C $releaseDirectory rm -r -f --ignore-unmatch .
        if ($LASTEXITCODE -ne 0) { throw 'Cannot replace the previous generated release.' }
    }
    Get-ChildItem -LiteralPath (Join-Path $buildDirectory 'web') -Force | Copy-Item -Destination $releaseDirectory -Recurse -Force
    git -C $releaseDirectory add --all
    git -C $releaseDirectory diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { Write-Output 'The published files already match this release.'; return }
    git -C $releaseDirectory commit -m "Publish main game v$version (website $sourceCommit)"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot commit the generated release.' }
    git -C $releaseDirectory push origin gh-pages
    if ($LASTEXITCODE -ne 0) { throw 'Pages push failed. Re-run to build on the latest remote branch.' }
    Write-Output 'Published files to gh-pages. Site: https://reston.github.io/el-cuartico-nes/'
} finally {
    Pop-Location
}
