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

# Auth file

請參考 flickr_api 的文件

# Usage

    $ python qclickr.py [dir path or photo path]
