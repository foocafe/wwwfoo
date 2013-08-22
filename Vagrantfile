# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "debian-7-32-vanilla (virtualbox)"
  config.vm.box_url = "/Users/hakansvalin/Tools/Vagrants/boxes/debian-7.1-32-vanilla.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network :forwarded_port, guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "192.168.56.30"

  # On the first vagrant up command let this be commented out.
  # The NFS client software will be installed when the box is provisioned.
  # Uncomment on subsequent vagrant up:s
  config.vm.synced_folder "../wwwfoo", "/home/vagrant/host-share", :nfs => true

  config.vm.provider :virtualbox do |vb|

     # Use VBoxManage to customize the VM. For example to change memory:
      vb.customize ["modifyvm", :id, "--memory", "2048"]
      vb.customize ["modifyvm", :id, "--cpus", "4"]
      vb.customize ["modifyvm", :id, "--name", "Foo Vagrant 1.0"]
      vb.customize ["modifyvm", :id, "--cpuexecutioncap", "80"]
  end

  # Lets do some provisioning here
  config.vm.provision :shell, :path => "vagrant-support/setup.sh"
  config.vm.provision :shell, :path => "vagrant-support/configure.sh"

end
