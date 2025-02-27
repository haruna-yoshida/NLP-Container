pip install --upgrade pip --user
# init install python packages
pip install -r requirements.txt --user

# setup japanease font
wget https://moji.or.jp/wp-content/ipafont/IPAexfont/ipaexg00401.zip --no-check-certificate
unzip ipaexg00401.zip "*.ttf"
mv ipaexg00401/ipaexg.ttf /workspace/.pip-modules/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
rm -r ipaexg00401
rm ipaexg00401.zip
sed -i -e 's/#font.family:  sans-serif/font.family : IPAexGothic/g' /workspace/.pip-modules/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc

# setup import csv (google spread sheet)

# Download csv file
sh update_csv_data.sh

#install magnitude
if [ ! -e "chive-1.2-mc5.magnitude" ];then
    wget https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc5.magnitude --no-check-certificate
fi