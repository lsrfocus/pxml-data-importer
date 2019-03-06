### Development

Requirements:
- Python v2.7
- Docker (with docker-compose)

Setup:
- Install libs: `pip install --user lxml neo4j`
- Download Neo4j plugins: `(cd .neo4j/plugins/ && curl -LO https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.2/apoc-3.5.0.2-all.jar)`
- Create the database: `docker-compose -f db.yml up -d palantir-import`
- Open <http://localhost:7474/browser/> to set your password (default is `neo4j`, python script expects `pwd`)

Usage:
- Update `files = ...` to point to the files you want to import
- Run `python example.py`

Import/export data:
- Uncomment the appropriate lines in `.neo4j/data/setup-neo4j.sh`
- Restart the database: `docker-compose -f db.yml restart palantir-import`
