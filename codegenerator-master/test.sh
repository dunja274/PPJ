correct=0
sum=0
for i in tests/*
do
    let sum=sum+1
	echo "#$sum: $i"
    python GeneratorKoda.py < $i/test.in
    timeout 20 node main.js a.frisc 2> /dev/null > $i/out

    dos2unix $i/test.out > /dev/null 2>&1
    dos2unix $i/out > /dev/null 2>&1

    res=`diff $i/test.out $i/out`
    rm $i/out

    if [ "$res" != "" ]
	then
        echo "FAIL"
        echo $res
	else
		let correct=correct+1
    	echo "OK"
    fi
done
echo "$correct/$sum"
