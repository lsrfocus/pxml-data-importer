### Development

Setup:
- Requires python v2.7
- `pip install --user lxml neo4j`
- `(cd .neo4j/plugins/ && curl -LO https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.2/apoc-3.5.0.2-all.jar)`
- `docker-compose -f db.yml up -d palantir-import`
- Open <http://localhost:7474/browser/> to set your password (default is `neo4j`, python script expects `pwd`)

Import/export data:
- Uncomment the appropriate lines in `.neo4j/data/setup-neo4j.sh`
- `docker-compose -f db.yml restart palantir-import`
