# stop and remove container
docker container stop buildapcwatcher
docker container rm buildapcwatcher

#!/bin/bash
docker build -t buildapcwatcher .
# include -it  --rm to run interactively
docker run -d --name buildapcwatcher buildapcwatcher

