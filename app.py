import pandas as pd
import numpy as np
#from IPython.display import display
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
#pd.set_option("Display.max_colwidth",200)

users= pd.read_csv("Data/users.csv").rename(columns={"User-ID":"user-id","Name":"name","Location":"location","Country":"country","Age":"age"})
#display(users.head())
ratings = pd.read_csv("Data/ratings.csv").rename(columns={"User_ID":"user-id","Food_ID":"food-id","Rating":"rating"})
#display(ratings.head())
food = pd.read_csv("Data/food.csv").rename(columns={ "Food_ID":"food-id","Name":"name","C_Type":"type","Veg_Non":"veg-non","Describe":"describe"})
#display(food.head())
ratings_with_food = ratings.merge(food,on="food-id")
#display(ratings_with_food)

num_ratings = ratings_with_food.groupby("name")["rating"].count().reset_index()
num_ratings.rename(columns={
    'rating':'num of rating'
},inplace=True)
#display(num_ratings.head())

final_ratings = ratings_with_food.merge(num_ratings,on="name")
#display(final_ratings.head())

povit_food = final_ratings.pivot_table(columns="user-id",index="name",values="rating")
#display(povit_food.head())

povit_food.fillna(0,inplace=True)
#display(povit_food.head())

food_sparse = csr_matrix(povit_food)
#display(povit_food.head())

model = NearestNeighbors(algorithm="brute")
model.fit(food_sparse)


def recommemd_food(food_name):
    food_name = food_name.lower()
    suggestion_food_list = []
    try:
        food_id = np.where(povit_food.index == food_name)[0][0]
        destance,suggestion = model.kneighbors(povit_food.iloc[food_id,:].values.reshape(1,-1),n_neighbors=6)
        for i in range(len(suggestion)):
            suggestion_food = povit_food.index[suggestion[i]]
            for j in suggestion_food:
                if j == food_name:
                    continue
                else:             
                    suggestion_food_list.append(j)    
        return suggestion_food_list   
    except:
        return {"message":"No Data Recommanded"}     

def return_by_rating(food_rating):
    data = ratings_with_food[ratings_with_food["rating"] == food_rating]
    result = data["name"].values.tolist()
    return {"By Rating":result}
    
        
        
if __name__ =="__main__":
    print(recommemd_food("chicken dong style"))