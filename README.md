# Japanese

This is an ongoing project to assist me in learning Japanese.

Based on the Genki series of textbooks, these exercises will take the
user through basic Japanese.

It is also a guide for me to work through the difficulties of English natural
language processing.

This is very much a work in progress. As such, the directories are complete
spaghetti and are NOT to be considered anywhere near a master work.


## Set Up

```
pip3 install virtualenv
cd /path/to/this/directory
virtualenv venv
source venv/bin/activate
```

Optionally, one can use virtualenvwrapper as well
```
pip install virtualenvwrapper
echo 'export WORKON_HOME=~Envs' >> ~/.bashrc
echo 'export WORKON_HOME=~Envs' >> ~/.zshrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.zshrc
source ~/.bashrc  # or zshrc
mkproject japanese
git clone git@github.com:PentheusLennuye/japanese.git
```

Install the software
```
yum groupinstall 'Development Tools'
yum install gcc-c++ gtk2-devel gtk3-devel python3-devel
pip install -r requirements.txt
```

## Use

With VirtualEnv
```
cd /path/to/this/directory
virtualenv venv
<do stuff>
deactivate
```

With VirtualEnvWrapper
```
workon japanese
<do stuff>
deactivate
```
