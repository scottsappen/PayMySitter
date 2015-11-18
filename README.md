# PayMySitter
A skeleton project of the real PayMySitter Python web application (http://www.paymysitter.com or http://paymysitter.appspot.com) running in Google Cloud Platform with Stripe payments integration.

While I cannot put the codebase here, this will be instructive if you can read pseudo-code:
- learning how to put Python web apps up on GCP, formerly strictly GAE (Google App Engine)
- working with Managed Accounts in Stripe (purely an API implementation)
- working with a combination of SQL and NoSQL datastores (use together for a nice combination of relational flexibility and massive scale)

**app.yaml**<br/>
This is your starting point for configuration<br/>
examplesecuredirectory - this calls out to a separate .app file for code execution. This would be useful if you have a separate codebase for handling "admins" for the web app, like Google Login auth users. Everything else (like regular non-admin, authenticated or not) falls to main.app

**index.yaml**<br/>
These are your indexes for your queries

**/templates/circleinvite.html**<br/>
An example of a HTML template that would be rendered using the Jinja2 templating engine<br/>
- Example of leveraging the Google Image API in Jinja2 (40 pixels wide by tall, aspect ratio)<br/>
  `{{ member.pictureservingurl|replace('http', 'https') }}=s40{% else %}/img/icon57.png{% endif %}`
- Example of iterating over a loop in Jinja2<br/>
  `{% for each_member in connectionsIMadeMemberList %}`

**/js/pages/stripepaymentauthwizard.js**<br/>
An exampe of how you might like to do a little client side JavaScript simple field validation using Stripe's payment library

**main.py**<br/>
Your main execution program.
- An example of how you can set an app secret_key for session cookies in Python (#>>> means the Python shell)<br/>
  `#>>> import uuid`<br/>
  `#>>> x = uuid.uuid4()`<br/>
  `#>>> x.bytes`<br/>
- An example of creating your own custom Jinja2 function for dynamic HTML rendering<br/>
  `@app.template_filter('format_cents_as_currency')`<br/>
    `def format_cents_as_currency_filter(value):`<br/>
    `return "${:,.2f}".format(float(value) / 100.0)`<br/>
- An example of logging in<br/>
  `@app.route('/signinauthenticate', methods=['POST'])`<br/>
- An example of saving a photo using Google's Blobstore and Image API<br/>
  `@app.route('/userprofilephotoconfirm', methods=['POST'])`<br/>
- An example of making a synchronous call to Stripe to set up a subscription plan for a member<br/>
  `@app.route('/subscriptionsignupconfirm', methods=['POST'])`<br/>
- An example of listening out for asynchronous webhook callbacks from Stripe to your app<br/>
  You could obfuscate this URL below and provide it to Stripe. That should cut down on random calls from script kiddies<br/>
  `@app.route('/stripewebhookbdfjkl4378hsfk43jkasdkl', methods=['POST'])`<br/>
- An example of logging out<br/>
  `@app.route('/signout')`<br/>
- Some basic error handlers too

**pmsdatamodel.py**<br/>
An example of using an external Python class to represent data models for Google Cloud's NDB and Blobstore

**pmsmemberinfo.py**<br/>
An example of retrieving an entity from regular SQL-like CloudSQL and NoSQL, Google's High Replication Datastore

**pmsemailutility.py**<br/>
An example of sending email out via the Google mail API by rendering a HTML template

**pmstextutility.py**<br/>
An example of a crude text messaging utility via email - or you could use Twilio or other APIs

**/lib**<br/>
flask<br/>
jinja2<br/>
markupsafe<br/>
requests<br/>
stripe<br/>
werkzeug<br/>