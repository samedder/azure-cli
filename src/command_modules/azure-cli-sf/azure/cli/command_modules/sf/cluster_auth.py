# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.authentication import Authentication

class ClientCertAuthentication(Authentication):
    """
    Client certificate authentication for Service Fabric clusters

    :param str cert_path: Path to certificate to use for authentication
    :param str cert_password: Password if certificate is protected
    """
    def __init__(self, cert_path, cert_password=None):
        self.cert_path = cert_path
        self.cert_pass = cert_password

    def signed_session(self):
        """Create requests session with any required auth headers
        applied.

        :rtype: requests.Session.
        """
        session = super(ClientCertAuthentication, self).signed_session()
        if self.cert_pass is not None:
            session.cert = (self.cert_path, self.cert_pass)
        else:
            session.cert = self.cert_path

        return session
