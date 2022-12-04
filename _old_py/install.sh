if [[ $(pwd) != *backend-gm ]]
then
	echo "wrong workplace"
	exit 0
fi
root=$(pwd)

sudo apt install python3-pip

# html
python3 -m pip install pygments

if [[ -d src_cache ]]
then
	rm -rf src_cache
fi
mkdir src_cache

# python3 -m pip install -e .