# PayMySitter
A skeleton project of the real PayMySitter Python web application (www.paymysitter.com or paymysitter.appspot.com) running in Google Cloud Platform with Stripe payments integration.

While I cannot put the codebase here, this will be instructive if you can read pseudo-code:
- learning how to put Python web apps up on GCP, formerly strictly GAE (Google App Engine)
- working with Managed Accounts in Stripe (purely an API implementation)
- working with a combination of SQL and NoSQL datastores

**app.yaml**<br/>
This is your starting point for configuration
examplesecuredirectory - this calls out to a separate .app file for code execution. This would be useful if you have a separate codebase for handling "admins" for the web app, like Google Login auth users. Everything else (like regular non-admin, authenticated or not) falls to main.app

**index.yaml**
These are your indexes for your queries

**/templates/circleinvite.html**
An example of a HTML template that would be rendered using the Jinja2 templating engine
- Example of leveraging the Google Image API in Jinja2 (40 pixels wide by tall, aspect ratio)
  {{ member.pictureservingurl|replace('http', 'https') }}=s40{% else %}/img/icon57.png{% endif %}
- Example of iterating over a loop in Jinja2
  {% for each_member in connectionsIMadeMemberList %}

**/js/pages/stripepaymentauthwizard.js**
An exampe of how you might like to do a little client side JavaScript simple field validation using Stripe's payment library

Again, this is all pseudo code:
**main.py**
Your main execution program.
- An example of how you can set an app secret_key for session cookies in Python (#>>> means the Python shell)
  #>>> import uuid
  #>>> x = uuid.uuid4()
  #>>> x.bytes
- An example of creating your own custom Jinja2 function for dynamic HTML rendering
  @app.template_filter('format_cents_as_currency')
    def format_cents_as_currency_filter(value):
    return "${:,.2f}".format(float(value) / 100.0)
- An example of logging in
  @app.route('/signinauthenticate', methods=['POST'])
- An example of saving a photo using Google's Blobstore and Image API
  @app.route('/userprofilephotoconfirm', methods=['POST'])
- An example of making a synchronous call to Stripe to set up a subscription plan for a member
  @app.route('/subscriptionsignupconfirm', methods=['POST'])
- An example of listening out for asynchronous webhook callbacks from Stripe to your app
  You could obfuscate this URL below and provide it to Stripe. That should cut down on random calls from script kiddies
  @app.route('/stripewebhookbdfjkl4378hsfk43jkasdkl', methods=['POST'])
- An example of logging out
  @app.route('/signout')
- Some basic error handlers too

**pmsdatamodel.py**
An example of using an external Python class to represent data models for Google Cloud's NDB and Blobstore

**pmsmemberinfo.py**
An example of retrieving an entity from regular SQL-like CloudSQL and NoSQL, Google's High Replication Datastore

**pmsemailutility.py**
An example of sending email out via the Google mail API by rendering a HTML template

**pmstextutility.py**
An example of a crude text messaging utility via email - or you could use Twilio or other APIs

**/lib**
flask
jinja2
markupsafe
requests
stripe
werkzeug