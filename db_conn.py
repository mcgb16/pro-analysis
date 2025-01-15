from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

top5_collection = conn[ext.top5_collection]
player_info_collection = conn[ext.player_info_collection]

def create_top5(top5_list):
    try:
        for top5 in top5_list:
            filter_condition = {
                "date": top5["date"],
                "sector": top5["sector"]
                }

            upsert_top5 = {
                "$setOnInsert": top5
            }
            
            top5_collection.update_one(filter_condition, upsert_top5, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e

def get_top5(split, playoff):
    search_filter = {
        "split": split,
        "playoffs": playoff,
    }

    results = top5_collection.find(search_filter)

    return results

def create_info_player_record(pl_list):
    try:
        for pl in pl_list:
            filter_condition = {
                "date": pl["date"],
                "playername": pl["playername"]
                }

            upsert_pl = {
                "$setOnInsert": pl
            }
            
            player_info_collection.update_one(filter_condition, upsert_pl, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e
    
def get_info_player(split, playoffs):
    search_filter = {
        "split": split,
        "playoffs": playoffs
    }

    results = player_info_collection.find(search_filter)

    return results