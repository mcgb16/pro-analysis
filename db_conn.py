from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

top5_collection = conn[ext.top5_collection]
all_pl_score_collection = conn[ext.all_pl_score_collection]

def create_top5(top5_list):
    try:
        top5_insert = top5_collection.insert_many(top5_list)
        return top5_insert
    except Exception as e:
        print(e)
        return e

def create_player_record(pl_list):
    try:
        player_insert = all_pl_score_collection.insert_many(pl_list)
        return player_insert
    except Exception as e:
        print(e)
        return e

def update_player_record(pl_list):
    for pl in pl_list:
        try:
            upd_filter = {"playername" : pl["playername"]}
            update_info = {
                "$inc" : {"total_score" : pl["total_score"]},
                "$push" : {"date": pl["date"]}
                }
            player_update = all_pl_score_collection.update_one(upd_filter, update_info)
        except Exception as e:
            print(e)
            return e
        
    return True