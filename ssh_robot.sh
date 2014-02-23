ip=$(wget robot.usr.sh/get -q -O -)
echo "SSH'ing to $ip"
ssh pi@$ip
