from sys import argv

class Product:
  def __init__(self, product, category, originalPrice, discount):
    self.product = product
    self.category = category
    self.originalPrice = originalPrice
    self.discount = discount

class CartItem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
       

def main():
    # Sample code to read inputs from the file
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    lines = f.readlines()

    #creating list
    cartList = []

    # creating dict
    productDict = {}
 
    # populating list with products
    productDict = {
        "TSHIRT" : Product("TSHIRT", "Clothing", 1000, 10),
        "JACKET" : Product("JACKET", "Clothing", 2000, 5),
        "CAP" : Product("CAP", "Clothing", 500, 20),
        "NOTEBOOK" : Product("NOTEBOOK", "Stationery", 200, 20),
        "PENS" : Product("PENS", "Stationery", 300, 10),
        "MARKERS" : Product("MARKERS", "Stationery", 500, 5)
    }

    # maximum clothing purchase limit
    clothingMax = 2

    # maximum stationery purchase limit
    stationeryMax = 3

    #sales tax 
    salesTax = 10

    #minimum amount to avail discount
    minimumAmountToAvailDiscount = 1000

    #additional discount
    additionalDiscount = 5

    #minimum amount to avail additional discount
    minimumAmountToAvailAdditionalDiscount = 3000

    #total discount
    totalDiscount = 0

    #total amount to pay
    totalAmountToPay = 0

    #to get the maximum purchase limit for the category of the selected product.
    def getMaxPurchaseLimitByCategory(name):
        #check if the product exists in the inventory,
        # If present, return the maximum limit for the category to which the product belongs.
        if name in productDict.keys():
            limit = 0
            category = productDict[name].category
            if category == "Clothing":
                limit = clothingMax
            else:
                limit = stationeryMax
            return  limit

    #to get the discount percentage for the selected product
    def getDiscount(name):
        if name in productDict.keys():
            return productDict[name].discount

    #to get the price for the selected product
    def getPrice(name):
        if name in productDict.keys():
            return productDict[name].originalPrice

    #handling the inputs and generating approriate outputs
    for line in lines:
        paramList = line.split()

        #Check the limit and add the product to cart if the command is "ADD_ITEM"
        if paramList[0] == "ADD_ITEM":
            maxLimit = getMaxPurchaseLimitByCategory(paramList[1])
            if int(paramList[2]) <= maxLimit:
                cartList.append(CartItem(paramList[1], int(paramList[2])))
                output = "ITEM_ADDED" 
                print(output)
            else:
                output = "ERROR_QUANTITY_EXCEEDED" 
                print(output)

        #Calculate the total amount to be paid after calculating discounts and sales tax.
        elif paramList[0] == "PRINT_BILL":
                for each in cartList:
                    #for each item in the cart, calculate the total amount and total discount that can be applied
                    discount = getDiscount(each.name)
                    amount = each.quantity * getPrice(each.name)
                    discountApplied = amount * (discount / 100)
                    totalAmountToPay += amount
                    totalDiscount += discountApplied

                #check if eligible to avail discount
                if totalAmountToPay > minimumAmountToAvailDiscount:
                    totalAmountToPay -= totalDiscount

                    #check if eligible to avail additional discount
                    if totalAmountToPay > minimumAmountToAvailAdditionalDiscount:
                        discountApplied = totalAmountToPay * (additionalDiscount / 100)
                        totalAmountToPay -= discountApplied
                        totalDiscount += discountApplied

                #set total discount back to 0
                else:
                    discountApplied = totalAmountToPay 
                    totalDiscount = 0.0
                
                #add sales tax after applying all eligible discounts
                afterTax = totalAmountToPay * (salesTax / 100)
                totalAmountToPay = totalAmountToPay + afterTax

                #print outputs
                print("TOTAL_DISCOUNT","%.2f" % totalDiscount, sep = " ")
                print("TOTAL_AMOUNT_TO_PAY","%.2f" % totalAmountToPay, sep = " ")
               

    
if __name__ == "__main__":
    main()