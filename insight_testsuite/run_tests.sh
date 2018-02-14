python ../src/donation-analytics.py ./tests/test_1/input/itcont.txt ./tests/test_1/input/percentile.txt ./tests/test_1/output/test_repeat_donors.txt
if [ ! -z "$(diff ./tests/test_1/output/repeat_donors.txt ./tests/test_1/output/test_repeat_donors.txt)" ]; then
	echo "0 of 1 tests passed"
else
	echo "1 of 1 tests passed"
fi
	
