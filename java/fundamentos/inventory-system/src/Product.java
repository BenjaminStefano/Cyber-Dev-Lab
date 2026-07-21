public class Product {
    private int ID;
    private String Name;
    private int Units;
    private int unitPrice;

    // Instance field declarations
    public Product() {
        this.ID = 0; // Inicializa el ID de los productos en 0
        this.Name = ""; // Inicializa el nombre de los Productos como "None"
        this.Units = 0; // Inicializa el stock en 0
        this.unitPrice = 0; // Inicializa el precio en 0
    }
    public Product(int number, String name, int qty, int price) {
        this.ID = number; // Inicializa el ID de los productos con el valor del parámetro number
        this.Name = name; // Inicializa el nombre de los Productos con el valor del parámetro name
        this.Units = qty; // Inicializa el stock con el valor del parámetro qty
        this.unitPrice = price; // Inicializa el precio con el valor del parámetro price
    }

    // Getters and Setters for the fields
    public int getID() {
        return ID;
    }

    public void setID(int ID) {
        this.ID = ID;
    }

    public String getName() {
        return Name;
    }

    public void setName(String Name) {
        this.Name = Name;
    }

    public int getUnits() {
        return Units;
    }

    public void setUnits(int Units) {
        this.Units = Units;
    }

    public int getUnitPrice() {
        return unitPrice;
    }

    public void setUnitPrice(int unitPrice) {
        this.unitPrice = unitPrice;
    }
    @Override
    public String toString() {
        return "Item Number : " + ID + "\n" +
                "Name : " + Name + "\n" +
                "Quantity in stock: " + Units + "\n" +
                "Price : " + unitPrice;
    }
}

