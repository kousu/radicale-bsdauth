# OpenBSD Authentication plugin for Radicale

This connects a [radicale](https://radicale.org/) install to the local
OpenBSD's [authenticate(3)](https://man.openbsd.org/authenticate.3) system
that it is installed on. It means you can access your calendars with the
same password you use for ssh and, perhaps, email, chat, etc.


## Installation

This has only been tested against `radicale>=3`, which is not yet packaged
for OpenBSD, so you must install that version manually.

**If you are currently using version 2, you should backup your calendars before proceeding**
because this implies doing a migration; but luckily, CalDAV is a pretty stable format and hopefully won't be hurt much by this:

```
doas pkg_add python3
doas pip install --upgrade pip
doas pip install "radicale>=3"

# ( these rest of these steps would normally be handled by pkg_add )
doas useradd -d /var/lib/radicale -m -L daemon -r 1..999 _radicale # if you don't already have this user
cat <<EOF | doas tee /etc/rc.d/radicale && doas chmod +x /etc/rc.d/radicale
#!/bin/ksh

daemon="/usr/local/bin/radicale"
daemon_user="_radicale"

. /etc/rc.d/rc.subr

rc_start() {
        \${rcexec} "\${daemon} \${daemon_flags} &"
}

pexp="/usr/local/bin/python3 /usr/local/bin/radicale"

rc_cmd $1
EOF
```


Then install the plugin:

```
doas pip install radicale-bsdauth
```

In order to function, you also need to grant `radicale` access to authenticate(3):

```
usermod -G auth _radicale
```

And then tell radicale to use it by editing [`/etc/radicale/config` or `/var/lib/radicale/.config/radicale/config`](https://radicale.org/v3.html#configuration) to add

```
[auth]
type = radicale_bsdauth
```


## Related Work

* [`radicale-auth-PAM`](https://pypi.org/project/radicale-auth-PAM/):

  OpenBSD's [authenticate(3)](https://man.openbsd.org/authenticate.3) is like
  Linux's [PAM(8)](https://man.archlinux.org/man/pam.8): a way to enable multiple
  ways to prove your identity, from passwords to LDAP to YubiKeys.

  So `radicale-auth-PAM` provides the same basic feature to `radicale`
  as `radicale-bsdauth`, and if you're using Linux you should use it.
