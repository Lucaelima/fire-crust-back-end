-- Create ENUM type for category if not exists
DO $$ BEGIN
  CREATE TYPE menu_category AS ENUM ('pizza', 'drink', 'side', 'dessert');
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- Create menu_items table if not exists
CREATE TABLE IF NOT EXISTS menu_items (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  description TEXT DEFAULT '',
  category menu_category NOT NULL,
  price FLOAT NOT NULL,
  is_available BOOLEAN DEFAULT true
);

-- Insert menu items
INSERT INTO menu_items (name, description, category, price, is_available)
VALUES
  ('Pizza Margherita', 'Molho de tomate, muçarela, manjericão fresco e azeite', 'pizza', 49.90, true),
  ('Pizza Calabresa', 'Calabresa artesanal, cebola roxa e muçarela', 'pizza', 54.90, true),
  ('Pizza Quatro Queijos', 'Muçarela, provolone, parmesão e gorgonzola', 'pizza', 59.90, true),
  ('Pizza Pepperoni', 'Pepperoni fatiado, muçarela e orégano', 'pizza', 57.90, true),
  ('Refrigerante Lata', 'Coca-Cola, Guaraná ou Sprite - 350ml', 'drink', 7.50, true),
  ('Suco Natural', 'Laranja ou limão - 400ml', 'drink', 11.00, true),
  ('Batata Rústica', 'Porção de batata rústica com ervas', 'side', 22.00, true),
  ('Borda Recheada', 'Adicional de borda recheada de catupiry', 'side', 12.00, true),
  ('Brownie com Sorvete', 'Brownie de chocolate com sorvete de creme', 'dessert', 18.00, true),
  ('Pudim da Casa', 'Pudim de leite condensado da Fire Crust', 'dessert', 14.00, true)
ON CONFLICT (name) DO UPDATE
SET
  description = EXCLUDED.description,
  category = EXCLUDED.category,
  price = EXCLUDED.price,
  is_available = EXCLUDED.is_available;
