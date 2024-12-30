from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

top5_collection = conn[ext.top5_collection]
all_pl_score_collection = conn[ext.all_pl_score_collection]

def create_top5(top5_list):
    try:
        for top5 in top5_list:
            filter_condition = {"date": top5["date"]}

            upsert_top5 = {
                "$setOnInsert": top5
            }
            
            top5_collection.update_one(filter_condition, upsert_top5, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e

def create_player_record(pl_list):
    try:
        for pl in pl_list:
            filter_condition = {
                "playername": pl["playername"],
                "split" : pl["split"]
                }

            upsert_pl = {
                "$setOnInsert": pl
            }
            
            all_pl_score_collection.update_one(filter_condition, upsert_pl, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e

def update_player_record(pl_list):
    for pl in pl_list:
        try:
            upd_filter = {
                "playername" : pl["playername"],
                "date": {"$ne": pl["date"]},
                "split": pl["split"]
                }
            update_info = {
                "$inc" : {"total_score" : pl["total_score"]},
                "$push" : {"date": pl["date"]}
                }
            player_update = all_pl_score_collection.update_one(upd_filter, update_info)
        except Exception as e:
            print(e)
            return e
    if str(player_update) == "UpdateResult({'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}, acknowledged=True)":
        return False
    else:
        return True