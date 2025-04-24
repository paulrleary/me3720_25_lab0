# sudo apt install python3-pip
pip3 install --upgrade setuptools wheel
# git clone https://github.com/osvenskan/posix_ipc.git
cd posix_ipc
python3 -m pip install .
 
cd ..
 
# USER="{REPLACE WITH GITHUB USER NAME}"
# GROUP_NAME="byu-holoocean"
# REPO_NAME="HoloOcean"
# BRANCH="develop"
# PAT="{REPLACE WITH PERSONAL ACCESS TOKEN}"
 
# git clone -b $BRANCH https://$USER:$PAT@github.com/$GROUP_NAME/$REPO_NAME.git
 
# cd $REPO_NAME/client
# pip install .
# cd ../..

cd HoloOcean
git checkout develop
cd client

pip install .

cd ../..
 
# python -c `import holoocean; holoocean.install("Ocean")`
python -c 'import holoocean; holoocean.install("Ocean", branch="develop")'