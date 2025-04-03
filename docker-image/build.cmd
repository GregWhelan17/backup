docker build --secret=type=file,id=pipconf,src=./pip.conf --secret=type=file,id=aptconf,src=./secret.txt -t nexus3.systems.uk.hsbc:18080/hsbc-12437542-cpopen-turbonomic/dbbkupfull:0.2 .
docker push nexus3.systems.uk.hsbc:18080/hsbc-12437542-cpopen-turbonomic/dbbkupfull:0.2 




@REM docker build -t nexus3.systems.uk.hsbc:18080/hsbc-12437542-cpopen-turbonomic/dbbkupfull:0.2 .
@REM docker build --secret=type=file,id=pipconf,src=./pip.conf --secret=type=file,id=aptconf,src=./secret.txt -t nexus3.systems.uk.hsbc:18080/hsbc-12437542-cpopen-turbonomic/action:0.9 .
