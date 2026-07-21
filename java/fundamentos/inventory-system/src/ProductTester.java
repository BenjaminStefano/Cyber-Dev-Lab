public class ProductTester {
    public static void main(String[] args) {
        // Creando dos productos con el constructor predeterminado
        Product producto1 = new Product();
        Product producto2 = new Product();
        
        // Creando cuatro productos con valores para los argumentos
        Product producto3 = new Product(42312, "Pantalla Celular", 15, 20000);
        Product producto4 = new Product(186791, "howToTrainYouDragonDVD", 120, 10000);
        Product producto5 = new Product(24623, "justinBieberCD", 350, 30000);
        Product producto6 = new Product(104, "mazeRunnerDVD", 13, 13000);
        
        // Mostrando los productos creados
        System.out.println("=== Producto 1 (Constructor predeterminado) ===");
        System.out.println(producto1);
        System.out.println("\n=== Producto 2 (Constructor predeterminado) ===");
        System.out.println(producto2);
        System.out.println("\n=== Producto 3 (Con valores) ===");
        System.out.println(producto3);
        System.out.println("\n=== Producto 4 (Con valores) ===");
        System.out.println(producto4);
        System.out.println("\n=== Producto 5 (Con valores) ===");
        System.out.println(producto5);
        System.out.println("\n=== Producto 6 (Con valores) ===");
        System.out.println(producto6);
    }
}
