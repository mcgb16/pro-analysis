from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

top10_collection = conn[ext.top10_collection]
player_info_collection = conn[ext.player_info_collection]

def create_top10(top10_list):
    try:
        for top10 in top10_list:
            filter_condition = {
                "round": top10["round"],
                "sector": top10["sector"],
                "rank": top10["rank"]
                }

            upsert_top10 = {
                "$setOnInsert": top10
            }
            
            top10_collection.update_one(filter_condition, upsert_top10, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e

def get_top10(split):
    search_filter = {
        "split": split
    }

    results = top10_collection.find(search_filter)

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
    
def get_info_player(split):
    search_filter = {
        "split": split
    }

    results = player_info_collection.find(search_filter)

    return results