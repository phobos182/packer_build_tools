require 'yarjuf'
require 'serverspec'

set :backend, :exec
set :path, '/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin:/usr/local/sbin'
set :host, 'localhost'
