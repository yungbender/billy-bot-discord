docker exec -it billy-db bash -c "psql billy-db -c \"`cat $1`\""
