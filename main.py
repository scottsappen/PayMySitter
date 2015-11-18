import os
import sys
import logging
import uuid
import traceback
import datetime
import cgi
import MySQLdb
import stripe
import re
import requests
import urllib
import time
import pmsconstants

from flask import Flask, render_template, request, jsonify, redirect, url_for, Markup, session, Response
from werkzeug import parse_options_header, generate_password_hash, check_password_hash
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.api import mail, users, memcache, images
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from datetime import date, datetime, timedelta
from webapp2_extras import security

from pmsdatamodel import Members.........
from pmsmemberinfo import MemberInfo
from pmsemailutility import EmailerUtility
from pmstextutility import TextUtility

app = Flask(__name__)

app.secret_key = ...


#Custom template filters
@app.template_filter('format_cents_as_currency')
def format_cents_as_currency_filter(value):
  return "${:,.2f}".format(float(value) / 100.0)




#:: SIGNING IN AUTHENTICATION ::
#Someone is trying to login
@app.route('/signinauthenticate', methods=['POST'])
def signinauthenticate():

    #grab the request data
    try:
      #or use a email parsing library, you get the idea and do something...
      inputEmailAddress = request.form.get("inputEmailAddress")
      if not re.match(r"[^@]+@[^@]+\.[^@]+", inputEmailAddress):
      if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", inputEmailAddress):

      inputPassword = request.form.get("inputPassword")

      #Query NoSQL and find out if this member already exists by email, if so, show the error
      member = MemberInfo()
      member = member.getMemberInfoByEmail(inputEmailAddress)

      #Make sure the password is correct
      if not check_password_hash(member.passwordhash, inputPassword):
        return render_template('index.html', inputEmailAddress=inputEmailAddress, alertmessage='It appears that is not quite right.')
      
      #Save the session and cookie values (do more than just email, but again, you get the idea)
      session[_SESSION_COOKIE_EMAIL] = member.emailaddress

      return redirect(url_for('landingpage'))
      
    except:
      return render_template('index.html', inputEmailAddress='', alertmessage='Oops!')



#:: SAVE USER PROFILE PHOTO ::
#This route only gets used when a user saves updates to their profile photo
@app.route('/userprofilephotoconfirm', methods=['POST'])
def userprofilephotoconfirm():
    member = MemberInfo()

    #this will cause an ugly key error if we don't handle it properly
    try:
      inputUploadedPictureFile = request.files['inputProfilepicture']
      if inputUploadedPictureFile:
        header = inputUploadedPictureFile.headers['Content-Type']
        parsed_header = parse_options_header(header)
        blob_key = parsed_header[1]['blob-key']
    except:
      #no need to log this error output
      dummyvariable = ""

      #a user is uploading a picture, either new if they did not have one prior, or uploaded a new one which would delete the old one
      if inputUploadedPictureFile:
        if member.pictureblobstorekey:
          blobstore.delete(member.pictureblobstorekey)
          images.delete_serving_url(member.pictureblobstorekey)
        member.pictureservingurl = images.get_serving_url(blob_key)
        member.pictureblobstorekey = blob_key
        member.put()

      return render_template('userprofilephotosaved.html', member=member)
    except:
      try:
        #If you couldn't complete the user save, be sure to delete the photo from the blobstore or re-use it later (to avoid a lost child hanging around)
        inputUploadedPictureFile = request.files['inputProfilepicture']
        if inputUploadedPictureFile:
          header = inputUploadedPictureFile.headers['Content-Type']
          parsed_header = parse_options_header(header)
          blob_key = parsed_header[1]['blob-key']
          blobstore.delete(blob_key)
      except:
        #no need to log this error output
        dummyvariable = ""
      #Create a new form POST URL for the blobstore
      userprofilephoto_form_url = blobstore.create_upload_url('/userprofilephotoconfirm')
      return render_template('userprofilephoto.html', member=member, userprofilephoto_form_url=userprofilephoto_form_url, user_profilepicturesrc=user_profilepicturesrc, alertmessage='Oops!', userprofilephoto_form_url=userprofilephoto_form_url, user_profilepicturesrc=user_profilepicturesrc)



#:: SUBSCRIPTION SIGN UP CONFIRMATION ::
#This route only gets used when a parent signs up for a plan
@app.route('/subscriptionsignupconfirm', methods=['POST'])
def subscriptionsignupconfirm():
    member = MemberInfo()

    try:
      #Set the required stripe API key that is going to be used
      stripe.api_key = _STRIPE_SECRET_KEY

      #If this person has a stripecustomerid (they are a Stripe customer object), then just update the plan!
      if stripeprofile.stripecustomerid:
        #Retrieve the customer from Stripe
        try:
          stripeCustomer = stripe.Customer.retrieve(stripeprofile.stripecustomerid)
        except:
          # The card has been declined
          logging.error(':: Error | subscriptionsignupconfirm | 1 -- Error creating a new subscription ... ::')
          raise Exception
      else:
        #If this person does not have a stripecustomerid (they are not a Stripe customer object), then they MUST have a token, otherwise we bomb
        inputStripeToken = request.form.get("inputStripeToken")
        if not inputStripeToken:
          logging.error(':: Error | subscriptionsignupconfirm | 1 -- inputStripeToken was None ... ::')
          raise Exception
        #Create a new Stripe customer for this member
        try:
          stripeCustomer = stripe.Customer.create(
            source=inputStripeToken,
            email=member.emailaddress
          )
          #Save that payment profile object
          stripeprofile.stripecustomerid = stripeCustomer.id
        except:
          # The card has been declined
          logging.error(':: Error | subscriptionsignupconfirm | 1 -- Error creating a new subscription ... ::')
          raise Exception

      #This customer update call will update the customer subscription
      try:
        #Save the plan on the customer record at Stripe
        #planType could be any plan you set up at Stripe, like a yearly or monthly plans perhaps
        subscription = stripeCustomer.subscriptions.create(plan=planType)
        #Save the plan type for the user in NoSQL
        stripeprofile.stripe_subscription_plan = planType
        stripeprofile.stripe_subscription_id = subscription.id
        #You could even use gift codes in your app very easily too
        #if inputGiftCode:
        #  stripeprofile.subscriptiongiftcode = inputGiftCode
        #else:
        #  stripeprofile.subscriptiongiftcode = None
        #stripeprofile.put()
      except:
        # The card has been declined
        logging.error(':: Error | subscriptionsignupconfirm | 1 -- Error creating a new subscription ... ::')
        raise Exception
        
      return redirect(url_for('subscriptionsignupsuccess'))

    except:
      logging.error(':: Error | subscriptionsignupconfirm | An error occurred trying ... ::')
      logging.error(traceback.format_exc())
      return render_template('subscriptionsignupfailure.html', member=member)





#:: STRIPE ACCOUNT WEBHOOK ::
#Used by Stripe to contact us programmatically telling us about certain back-end events, like an account that has become unverified due to incorrect information
@app.route('/stripewebhookbdfjkl4378hsfk43jkasdkl', methods=['POST'])
def stripewebhookbdfjkl4378hsfk43jkasdkl():
    webhookJSON = request.get_json()

    #Get the type of event
    eventType = webhookJSON.get('type')

    #Get the live mode of event
    eventMode = webhookJSON.get('livemode')
    if not eventMode:
      return Response(status=200)

    #Get the event ID and Account ID
    eventID = webhookJSON.get('id')
    eventAccountID = webhookJSON.get('user_id')

    #Check if this event ID already exists in our system, no need to call Stripe for a duplicate event
    if eventexists...:
      return Response(status=200)

    #Call Stripe asking for event details for that event ID.
    stripe.api_key = pmsconstants._STRIPE_SECRET_KEY
    stripeEvent = None
    try:
      #Get the stripe event from Stripe itself using the eventID as input
      stripeEvent = stripe.Event.retrieve(id=eventID, stripe_account=eventAccountID)
    except:
      #If botched request for some reason return 300 so Stripe will re-send it
      logging.error(traceback.format_exc())
      return Response(status=300)

    #If botched request for some reason return 300 so Stripe will re-send it
    if not stripeEvent:
      logging.error(traceback.format_exc())
      return Response(status=300)

    #Check and make sure the event from Stripe is live and not test and also an account.updated event
    if stripeEvent.type=='account.updated' and stripeEvent.livemode:
      #Call Stripe, asking for the Account entity, get legal_entity
      stripeAccount = stripe.Account.retrieve(stripeprofile.stripeaccountid)

    #and so on...keep processing whatever business logic is required

    return Response(status=200)



#:: LOGOUT ::
#This is where users will logout
@app.route('/signout')
def signout(action=None, param=None):
    #Remove the session cookie security goodies
    if _SESSION_COOKIE_EMAIL in session:
      session.pop(_SESSION_COOKIE_EMAIL, None)

    return render_template('signedout.html')



#:: Error handlers ::
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    logging.error(':: A 404 was thrown a bad URL was requested ::')
    logging.error(traceback.format_exc())
    return render_template('404.html'), 404



@app.errorhandler(400)
def key_error(e):
    logging.error(':: A 400 was thrown key_error ::')
    logging.error(traceback.format_exc())
    return render_template('400.html'), 400
