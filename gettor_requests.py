#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""
This library implements all of the email parsing features needed for gettor.
"""

import sys
import email
import dkim
import re

def getMessage():
    """ Read the message into a buffer and return it """
    rawMessage = sys.stdin.read()
    return rawMessage

def verifySignature(rawMessage):
    """ Attempt to verify the DKIM signature of a message and return a positive or negative status """
    signature = False

    # TODO XXX:
    # This should catch DNS exceptions and fail to verify if we have a 
    # dns timeout
    if dkim.verify(rawMessage):
        signature = True
        return signature
    else:
        return signature

def parseMessage(message):
    """ parse an email message and return a parsed email object """
    return email.message_from_string(message)

def parseReply(parsedMessage):
    """ Return an email address that we want to email """
    # TODO XXX: 
    # Scrub this data
    address = parsedMessage["from"]
    return address

def parseRequest(parsedMessage, packages):
    """ This parses the request and returns the first specific package name for
    sending. If we do not understand the request, we return None as the package
    name."""
    # XXX TODO:
    # Should we pick only the first line of the email body. Drop the rest?
    # It may be too unfriendly to our users
    for line in email.Iterators.body_line_iterator(parsedMessage):
        for package in packages.keys():
            match = re.match(package, line)    
            if match: 
                return package
    # If we get here, we didn't find a package we're currently serving
    return None

if __name__ == "__main__" :
    """ Give us an email to understand what we think of it. """
    packageList = { 
        "windows-bundle": "/var/lib/gettor/pkg/windows-bundle.z",
        "macosx-bundle": "/var/lib/gettor/pkg/macosx-bundle.z",
        "linux-bundle": "/var/lib/gettor/pkg/linux-bundle.z",
        "source-bundle": "/var/lib/gettor/pkg/source-bundle.z"
        }

    print _("Fetching raw message.")
    rawMessage = getMessage()
    # This doesn't work without DNS ( no wifi on board current airplane )
    print _("Verifying signature of message.")
    signature = verifySignature(rawMessage)
    print _("Parsing Message.")
    parsedMessage = parseMessage(rawMessage)
    print _("Parsing reply.")
    parsedReply = parseReply(parsedMessage)
    print _("Parsing package request.")
    package = parseRequest(parsedMessage, packageList)
    if package == None:
        package = "help"        
    else:
        package = packageList[package]

    print _("The signature status of the email is: %s") % str(signature)
    print _("The email requested the following reply address: %s") % parsedReply
    print _("It looks like the email requested the following package: %s") % package
    print _("We would select the following package file: ") % package
