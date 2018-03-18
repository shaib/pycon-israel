# ilpycon

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
npm install
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites conference sponsor_levels sponsor_benefits proposal_base pages audience
./manage.py sitetree_resync_apps ilpycon
./manage.py compilemessages
./manage.py createsuperuser --username=admin --email=admin@example.com --noinput
./manage.py loaddata sponsors  # db must have at least 1 user to load that
npm run dev
```

Browse to http://localhost:3000/

## Common operations

### Editing pages

After editing static pages from the CMS, export them them into fixtures using the following command:
```
./manage.py dumpdata --indent 2 pinax_pages >fixtures/pages.json
```

After changing symposion metadata:
```
./manage.py dumpdata --indent 4 symposion_conference >fixtures/conference.json
./manage.py dumpdata --indent 4 symposion_sponsorship.sponsorlevel >fixtures/sponsor_levels.json
./manage.py dumpdata --indent 4 symposion_sponsorship.benefit symposion_sponsorship.benefitlevel >fixtures/sponsor_benefits.json
```
Until we have master db access, we pass data via fixtures as well, so when editing sponsors do:
```
./manage.py dumpdata --indent 4 symposion_sponsorship.sponsor symposion_sponsorship.sponsorbenefit >fixtures/sponsors.json
```

### Adding translations

To (re)create the translation files:

```
./manage.py makemessages --keep-pot --locale "he"
#./manage.py makemessages --domain djangojs --keep-pot --locale "he"  # For js (we don't need this yet)
```
## Deploy a branch to Heroku

- Use the `pycon.israel.devops@gmail.com` account to add site collaborators
- Install the Heroku CLI and login via `heroku login`
- Before pushing, we need to setup the buildpacks (gettext, nodejs, python - in that order):
```
  heroku buildpacks:add https://github.com/piotras/heroku-buildpack-gettext.git
  heroku buildpacks:add heroku/nodejs
  heroku buildpacks:add heroku/python
```
  verify the resulting list using: `heroku buildpacks`, check that these and only these appear
  on the list. If not, use `heroku buildpacks:remove -i {number}` to remove bad ones.

- `git push heroku $branch_name:master`, e.g. `git push heroku heroku-deploy:master`

## Configure the site to be ran behind a reverse proxy

To run the site behind a reverse proxy, we need to:

- Set the proxy path via `settings.FORCE_SCRIPT_NAME`
- Update the `domain` of the current `contrib.sites.Site` model to include the proxy (since current_site.domain is used in Symposion templates to construct URLs)

### Setting the reverse proxy path
_e.g., configure the project to be accessed via `/2018-WIP` rather than `/`:_

1. Set the `FORCE_SCRIPT_NAME` env var:

```
heroku config:set FORCE_SCRIPT_NAME="/2018-WIP"
```

2. Run the `update_site_domain` management command:

```
heroku run python manage.py update_site_domain
```

3. Restart the web dyno(s) to pick up the change to Site.domain

```
heroku ps:restart web
```

### Updating the reverse proxy path
_e.g., configure the project to be accessed via `/2018` rather than `/2018-WIP`:_

1. Update the `FORCE_SCRIPT_NAME` env var:

```
heroku config:set FORCE_SCRIPT_NAME="/2018"
```

2. Run the `update_site_domain` management command:

```
heroku run python manage.py update_site_domain
```

3. Restart the web dyno(s) to pick up the change to Site.domain

```
heroku ps:restart web
```


### Clearing the reverse proxy path

1.  Clear the `FORCE_SCRIPT_NAME` env var:

```
heroku config:remove FORCE_SCRIPT_NAME
```

2. Run the `update_site_domain` management command:

```
heroku run python manage.py update_site_domain
```

3. Restart the web dyno(s) to pick up the change to Site.domain

```
heroku ps:restart web
```
