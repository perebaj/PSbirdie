# PSbirdie



# Build docker
docker-compose build 
# *Subindo mensagens para o aws SQS
docker-compose up --scale product-worker=0 --scale publisher=1 --scale review-worker=0
# *Setando 10 reviews-workers
docker-compose up --scale product-worker=0 --scale publisher=0 --scale review-worker=10

