## Dublin Bus Data Pipeline - Consumer

### What does this project do?
 * Using the modules created in [here]('https://gitlab.scss.tcd.ie/panthb/Dublin-Transport_RPP'), the project establishes a pipeline to pull messages from the queue (RabbitMQ)
 * Runs classification and regression on the stream data
 * Trying to build an ensemble of multiple classification algorithms

#### RabbitMQ specifics
 * ```sudo rabbitmq-server start```
 * [RabbitMQ dashboard access]('https://developers.coveo.com/display/public/SitecoreV3/Accessing+the+RabbitMQ+Management+Console;jsessionid=548855A4C0EC0A72DA10CA8E400B124F')
 * Pre-req [here]('https://www.rabbitmq.com/management.html')

#### Elastic Search
 * Install Elastic Search for Ubuntu - [here]('https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-16-04')
 * ```sudo systemctl enable elasticsearch.service``` to start Elastic Search service

#### Run the project
If you want to use RabbitMQ for the pipelines
 * ```sudo rabbitmq-server start```
 * ```python main.py --flag=bus --host=localhost```

 If you want to use Kafka
 * Start the Kafka instance
 * Make the change - replace all dataframe instances to ConsumerKafka instances 
 * `python main.py --flag=bus --host=localhost`

#### RabbitMQ Docker
 * Image available [here]('https://docs.docker.com/samples/library/rabbitmq/')

#### Next steps
 * Docker build this project into an image
 * Docker build container for RabbitMQ
 * Docker build containers for Elastic Search
 * Utilize GitLab CI 
 * Utilize Travis for CI - Write test cases