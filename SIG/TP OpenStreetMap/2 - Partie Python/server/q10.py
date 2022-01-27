import argparse, database as db

# ------- Question 10 --------
# Écrivez un petit programme de test prenant un argument en ligne de commande, et affichant
# tous les noms et coordonnées géographiques des points dont le nom ressemble à l'argument.

def main(args):
    query = f"SELECT tags->'name', linestring FROM ways WHERE tags->'name' LIKE '{args.name}';"
    with db.execute_query(query) as cursor:
        for name, linestring in cursor:
            for x, y in linestring:
                print(f'{name}\t [X:{x:.7f} | Y:{y:.7f}]')
    db.close_connection()

if __name__ == '__main__':
    # Create and configure the argument parser
    parser = argparse.ArgumentParser(
        description = "Displays the name and coordinates of all points whose name is similar to the argument")
    parser.add_argument(dest = "name")
    # Parse args
    args = parser.parse_args()
    # Call main function
    main(args)
