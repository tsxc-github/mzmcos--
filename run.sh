git clone https://github.com/Light-Beacon/HomepageBuilder
pip install ./HomepageBuilder
pip install -r ./requirements.txt
python ./script.py

git config user.email "tsxc_personal@163.com"
git config user.name "星澜曦光"
git add output.xaml -f
git commit -m "更新output.xaml"