# OpenBSD Authentication plugin for Radicale

This connects a [radicale](https://radicale.org/) install to the local
OpenBSD's [authenticate(3)](https://man.openbsd.org/authenticate.3) system
that it is installed on. It means you can access your calendars with the
same password you use for ssh and, perhaps, email, chat, etc.


## Installation

This has only been tested against `radicale>=3`, which is not yet packaged
for OpenBSD, so you must [install that version manually](#install-radicale-3-on-openbsd) (below) if it's not already.

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

### Install Radicale 3 on OpenBSD

(these have been tested for OpenBSD 7.7, but will need adjusting for a different version)

**If you are currently using version 2, you should backup your calendars before proceeding** because upgrading risks breaking something. It's unlikely, but possible.

```
doas -u _radicale tar -jcvf - /var/lib/radicale/collections | (umask 027; cat > radicale-collections.tgz) # for example
```

Then install radicale 3:

```
doas pkg_add python3
doas pip install --break-system-packages "radicale>=3"  # it's either --break-system-packages or making a venv and pointed /etc/rc.d/radicale at your venv

# Set up radicale's environment
# ( these rest of these steps would normally be handled by pkg_add(1) )
doas useradd -d /var/lib/radicale -m -L daemon -r 1..999 _radicale # if you don't already have this user
cat <<EOF | doas tee /etc/rc.d/radicale && doas chmod +x /etc/rc.d/radicale
#!/bin/ksh

daemon="/usr/local/bin/radicale"
daemon_user="_radicale"
rc_bg=YES

. /etc/rc.d/rc.subr

pexp="/usr/local/bin/python3.12 \${daemon}\${daemon_flags:+\${daemon_flags}}"
rc_reload=NO

rc_cmd \$1
EOF
doas rcctl enable radicale
doas rcctl start radicale
```


## Related Work

* [`radicale-auth-PAM`](https://pypi.org/project/radicale-auth-PAM/):

  OpenBSD's [authenticate(3)](https://man.openbsd.org/authenticate.3) is like
  Linux's [PAM(8)](https://man.archlinux.org/man/pam.8): a way to enable multiple
  ways to prove your identity, from passwords to LDAP to YubiKeys.

  So `radicale-auth-PAM` provides the same basic feature to `radicale`
  as `radicale-bsdauth`, and if you're using Linux you should use it.
