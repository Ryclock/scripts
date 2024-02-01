FROM mongo:latest

COPY ./mongodb.conf /etc/mongod.conf
COPY ./init_mongodb.sh /root/script/init_mongodb.sh
COPY ./init_test_db.sh /root/script/init_test_db.sh

RUN chmod +x /root/script/init_mongodb.sh
CMD ["./root/script/init_mongodb.sh"]
