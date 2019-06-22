from tqdm import tqdm

streets = {}
numbers = {}
zip_codes = {}
cities = {}

full_addresses = {}

def parse_line(line):
        line = line.split(',')

        number = line[2]
        street = line[3]
        city = line[5]
        zip_code = line[8]

        full_address = street + " " + number + " " + city + " " + zip_code

        full_addresses[full_address] = 1

        if street and street not in streets:
            streets[street] = 1

        if number and number not in numbers:
            numbers[number] = 1

        if zip_code and zip_code not in zip_codes:
            zip_codes[zip_code] = 1

        if city and city not in cities:
            cities[city] = 1


def dict_to_file(file_name, att_name, dict):
    with open(file_name, 'w') as fp:
        fp.write("~["+att_name+"]\n")
        for elem in dict.keys():
            fp.write("    "+str(elem)+"\n")



if __name__ == "__main__":
    try:
        with open('addresses.csv', 'r') as fp:
            line = fp.readline()

            print("Parsing file addresses.csv line by line...")
            for p in tqdm(range(6921859)):
                parse_line(line)
                line = fp.readline()
            print("Finished Parsing!")
    finally:
        print("Saving parsed content to files...")
        dict_to_file("streets.chatito", "street", streets)
        dict_to_file("numbers.chatito", "number", numbers)
        dict_to_file("zip_codes.chatito", "zip_code", zip_codes)
        dict_to_file("cities.chatito", "city", cities)
        dict_to_file("full_addresses.chatito", "full_address", full_addresses)
        print("Done!")
