# OpenBSD Authentication plugin for Radicale

This connects a [radicale](https://radicale.org/) install to the local
OpenBSD's [authenticate(3)](https://man.openbsd.org/authenticate.3) system
that it is installed on. It means you can access your calendars with the
same password you use for ssh and, perhaps, email, chat, etc.


## Installation

This has only been tested against `radicale>=3`, which is not yet packaged
for OpenBSD, so you **must [install that version manually](#install-radicale-3-on-openbsd)** (below) if it's not already.

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

And restart:

```
doas rcctl restart radicale
```

### Install Radicale 3 on OpenBSD

**If you are currently using version 2, you should backup your calendars before proceeding** because upgrading risks breaking something. It's unlikely, but possible.

```
doas -u _radicale tar -jcvf - /var/lib/radicale/collections | (umask 027; cat > radicale-collections.tgz) # for example
```

Then install radicale 3:

```
doas pkg_add python3 py3-pip
doas pip install "radicale>=3"

# Set up radicale's environment
# ( these rest of these steps would normally be handled by pkg_add(1) )
doas useradd -d /var/lib/radicale -m -L daemon -r 1..999 _radicale # if you don't already have this user
```

You need to put this in `/etc/rc.d/radicale`:

```
daemon="/usr/local/bin/radicale"
daemon_user="_radicale"
daemon_logger="daemon.info"

. /etc/rc.d/rc.subr

pexp="/usr/local/bin/python3.12 ${daemon}${daemon_flags:+ ${daemon_flags}}"
rc_reload=NO

rc_start() {
  # radicale doesn't self-daemonize so add &
  rc_exec "${daemon} ${daemon_flags}" &
}

rc_cmd $1
```

and

```
doas chmod +x /etc/rc.d/radicale
```

Finally turn it on:

```
doas rcctl enable radicale
doas rcctl start radicale
```

You can monitor it with:

```
tail -f /var/log/daemon | grep radicale
```


## Related Work

* [`radicale-auth-PAM`](https://pypi.org/project/radicale-auth-PAM/):

  OpenBSD's [authenticate(3)](https://man.openbsd.org/authenticate.3) is like
  Linux's [PAM(8)](https://man.archlinux.org/man/pam.8): a way to enable multiple
  ways to prove your identity, from passwords to LDAP to YubiKeys.

  So `radicale-auth-PAM` provides the same basic feature to `radicale`
  as `radicale-bsdauth`, and if you're using Linux you should use it.
