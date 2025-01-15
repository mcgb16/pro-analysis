from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

top5_collection = conn[ext.top5_collection]
all_pl_score_collection = conn[ext.all_pl_score_collection]
week_pl_score_collection = conn[ext.week_pl_score_collection]
all_team_score_collection = conn[ext.all_team_score_collection]
week_team_score_collection = conn[ext.week_team_score_collection]
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

def create_player_record(pl_list):
    try:
        for pl in pl_list:
            filter_condition = {
                "playername": pl["playername"],
                "split" : pl["split"],
                "playoffs" : pl["playoffs"]
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
                "split": pl["split"],
                "playoffs": pl["playoffs"]
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
    
def create_week_player_record(pl_list):
    try:
        for pl in pl_list:
            filter_condition = {
                "playername": pl["playername"],
                "split" : pl["split"],
                "week" : pl["week"]
                }

            upsert_pl = {
                "$setOnInsert": pl
            }
            
            week_pl_score_collection.update_one(filter_condition, upsert_pl, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e
    
def update_week_player_record(pl_list):
    for pl in pl_list:
        try:
            upd_filter = {
                "playername" : pl["playername"],
                "date": {"$ne": pl["date"]},
                "split": pl["split"],
                "week" : pl["week"]
                }
            update_info = {
                "$inc" : {"total_score" : pl["total_score"]},
                "$push" : {"date": pl["date"]}
                }
            player_update = week_pl_score_collection.update_one(upd_filter, update_info)
        except Exception as e:
            print(e)
            return e
    if str(player_update) == "UpdateResult({'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}, acknowledged=True)":
        return False
    else:
        return True

def get_stage_player(split, playoff):
    search_filter = {
        "split": split,
        "playoffs": playoff,
    }

    results = all_pl_score_collection.find(search_filter)

    return results

def get_player(split):
    search_filter = {
        "split": split
    }

    results = all_pl_score_collection.find(search_filter)

    return results

def get_week_player(split, week):
    search_filter = {
        "split": split,
        "week": week,
    }

    results = week_pl_score_collection.find(search_filter)

    return results

def get_top5(split, playoff):
    search_filter = {
        "split": split,
        "playoffs": playoff,
    }

    results = top5_collection.find(search_filter)

    return results

def create_week_team_record(team_list):
    try:
        for t in team_list:
            filter_condition = {
                "teamname": t["teamname"],
                "split" : t["split"],
                "week" : t["week"]
                }

            upsert_team = {
                "$setOnInsert": t
            }
            
            week_team_score_collection.update_one(filter_condition, upsert_team, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e

def update_week_team_record(team_list):
    for t in team_list:
        try:
            upd_filter = {
                "teamname" : t["teamname"],
                "date": {"$ne": t["date"]},
                "split": t["split"],
                "week": t["week"]
                }
            update_info = {
                "$inc" : {"total_score" : t["total_score"]},
                "$push" : {"date": t["date"]}
                }
            
            team_update = all_team_score_collection.update_one(upd_filter, update_info)
        except Exception as e:
            print(e)
            return e
    if str(team_update) == "UpdateResult({'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}, acknowledged=True)":
        return False
    else:
        return True

def create_team_record(team_list):
    try:
        for t in team_list:
            filter_condition = {
                "teamname": t["teamname"],
                "split" : t["split"],
                "playoffs" : t["playoffs"]
                }

            upsert_team = {
                "$setOnInsert": t
            }
            
            all_team_score_collection.update_one(filter_condition, upsert_team, upsert=True)
        
        return True
    except Exception as e:
        print(e)
        return e

def update_team_record(team_list):
    for t in team_list:
        try:
            upd_filter = {
                "teamname" : t["teamname"],
                "date": {"$ne": t["date"]},
                "split": t["split"],
                "playoffs": t["playoffs"]
                }
            update_info = {
                "$inc" : {"total_score" : t["total_score"]},
                "$push" : {"date": t["date"]}
                }
            
            team_update = all_team_score_collection.update_one(upd_filter, update_info)
        except Exception as e:
            print(e)
            return e
    if str(team_update) == "UpdateResult({'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}, acknowledged=True)":
        return False
    else:
        return True

def get_team(split):
    search_filter = {
        "split": split
    }

    results = all_team_score_collection.find(search_filter)

    return results

def get_stage_team(split, playoffs):
    search_filter = {
        "split": split,
        "playoffs": playoffs
    }

    results = all_team_score_collection.find(search_filter)

    return results

def get_week_team(split, week):
    search_filter = {
        "split": split,
        "week": week
    }

    results = week_team_score_collection.find(search_filter)

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