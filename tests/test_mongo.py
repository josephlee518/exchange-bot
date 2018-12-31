import unittest
from machine.db.MongoDB import MongoDB

class MongoDBHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.Mongodb = MongoDB.MongoDB()
        self.Mongodb.delete_items({})
        docs = [
            {"currency":"btc", "price":10000},
            {"currency":"eth", "price":1000},
            {"currency":"xrp", "price":100},
            {"currency":"btc", "price":20000}
        ]
        self.Mongodb.insert_items(docs)

    def tearDown(self):
        pass

    def test_get_one_item(self):
        """데이터 하나 집어넣기"""
        returned = self.Mongodb.find_item({"currency":"btc"})
        assert returned

    def test_find_items(self):
        """데이터 찾기"""
        returned = self.Mongodb.find_items({"currency":"eth"})
        for a in returned:
            print(a)
        assert returned

    def test_update_items(self):
        """아이템 업데이트하기"""
        result = self.Mongodb.update_items({"currency":"xrp"}, {"$set":{"price":300}})
        assert result 
        print("matched_count: "+str(result.matched_count))
        print("modified_count: "+str(result.modified_count))

    def test_aggregate_items(self):
        """집계연산"""
        pipeline = [
            {"$match":{"currency":"btc"}},
            {"$group":{"_id":"$currency",
            "min_val":{"$min":"$price"},
            "max_val":{"$max":"$price"},
            "sum_val":{"$sum":"$price"}}
            }
        ]
        result = self.Mongodb.aggregate(pipeline=pipeline)
        assert result
        for item in result:
            print(item)

    def test_delete_many(self):
        """모두 삭제하기"""
        deleted = self.Mongodb.delete_items({"currency":"xrp"})
        assert deleted
        print(deleted.deleted_count)
    
if __name__ == "__main__":
    unittest.main()