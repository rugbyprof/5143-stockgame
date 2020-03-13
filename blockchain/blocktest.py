import hashlib
import json

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

class BlockChain(object):
    def __init__(self):
        self.blocks = {}
        self.keys = ['prev_hash','hash','transactions','timestamp','sender','receiver']
        self.index = 0

    def __str__(self):
        string = ""
        for key,block in self.blocks.items():
            string = str(block)
        return string
    
    def _validate_block(self,data):
        """Check to make sure all keys in data.
        """
        pass
    
    def _serialize_block_hash(self,block):
        block_serialized = json.dumps(block, sort_keys=True).encode("utf-8")
        block_hash = hashlib.sha256(block_serialized).hexdigest()
        return block_hash

    def _get_previous_hash(self,index):
        if self.index == 0:
            return self._serialize_block_hash({'genesis':'start_block'})
        else:
            return blocks[self.index]['prev_hash']

    def add_block(self,data):
        
        if is_json(str(data)):
            jsondata = json.loads(str(data))
            print(jsondata)
            self.blocks[self.index] = {}
            self.blocks[self.index]['data'] = jsondata
            self.blocks[self.index]['prev_hash'] = self._get_previous_hash(self.index)
            self.blocks[self.index]['hash'] = self._serialize_block_hash(jsondata)
            print(self.blocks[self.index])
            self.index += 1
        else:
            return False




if __name__=='__main__':
    B = BlockChain()
    B.add_block({"test":[1,2,3,4]})
    print(B)
    print(json.loads({"test":[1,2,3,4]}))



