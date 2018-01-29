#!/usr/bin/env python

'''
fetch_rsvps.py -- from Meetup emails, parse and output RSVPs

USAGE:

- 1) First, run "./fetch_rsvps.py fetch" to fetch RSVP candidate emails from Gmail.  
Provide "EMAIL" and "PASSWORD" in environment.

TIP: For security, generate an App Password, then use that as the PASSWORD
value.  When this program is finished, the app password is easily
deleted.  See https://support.google.com/mail/answer/185833?hl=en

- 2) "./fetch_rsvps.py" reads in emails from local database,
finds those from Meetup, and outputs each in tab-delimited report.
First column is Name of person, 2nd column is the message.

This second step can be repeated, since it's just using
the local filesystem. It's quick and easy to fine-tune the results
for the specific output desired.
'''

import email
import operator
import os
import pickle
import re
import sys
from imapclient import IMAPClient


RSVP_QUERY = 'from:info@meetup.com socal sent you a message'


def fetch_mail():
	"fetch email from Gmail"
	with IMAPClient(host="imap.gmail.com") as client:
		client.login(os.environ['EMAIL'], os.environ['PASSWORD'])
		client.select_folder('INBOX')

		rsvp_messages = client.gmail_search(RSVP_QUERY)

		return client.fetch(rsvp_messages, ['ENVELOPE', 'RFC822'])


def format_mails(mails):
	"find mail envelopes and plain text bodies"
	for raw_info in mails.values():
		envelope = raw_info[b'ENVELOPE']
		msg = email.message_from_string(raw_info[b'RFC822'].decode())
		text = None
		for num,part in enumerate(msg.walk()):
			if part.get_content_type() == 'text/plain':
				text = part.get_payload(decode=1)
		yield envelope, text and text.decode()


def parse_meetup_message(body):
	"parse Meetup email body to pick up name and message"
	fields_pat = re.compile(
		'(?P<name>		.+).sent.you.this.message.from.Meetup:\s+'
		'(?P<message>	.+?)'
		'(?:Member.since)'
		, re.DOTALL|re.VERBOSE)
	m = fields_pat.match(body)
	return m and m.groupdict()


def print_report(mails):
	def parseall():
		for envelope,text in format_mails(mails):
			if text:
				fields = parse_meetup_message(text)
				if fields:
					yield fields
				else:
					print('** BAD PARSE: {}'.format(text[:200]))
			else:
				print('** NO BODY: {}'.format(envelope.subject))
	for info in sorted(parseall(), key=operator.itemgetter('name')):
		message = re.sub('\n+', ' ', info['message'])
		print('{}\t{}'.format(info['name'], message))


if __name__ == '__main__':
	if sys.argv[-1] == 'fetch':
		mail_response = fetch_mail()
		pickle.dump(obj=mail_response, file=open('mails.pickle', 'wb'))

	else:
		mails = pickle.load(file=open('mails.pickle', 'rb'))
		print_report(mails)
		
