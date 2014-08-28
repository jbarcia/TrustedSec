# /bin/bash

page=http://www.offsec.com/pwbonline/icq.html
site=icq.com
#hosts=icq
#ips=$output


echo "Enter the page to scan: "
echo Ex. [$page]
read -p ""
page="$REPLY"

echo "Enter the sitename: "
echo Ex. [$site]
read -p ""
site="$REPLY" 


mkdir $site
cd $site

wget $page -O ~/$site/$site.txt -o /dev/null
grep 'href=' $site.txt | cut -d"/" -f3 |grep $site |sort -u > ~/$site/$site-servers.txt

for hostname in $(cat ~/$site/$site-servers.txt);do
host $hostname |grep "has address" >> ~/$site/$site-temp.txt
done

cat ~/$site/$site-temp.txt |cut -d" " -f4 |sort -u > ~/$site/$site-ips.txt

rm $site-temp.txt
rm $site.txt

echo ========================================== >> ~/$site/$site.txt
echo Host Names >> ~/$site/$site.txt
echo ========================================== >> ~/$site/$site.txt
cat ~/$site/$site-servers.txt >> ~/$site/$site.txt
echo ========================================== >> ~/$site/$site.txt
echo IPs >> ~/$site/$site.txt
echo ========================================== >> ~/$site/$site.txt
cat ~/$site/$site-ips.txt >> ~/$site/$site.txt

cat ~/$site/$site.txt
