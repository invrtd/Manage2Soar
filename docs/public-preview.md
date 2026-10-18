# Public-site preview (`/preview/`)

An unlisted, self-contained draft of the redesigned public website, used to let
members review the proposed look before anything changes on the live site.

## What it is

- Served at `/preview/` (home) and `/preview/<slug>/`.
- Pages: `start-here` (Learn to Fly), `our-fleet`, `location` (Visit Us),
  `gallery`, `documents` (Club Files).
- Rendered entirely from bundled content (`preview/content.py`) and bundled
  static assets (`static/preview/`). It does **not** read CMS rows, the
  database, or `MEDIA_ROOT`, so it cannot affect the live site's content.
- Every page is marked `noindex, nofollow` and nothing links to it. The URL is
  unguarded (no token) — the branch is the on/off switch.
- The "Leave feedback" button reuses the existing SiteFeedback form
  (`/cms/feedback/`), which requires an active-member login.

## Branch model

The preview lives **only** on the `public-preview` branch:

- `public-preview` = `main` + the preview.
- The only file it changes from `main` is `manage2soar/urls.py` (adds the
  `preview/` route). Everything else is new files:
  - `preview/` (content + views + urls)
  - `templates/preview/base.html`
  - `static/preview/img/`, `static/preview/pdf/`
  - `static/css/public-site.css`

`main` does not contain any of it.

## Prerequisites

- Deployment: single-host Ansible (`infrastructure/ansible`), server
  `dev.antelopevalleysoaringclub.org`, settings `manage2soar.settings_single_host`,
  playbook `playbooks/single-host.yml`.
- Vault password file at `~/.ansible_vault_pass`.
- The deployed branch is controlled by `m2s_git_branch` in
  `infrastructure/ansible/group_vars/single_host/vars.yml` (currently `main`).

## Deploy / enable

```bash
# 1. Publish the branch
git push -u origin public-preview      # from a checkout of the public-preview branch

# 2. Point the deploy at the branch
#    Edit infrastructure/ansible/group_vars/single_host/vars.yml:
#      m2s_git_branch: "public-preview"

# 3. Deploy (updates code, runs migrations, collectstatic, restarts gunicorn)
cd infrastructure/ansible
ansible-playbook -i inventory/single_host.yml \
  --vault-password-file ~/.ansible_vault_pass playbooks/single-host.yml
```

Then open:

```
https://dev.antelopevalleysoaringclub.org/preview/
```

### Verify

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://dev.antelopevalleysoaringclub.org/preview/
curl -s -o /dev/null -w '%{http_code}\n' https://dev.antelopevalleysoaringclub.org/preview/location/
# expect 200 for both; /preview/nope/ should be 404
```

## Take down / disable (no trace on the site)

```bash
# 1. Point the deploy back at main
#    Edit infrastructure/ansible/group_vars/single_host/vars.yml:
#      m2s_git_branch: "main"

# 2. Redeploy — git checkout removes the preview code from /opt/m2s/app
cd infrastructure/ansible
ansible-playbook -i inventory/single_host.yml \
  --vault-password-file ~/.ansible_vault_pass playbooks/single-host.yml

# 3. Purge the collected static files (collectstatic never deletes stale files,
#    and WhiteNoise serves them directly). Use the host/user from
#    infrastructure/ansible/inventory/single_host.yml
ssh <ssh-user>@<server> \
  'sudo rm -rf /var/www/m2s/static/preview /var/www/m2s/static/css/public-site.css'
```

After step 2 the route no longer exists (404 for everyone) and nothing links to
it. Step 3 removes the only remaining artifact.

## Full removal from git

```bash
# on the public-preview branch — or simply delete the branch:
git push origin --delete public-preview      # remote
git branch -D public-preview                 # local
```

Deleting the branch plus the server-side purge above leaves no trace of the
preview.

## Notes

- `public-site.css` is only linked from `templates/preview/base.html`, so it is
  inert on `main`.
- `collectstatic` copies but does not delete; always do the `rm -rf` in the
  purge step after disabling.
- Deploying `main` after the preview is a no-op for the public site — the route
  and assets are simply absent.
