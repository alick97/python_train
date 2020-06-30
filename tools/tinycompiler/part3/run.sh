PYTHON="python3"
COMPILER="tiny.py"
CC="gcc"
for i in $(ls ../examples/*.tiny); do
	BN=$(basename -s .tiny ${i})
	TTOUTPUT=$(${PYTHON} ${COMPILER} ${i} 2>&1)
	if [ $? -ne 0 ]; then
		echo "Error compiling $i: ${TTOUTPUT}"
	else
		mv out.c ${BN}.c
		CCOUTPUT=$(${CC} -o ${BN} ${BN}.c)
		if [ $? -ne 0 ]; then
			echo "Error compiling C output for $i: ${CCOUTPUT}"
		else
			echo "TINY $i"
		fi
	fi
done
