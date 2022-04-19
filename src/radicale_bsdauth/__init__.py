# This file is part of Radicale Server - Calendar Server
# Copyright © 2008 Nicolas Kandel
# Copyright © 2008 Pascal Halter
# Copyright © 2008-2017 Guillaume Ayoub
# Copyright © 2017-2019 Unrud <unrud@outlook.com>
# Copyright © 2022 <kousu@kousu.ca>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with radicale-plugin-bsdauth.  If not, see <http://www.gnu.org/licenses/>.

"""
Use OpenBSD's authentication in Radicale.
See https://radicale.org/v3.html#authentication-plugins

At the most basic level, this lets you use the same username/password
you use for ssh with Radicale, but in principle also makes OpenBSD's other
backends like LDAP or YubiKey available, similar to how Linux and FreeBSD
have PAM, if you have enabled those.
See http://man.openbsd.org/login.conf.5#AUTHENTICATION

In order for this to function on OpenBSD, you must authorize it first by

    usermod -G auth _radicale

Then you need to enable it in your radicale config with

    [auth]
    type = radicale_bsdauth

See https://radicale.org/v3.html#plugins

( This was inspired by Dovecot's https://doc.dovecot.org/configuration_manual/authentication/bsdauth/ ! )
"""


import sys
import ctypes

from radicale import auth


def auth_userokay(name, password, type=None, style=None):
    """
    wrap auth_userokay(8). see its manpage for full details.
    quickly though: name is the username, password is the password
    style defines the authentication method to use ('passwd' by default for most users, but could be anything in /usr/libexec/auth/login_*)
      if left unset, the *user* can set it by setting their username to 'name:style'
    type is just for logging: your app should an authentication

    Example:
      auth_userokay('test1', 'test1test1', 'spiffyd')
    """
    libc = ctypes.CDLL("libc.so")

    # convert python strings to C strings
    # None doubles as the NULL pointer, when translated by ctypes
    if name is not None:
        name = ctypes.c_char_p(name.encode())
    if style is not None:
        style = ctypes.c_char_p(style.encode())
    if type is not None:
        type = ctypes.c_char_p(type.encode())
    if password is not None:
        password = ctypes.c_char_p(password.encode())

    return bool(libc.auth_userokay(name, style, type, password))


class Auth(auth.BaseAuth):
    def login(self, login, password):
        if auth_userokay(login, password):
            # the user might have passed 'username:style' to
            # pick a particular backend 'style'; see auth_userokay(3).
            # At this point, we don't need 'style' anymore.
            username = login.split(":", 1)[0]
            return username
