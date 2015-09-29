require 'spec_helper'

describe service("ssh") do
  it { should be_running }
end

