## Dublin Bus Data Pipeline - Consumer

### What does this project do?

 * Using the modules created in [here]('https://gitlab.scss.tcd.ie/panthb/Dublin-Transport_RPP'), the project establishes a pipeline to pull messages from the queue (RabbitMQ)

#### RabbitMQ specifics
 * ```sudo rabbitmq-server start```
 * [RabbitMQ dashboard access]('https://developers.coveo.com/display/public/SitecoreV3/Accessing+the+RabbitMQ+Management+Console;jsessionid=548855A4C0EC0A72DA10CA8E400B124F')
 * Pre-req [here]('https://www.rabbitmq.com/management.html')

#### Elastic Search
 * Install Elastic Search for Ubuntu - [here]('https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-16-04')
 * ```sudo systemctl enable elasticsearch.service``` to start Elastic Search service

#### Run the project
 * ```sudo rabbitmq-server start```
 * ```sudo systemctl enable elasticsearch.service```
 * ```sudo service elasticsearch start``` - you can also run Elastic Search on start by using ```sudo update-rc.d elasticsearch defaults 95 10``` Taken from tutorial [here]('https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-elk-stack-on-ubuntu-14-04')
 * ```python main.py --flag=bus --host=localhost```

#### RabbitMQ Docker
 * Image available [here]('https://docs.docker.com/samples/library/rabbitmq/')

#### Next steps
 * Docker build this project into an image
 * Docker build container for RabbitMQ
 * Docker build containers for Elastic Search
 * Utilize GitLab CI 
 * Utilize Travis for CI - Write test cases