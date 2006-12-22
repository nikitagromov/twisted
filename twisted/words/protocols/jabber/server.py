# -*- test-case-name: twisted.words.test.test_jabberserver -*-
#
# Copyright (c) 2001-2006 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
XMPP Server-to-Server protocol.

This module implements several aspects of XMPP server-to-server communications
as described in XMPP Core (RFC 3920). Refer to that document for the meaning
of the used terminology.
"""

from Crypto.Hash import SHA256
import hmac

from zope.interface import implements
from twisted.words.protocols.jabber import ijabber

NS_DIALBACK = 'jabber:server:dialback'

def generateKey(secret, receivingServer, originatingServer, streamID):
    """
    Generate a dialback key for server-to-server XMPP Streams.

    The dialback key is generated using the algorithm described in
    U{XEP-0185<http://www.xmpp.org/extensions/xep-0185.html>}. The used
    terminology for the parameters is described in RFC-3920.

    @param secret: the shared secret known to the Originating Server and
                   Authoritive Server.
    @type secret: C{str}
    @param receivingServer: the Receiving Server host name.
    @type receivingServer: C{str}
    @param originatingServer: the Originating Server host name.
    @type originatingServer: C{str}
    @param streamID: the Stream ID as generated by the Receiving Server.
    @type streamID: C{str}
    @return: hexadecimal digest of the generated key.
    @type: C{str}
    """

    hashedSecret = SHA256.new(secret).hexdigest()
    message = " ".join([receivingServer, originatingServer, streamID])
    hash = hmac.HMAC(hashedSecret, message, digestmod = SHA256)
    return hash.hexdigest()

class OriginatingDialbackInitializer(object):
    """
    Server Dialback Initializer for the Orginating Server.
    """

    implements(ijabber.IInitiatingInitializer)

    _deferred = None

    def __init__(self, xs, secret):
        self.xmlstream = xs
        self.secret = secret

    def initialize(self):
        self._deferred = defer.Deferred()
        self.xmlstream.addObserver(xmlstream.STREAM_ERROR_EVENT,
                                   self.onStreamError)
        self.xmlstream.addObserver("/result[@xmlns='%s']" % NS_DIALBACK,
                                   self.onResult)

        key = generateKey(self.secret, self.xmlstream.otherHost,
                          self.xmlstream.thisHost, self.sid)

        result = domish.Element((NS_DIALBACK, 'result'))
        result['from'] = self.xmlstream.thisHost
        result['to'] = self.xmlstream.otherHost
        result.addContent(key)

        self.xmlstream.send(result)

    def onResult(self, result):
        self.xmlstream.removeObserver(xmlstream.STREAM_ERROR_EVENT,
                                      self.onStreamError)
        if result['type'] == 'valid':
            self._deferred.callback(None)
        else:
            self._deferred.errback(DialbackFailed())

    def onStreamError(self, failure):
        self.xmlstream.removeObserver("/result[@xmlns='%s']" % NS_DIALBACK,
                                      self.onResult)
        self._deferred.errback(failure)
