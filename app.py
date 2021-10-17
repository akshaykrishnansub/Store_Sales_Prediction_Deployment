from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)
client_model = pickle.load(open('models/rf_model.pkl','rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index_1.html')

 
@app.route("/predict",methods=['POST'])
def predict():
    if request.method == 'POST':
        Outlet_Establishment_Year=int(request.form['Outlet_Establishment_Year'])
        Outlet_Years_Op=2021-Outlet_Establishment_Year
        Item_Weight=float(request.form['Item_Weight'])
        Item_Visibility=float(request.form['Item_Visibility'])
        Item_MRP=float(request.form['Item_MRP'])
        Outlet_Size=request.form['Outlet_Size']
        if(Outlet_Size=='High'):
            Outlet_Size=0
        elif(Outlet_Size=='Medium'):
            Outlet_Size=1
        else:
            Outlet_Size=2
        Outlet_Location_Type=request.form['Outlet_Location_Type']
        if(Outlet_Location_Type=='Tier1'):
            Outlet_Location_Type=0
        elif(Outlet_Location_Type=='Tier2'):
            Outlet_Location_Type=1
        else:
            Outlet_Location_Type=2
        Outlet_Type_Supermarket_Type1=request.form['Outlet_Type_Supermarket_Type1']
        if(Outlet_Type_Supermarket_Type1=='Supermarket Type1'):
            Outlet_Type_Supermarket_Type1=1
            Outlet_Type_Supermarket_Type2=0
            Outlet_Type_Supermarket_Type3=0
            Outlet_Type_Grocery_Store=0
        elif(Outlet_Type_Supermarket_Type1=='Supermarket Type2'):
            Outlet_Type_Supermarket_Type1=0
            Outlet_Type_Supermarket_Type2=1
            Outlet_Type_Supermarket_Type3=0
            Outlet_Type_Grocery_Store=0
        elif(Outlet_Type_Supermarket_Type1=='Supermarket Type3'):
            Outlet_Type_Supermarket_Type1=0
            Outlet_Type_Supermarket_Type2=0
            Outlet_Type_Supermarket_Type3=1
            Outlet_Type_Grocery_Store=0
        else:
            Outlet_Type_Supermarket_Type1=0
            Outlet_Type_Supermarket_Type2=0
            Outlet_Type_Supermarket_Type3=0
            Outlet_Type_Grocery_Store=1
        Item_Fat_Content_Regular=request.form['Item_Fat_Content_Regular']
        if(Item_Fat_Content_Regular=='Regular'):
            Item_Fat_Content_Regular=1
            Item_Fat_Content_Low_Fat=0
            Item_Fat_Content_Non_Edible=0
        elif(Item_Fat_Content_Regular=='Low Fat'):
            Item_Fat_Content_Regular=0
            Item_Fat_Content_Low_Fat=1
            Item_Fat_Content_Non_Edible=0
        else:
            Item_Fat_Content_Regular=0
            Item_Fat_Content_Low_Fat=0
            Item_Fat_Content_Non_Edible=1
        Item_Type_New_Perishable=request.form['Item_Type_New_Perishable']
        if(Item_Type_New_Perishable=='Perishable'):
            Item_Type_New_Perishable=1
            Item_Type_New_Non_Perishable=0
            Item_Type_New_Not_Sure=0
        elif(Item_Type_New_Perishable=='Non Perishable'):
            Item_Type_New_Perishable=0
            Item_Type_New_Non_Perishable=1
            Item_Type_New_Not_Sure=0
        else:
            Item_Type_New_Perishable=0
            Item_Type_New_Non_Perishable=0
            Item_Type_New_Not_Sure=1      
        Item_Category_Food=request.form['Item_Category_Food']
        if(Item_Category_Food=='Food'):
            Item_Category_Food=1
            Item_Category_Drinks=0
            Item_Category_Non_Consumable=0
        elif(Item_Category_Food=='Drinks'):
            Item_Category_Food=0
            Item_Category_Drinks=1
            Item_Category_Non_Consumable=0
        else:
            Item_Category_Food=0
            Item_Category_Drinks=0
            Item_Category_Non_Consumable=1
        
        if Item_Weight==0 or Item_Visibility==0 or Item_MRP==0:
            return render_template('index_1.html',prediction_texts= "Please enter valid values as required to properly predict the sales")
            
        price_per_unit_wt=Item_MRP/Item_Weight
        
        if Item_MRP<69:
            Item_MRP_Clusters=1
        elif Item_MRP>=69 and Item_MRP<136:
            Item_MRP_Clusters=2
        elif Item_MRP>=136 and Item_MRP<203:
            Item_MRP_Clusters=3
        else:
            Item_MRP_Clusters=4

        prediction=client_model.predict([[Item_MRP, Item_Visibility, Item_Weight, Outlet_Location_Type, Outlet_Size, Outlet_Years_Op, price_per_unit_wt, Item_MRP_Clusters, Item_Fat_Content_Non_Edible, Item_Fat_Content_Regular, Item_Type_New_Perishable, Item_Category_Drinks, Item_Category_Food, Outlet_Type_Grocery_Store, Outlet_Type_Supermarket_Type1, Outlet_Type_Supermarket_Type2, Outlet_Type_Supermarket_Type3, Item_Type_New_Non_Perishable, Item_Type_New_Not_Sure, Item_Fat_Content_Low_Fat, Item_Category_Non_Consumable]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index_1.html',prediction_texts= "Sorry sales cannot be predicted")
        else:
            return render_template('index_1.html',prediction_text= "Expected sales is {}".format(output))
    else:
        return render_template('index_1.html')
            

if __name__ == "__main__":
    app.run(debug=True)

    

