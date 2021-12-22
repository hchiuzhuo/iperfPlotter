##!/bin/sh
# this shell script has been created
# to structure the lan test task for
# the project Period

# please be sure that you have allready installed iperf3
# https://iperf.fr/iperf-download.php
# see also -> https://iperf.fr/iperf-doc.php
#
# and iperfPlotter
# https://github.com/bosforox/iperfPlotter.git
echo "--------------------------------"
echo "| Period LAN Test (only Master) |"
echo "--------------------------------"
echo ""
echo "Did you set your IP adreses?"
echo "sudo ifconfig eth0 192.168.1.10 netmask 255.255.255.0 up"
echo ""
echo ""
echo "Please start iperf server on the SLAVE PC"
echo "iperf3 -s"
echo ""
echo "or route second LAN_Interface, if you use only a master pc"
echo ""
echo ""
echo ""
echo ""
echo "Please give the name of test object"
read NAME_OF_TEST_OBJECT

echo "The $NAME_OF_TEST_OBJECT is  getting tested"

# -find the IP of your first PC/LAN interface, which will used as server, use ifconfig
#IP_ADRESS_OF_SERVER=192.168.3.42
IP_ADRESS_OF_SERVER=192.168.1.1

VAR_T=1
#LIST_VAR_P="P1 P5 P10 P25 P50 P100"
LIST_VAR_P="P1 P5 P10 P25 P50"
LIST_VAR_M="Xm 1m 10m 100m 1000m 10000m 100000m"
#LIST_VAR_M="Xm 100m 1000m 10000m"


echo "Preset IP adress is $IP_ADRESS_OF_SERVER"
echo "Do you want to change the server IP address?(Y/N)"

read  DOIT
case $DOIT in
  y|Y|j|J) echo "what is the IP address of server?"; read IP_ADRESS_OF_SERVER;
esac

echo "Target IP of the server is $IP_ADRESS_OF_SERVER"

if ping -c 1 $IP_ADRESS_OF_SERVER
then
  echo "the given IP address $IP_ADRESS_OF_SERVER works"
else
  echo "the given IP aderess $IP_ADRESS_OF_SERVER is not reachable"
  echo "check the IP address restart the script again"
  exit 0;
fi

# start measurement on secon PC/LAN interface
iperf3 -c $IP_ADRESS_OF_SERVER  -p 5201 -fk -t 1?

echo "does iperf3 work properly? (y/n)"
read  DOIT
case $DOIT in
  n|N) echo "Try to test the conncetion to server manuelly and start the script again";exit 0;
esac

echo ""
#echo "removing old results"
#rm -rf testPeriod
#rm -rf graph
echo "creating empty folders"
#mkdir testPeriod
DATE_V=`date +%F_%H%M%S_` #$(date +%F_%H%M%S)
FOLDER_NAME=""
FOLDER_NAME+=$DATE_V
FOLDER_NAME+=$NAME_OF_TEST_OBJECT

mkdir $FOLDER_NAME
mkdir $FOLDER_NAME/data
mkdir $FOLDER_NAME/graph

for j in $LIST_VAR_P; do
  echo "$j"
  #M_VAL=$j
  mkdir $FOLDER_NAME/data/$j
  mkdir $FOLDER_NAME/graph/$j
done

echo "The folders are ready!"

echo ""
echo ""

echo ""
echo "Please enter the test duration in second (e.g.:10)"
read TEST_DURATION
echo ""

echo ""
echo "--------------------------"
echo "| >> Starting to test >> |"
echo "--------------------------"
echo ""
for i in $LIST_VAR_P; do
  #echo "$i"
  P_VAL=$i

  for j in $LIST_VAR_M; do
    #echo "$j"
    M_VAL=$j
    T_VAL="T0"$VAR_T
    TEST_NAME=$T_VAL"_"$P_VAL"_"$M_VAL"_t"$TEST_DURATION
    FILE_NAME=$NAME_OF_TEST_OBJECT"_"$TEST_NAME
    echo "Current Test:$TEST_NAME"

    case $j in
      Xm)
        iperf3 -c $IP_ADRESS_OF_SERVER -Z -i 1 -A 1 -t$TEST_DURATION -$P_VAL -J > ./$FOLDER_NAME/data/$P_VAL/$FILE_NAME;;
      *)
        iperf3 -c $IP_ADRESS_OF_SERVER -Z -i 1 -A 1 -b $M_VAL -t$TEST_DURATION -$P_VAL -J > ./$FOLDER_NAME/data/$P_VAL/$FILE_NAME;;
    esac
    echo "Done!"

  done
  VAR_T=$(($VAR_T + 1))
  echo ""
done
#-------------------------------

#iperf3 -c 192.168.3.42  -p 5201 -fk -t 5 -P 50
#iperf3 -c 192.168.3.42  -p 5201 -fk -t 5 -P 100
#iperf3 -c 192.168.3.42 -Z -i 1 -A 1 -t10 -P50 -P -J > ./testPeriod/T01_Parallel_Stream
#--
tree ./testPeriod/$FOLDER_NAME


for j in $LIST_VAR_P; do
  echo "$j"
  python3 iperf3_plot.py -f ./$FOLDER_NAME/data/$j -o $FOLDER_NAME/graph/$j/all.png
done



#python3 iperf3_plot.py -f ./testPeriod/$FOLDER_NAME/P5 -o graph/$FOLDER_NAME/P5/all.png
#python3 iperf3_plot.py -f ./testPeriod/$FOLDER_NAME/P10 -o graph/$FOLDER_NAME/P10/all.png
#python3 iperf3_plot.py -f ./testPeriod/$FOLDER_NAME/P25 -o graph/$FOLDER_NAME/P25/all.png
#python3 iperf3_plot.py -f ./testPeriod/$FOLDER_NAME/P50 -o graph/$FOLDER_NAME/P50/all.png
#python3 iperf3_plot.py -f ./testPeriod/$FOLDER_NAME/P100 -o graph/$FOLDER_NAME/P100/all.png
