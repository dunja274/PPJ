correct=0
for i in {0..19}
do
	echo "Test $i"
    python GSA.py < tests/test$i.san
    python analizator/SA.py < tests/test$i.in > tests/$i.out
    
    dos2unix tests/test$i.out > /dev/null 2>&1
    dos2unix tests/$i.out > /dev/null 2>&1
    res=`diff tests/test$i.out tests/$i.out`
    rm tests/$i.out

    if [ "$res" != "" ]
	then
        echo "FAIL"
        echo $res
	else
		let correct=correct+1
    	echo "OK"  
    fi
done
echo "$correct/20"
