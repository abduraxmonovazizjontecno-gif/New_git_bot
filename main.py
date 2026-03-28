from backend import Chat
class ChatUI:
    def message(self):
        messages = Chat().get_massage()
        for message in messages:
            text , user_id , username = message.values()
            print(f"{username} ({user_id}) : text")
        input("Back clik enter for back ")
        self.main()

    def send_massage(self):
        user_id = int(input("user_id :"))
        massage = input("massage :")
        Chat(user_id=user_id).send_massage(massage)
        self.main()

    def abs(self):
        ads_masssage = input("Reklama habarlar:")
        Chat().send_ads(ads_masssage)
        print("Hamma habarlar yuborildi")
        self.main()

    def main(self):
        menu = """
        1) xabalar
        2) xabarlar yuborish
        3) reklama
        4) Exit
    >>>"""
        choice = input(menu)
        match choice:
            case "1":
                self.message()
            case "2":
                self.send_massage()
            case "3":
                self.abs()
            case "4":
                print("Dastur foydalanuvchi tomonidan tohtatildi")
                return
ChatUI().main()