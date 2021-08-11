# init install python packages
pip install -r requirements.txt

# setup japanease font
wget https://moji.or.jp/wp-content/ipafont/IPAexfont/ipaexg00401.zip --no-check-certificate
unzip ipaexg00401.zip "*.ttf"
mv ipaexg00401/ipaexg.ttf /workspace/.pip-modules/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
rm -r ipaexg00401
sed -i -e 's/#font.family:  sans-serif/font.family : IPAexGothic/g' /workspace/.pip-modules/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc
rm -r ~/.cache/matplotlib