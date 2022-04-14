# configures a new web server to set up remote data directores
# for test and releases

exec { 'apt-get update':
  command => '/usr/bin/apt-get update',
}

exec { 'install nginx':
  command => '/usr/bin/apt-get install -y --no-upgrade nginx',
  require => Exec['apt-get update'],
}

exec { 'allow traffic':
  command => "/usr/sbin/ufw allow 'Nginx HTTP'",
  require => Exec['install nginx'],
}

exec { 'enable firewall':
  command => '/usr/sbin/ufw enable',
  require => Exec['allow traffic'],
}

exec { 'start nginx':
  command => '/usr/sbin/service nginx start',
  require => Exec['install nginx'],
}

file { 'data directory':
  path   => '/data',
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { 'web_static directory':
  path    => '/data/web_static',
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['data directory'],
}

file { 'releases directory':
  path    => '/data/web_static/releases',
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['web_static directory'],
}

file { 'shared directory':
  path    => '/data/web_static/shared/',
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['web_static directory'],
}

file { 'test directory':
  path   => '/data/web_static/releases/test/',
  ensure => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['releases directory'],
}

file { 'create a test index.html':
  path    => '/data/web_static/releases/test/index.html',
  ensure  => 'file',
  content => '<h1>testing nginx...</h1>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['test directory'],
}

file { 'current symlink':
  path    => '/data/web_static/current',
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  require => File['test directory'],
}

exec { 'new endpoint':
  command => '/usr/bin/sed -i -r "s|^(\s*)(location / \{)|\1location /hbnb_static {\n\1\1alias /data/web_static/current;\n\1\}\n\n\1\2|" /etc/nginx/sites-available/default',
  require => File['current symlink'],
}

exec { 'restart nginx':
  command => '/usr/sbin/service nginx restart',
}
