python ../src/donation-analytics.py ./tests/test_1/input/itcont.txt ./tests/test_1/input/percentile.txt ./tests/test_1/output/test_repeat_donors.txt
if [ ! -z "$(diff repeat_donors.txt test_repeat_donors.txt)" ]; then
	echo "TEST FAILED"
else
	echo "TEST PASSED"
fi
	
