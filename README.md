[![Build Status](https://travis-ci.org/andrewbeng89/tictactoe.svg?branch=master)](https://travis-ci.org/andrewbeng89/tictactoe)

## Part 1: Travis and Google App Engine (GAE)

Travis-CI is used to test and deploy updates to Google App Engine.

### Install Travis Ruby Gem

The Travi-CI gem will be used to encrypt a OAuth2 token that will be used to push updates to Google App Engine from the Travis build.

1. From the terminal, install the gem by entering `gem install travis`

###Install and run GAE Python SDK

From the console of your Nitrous.IO Box, execute the following commands:

1. cd ~/
2. curl http://googleappengine.googlecode.com/files/google_appengine_1.8.8.zip > gae_python-1.8.8.zip
3. unzip gae_python-1.8.8.zip
4. rm gae_python-1.8.8.zip

Sign up for Google App Engine if you haven’t. Create a new GAE Application. Fork this GitHub repository to your own GitHub account: https://github.com/andrewbeng89/tictactoe/. Clone the forked repository to your Nitrous.IO Box:

1. `git clone git@github.com:<your-github-account>/tictactoe.git`
2. Run the development server on Nitrous.IO: `~/google_appengine/dev_appserver.py --host=0.0.0.0 --port=8080 ~/tictactoe/`
3. To preview the app, select “Port 8080” from the “Preview” dropdown:

To configure a new GitHub repository and GAE app:

2. `cd tictactoe`
3. Reomve the .git directory `rm -rf .git`
4. Create a new GitHub repository with your account
5. Initialise the demo app as a git repo: `git init`
6. Add the remote to the newly create GitHub repository `git remote add origin git@github.com:<your_username>/<your_new_repo>.git`
7. Create a new GAE application [here](https://appengine.google.com/)
8. Open the app.yaml file and edit the following line: `application: <new-gae-app-id>`


### First Deploy to GAE

The very first deployment to GAE has to be made from the Nitrous.IO in order to retrieve the OAuth2 refresh_token which Travis-CI will use later

1. From the console, enter `appcfg.py --noauth_local_webserver --oauth2 update ./`
2. A link will be displayed, followed by a promt to enter an access code. Open the link in a new browser tab and allow Google to grant access. Copy the access code displayed to the clipboard
3. Paste the access code in the VM terminal and hit return
4. Open the .appcfg_oauth2_tokens (JSON) file and copy the value of the refresh_token field
5. Remove this line from the .travis.yml file `secure: <existing secure token>`
6. Encrypt this token as a secure global variable in the .travis.yml file `travis encrypt MY_GAE_TOKEN="<paste_token_from_clipboard>" --add -r <your_github_username/your_github_repo>`
7. Check the .travis.yml file to see whether the new secure variable has been added


### Setup and Build with Travis-CI

1. Register for [Travis-CI](https://travis-ci.org) using your GitHub account
2. From your Travis-CI [profile](https://travis-ci.org/profile) page, enable the newly created GitHub repository
3. Edit this line of the .travis.yml file: `- git clone https://github.com/<your_username>/<your_repo>.git deploy`
4. Add all file and folders `git add -A .`
5. Commit with message `git commit -a -m 'created GAE project'`
6. Push the update `git push origin master`
7. You can track the build progress at the Travis-CI website


### Functional and Unit Testing with Nose and Travis-CI

The Nose module allows developers to create simple functional and unit tests. In this sample app, the tests are in the /test.py file. This file tests the funcitonality of a single API call /api/get_bots. To break this test:

1. Edit line 96 in main.py to `@bottle.route('/api/get_bot')`
2. Commit and push the changes
3. Track the build progress on travis-ci


### View the GameBots demo app [here](http://gamebots-python.appspo.com)

## Python Bottle Framework Scaffold for Google App Engine

A skeleton for building Python applications on Google App Engine with the
[Bottle micro framework](http://bottlepy.org) version 0.11.6

See our other [Google Cloud Platform github
repos](https://github.com/GoogleCloudPlatform) for other sample applications.

## Run Locally
1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).
See the README file for directions. You'll need python 2.7 and [pip 1.4 or later](http://www.pip-installer.org/en/latest/installing.html) installed too.

2. Clone this repository with

   ```
   git clone https://github.com/GoogleCloudPlatform/appengine-python-bottle-skeleton.git
   ```
3. Install dependencies in the project's lib/ directory - App Engine
   can only import libraries from inside your project directory.

   ```
   cd appengine-python-bottle-skeleton
   pip install -r requirements.txt -t lib/
   ```
4. Run this project locally from the command line:

   ```
   dev_appserver.py <projectDirectory>
   ```

Open [http://localhost:8080](http://localhost:8080)

See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver)
for options when running dev_appserver.

## Deploy
To deploy the application:

1. Use the [Admin Console](https://appengine.google.com) to create an app and
   get the project/app id. (App id and project id are identical)
1. [Deploy the
   application](https://developers.google.com/appengine/docs/python/tools/uploadinganapp) with

```
appcfg.py -A <your-project-id> --oauth2 update <projectDirectory>
```
1. Congratulations! Your application is now live at your-project-id.appspot.com

## Next Steps
This skeleton includes TODO markers you can search for to determine some of the
basic areas you will want to customize.

### Relational Databases and Datastore
To add persistence to your models, use
[NDB](https://developers.google.com/appengine/docs/python/ndb/) for
scale.  Consider
[CloudSQL](https://developers.google.com/appengine/docs/python/cloud-sql) if you need a
relational database.

### Installing Libraries
See the [Third party
libraries](https://developers.google.com/appengine/docs/python/tools/libraries27)
page for libraries that are already included in the SDK.  To include SDK
libraries, add them in your app.yaml file. All other libraries must be included
in your project directory in order to be used by App Engine.  Only pure python
libraries may be added to an App Engine project.


### Feedback
Star this repo if you found it useful. Use the github issue tracker to give
feedback on this repo and to ask for skeletons for other frameworks or use cases.

## Contributing changes
See [CONTRIB.md](CONTRIB.md)

## Licensing
Note, this project includes source files that are licensed under terms
other than Apache 2.0.

* This project's source code: See [LICENSE](LICENSE) file.

* Bottle Microframe work: See [bottle.py](bottle.py) file.

## Authors
Logan Henriquez and Johan Euphrosine
