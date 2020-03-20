## Stockmarket Data

### Download Collections: 

http://cs.msutexas.edu/~griffin/stockgame.stock_info.json

http://cs.msutexas.edu/~griffin/stockgame.stock_data_3yr.json

Using Command Line:
```
wget http://cs.msutexas.edu/~griffin/stockgame.stock_info.json
wget http://cs.msutexas.edu/~griffin/stockgame.stock_data_3yr.json
```

Or use your browser and `save as` :( 


### Import into Mongo

**Import Command:**
```bash
mongoimport -d <DatabaseName> -c <CollectionName> --type <FileType> --file <PathToFIle>
```

**Examples:**
```bash
mongoimport -d stockgame -c stock_info --type json --file stockgame.stock_info.json
```

```bash
mongoimport -d stockgame -c stock_data --type json --file stockgame.stock_data_3yr.json
```

