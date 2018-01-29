#!/usr/bin/env python

import email
import os
import pickle
import re
import sys
from imapclient import IMAPClient


RSVP_QUERY = 'from:info@meetup.com socal sent you a message'


def fetch_mail():
	with IMAPClient(host="imap.gmail.com") as client:
		client.login(os.environ['EMAIL'], os.environ['PASSWORD'])
		client.select_folder('INBOX')

		rsvp_messages = client.gmail_search(RSVP_QUERY)

		return client.fetch(rsvp_messages, ['ENVELOPE', 'RFC822'])


def format_mails(mails):
	for raw_info in mails.values():
		envelope = raw_info[b'ENVELOPE']
		msg = email.message_from_string(raw_info[b'RFC822'].decode())
		text = None
		for num,part in enumerate(msg.walk()):
			if part.get_content_type() == 'text/plain':
				text = part.get_payload(decode=1)
		yield envelope, text and text.decode()


def simplify_text(body):
	goodpart_pat = re.compile('(.+?)(?:Member since)', re.DOTALL)
	try:
		return goodpart_pat.match(body).group(1)
	except IndexError:
		return 'XX-BAD-FORMAT'


if __name__ == '__main__':
	if sys.argv[-1] == 'fetch':
		mail_response = fetch_mail()
		pickle.dump(obj=mail_response, file=open('mails.pickle', 'wb'))

	else:
		mails = pickle.load(file=open('mails.pickle', 'rb'))
		for envelope,text in format_mails(mails):
			if text:
				print('okay: {}'.format(envelope.subject))
				print(simplify_text(text))
			else:
				print('** NO BODY: {}'.format(envelope.subject))
			print('\n')
