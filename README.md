QCLickr
----
Just a simple script for me to upload my photos to Flickrs

# Setup

    $ pip install -r ./requirements.txt -t ./lib/

## Note

If you use Homebrew's python and pip, you may encounter an issue like this:

    DistutilsOptionError: must supply either home or prefix/exec-prefix -- not both

[Here](https://github.com/Homebrew/brew/blob/master/docs/Homebrew-and-Python.md) is the reason, and please use the script `./setup_env_with_homebrew.sh` to setup the environment.

    $ ./setup_env_with_homebrew.sh

# First time use

## Config file
When first time use QCLickr, just use

    $ python qclickr.py

It will show information about how to create a config file `_config.py`.

## Auth file
After config file created, use the command again

    $ python qclickr.py 

It will open browser and asking you permission for uploading photo to Flickr. After getting permission, QCLickr will save auth in local via flickr_api. Now you can start to upload your photo to Flickr.

# Usage

    $ python qclickr.py [dir path or photo path]
