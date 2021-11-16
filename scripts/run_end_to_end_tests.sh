flask run --host=127.0.0.1 --port=5000 &
pid[0]=$!
npx cypress run 
kill ${pid[0]}