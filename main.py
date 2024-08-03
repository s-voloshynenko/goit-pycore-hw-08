from data_handler import load_data, save_data
from address_book import listen_commands

def main():
    book = load_data()
    listen_commands(book, on_exit=save_data)

if __name__ == "__main__":
    main()
